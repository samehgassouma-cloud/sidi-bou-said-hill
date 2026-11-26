/* Terrasse de café en gradins — Three.js r128.
   Tout est procédural (matières peintes au canvas), caméra sphérique maison,
   pas d'OrbitControls, pas de CapsuleGeometry. La sélection de table se fait au
   Raycaster sur des maillages individuels : c'est ce qui permet de cliquer une table
   précise, donc chaque table reste un objet à part malgré le coût. */
window.buildCafe = function (THREE, canvas, opts) {
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true });
  } catch (err) { return null; }
  let ctx = null;
  try { ctx = renderer.getContext(); } catch (err) { ctx = null; }
  if (!ctx) return null;

  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.setSize(canvas.clientWidth || innerWidth, canvas.clientHeight || innerHeight);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0xBBD8EA, 0.006);
  const camera = new THREE.PerspectiveCamera(46, 1, 0.1, 900);

  function paint(w, h, draw) {
    const c = document.createElement("canvas");
    c.width = w; c.height = h;
    draw(c.getContext("2d"), w, h);
    const tex = new THREE.CanvasTexture(c);
    tex.anisotropy = 4;
    return tex;
  }

  const tileTex = paint(256, 256, (g, w, h) => {
    g.fillStyle = "#EFE7D6"; g.fillRect(0, 0, w, h);
    g.strokeStyle = "rgba(150,138,116,.45)"; g.lineWidth = 2;
    for (let i = 0; i <= w; i += 32) {
      g.beginPath(); g.moveTo(i, 0); g.lineTo(i, h); g.stroke();
      g.beginPath(); g.moveTo(0, i); g.lineTo(w, i); g.stroke();
    }
    for (let i = 0; i < 500; i++) {
      g.fillStyle = "rgba(255,255,255,.35)";
      g.fillRect(Math.random() * w, Math.random() * h, 3, 3);
    }
  });
  tileTex.wrapS = tileTex.wrapT = THREE.RepeatWrapping;
  tileTex.repeat.set(8, 8);

  // natte tressée : c'est la matière qui donne son nom au Café des Nattes
  const mattingTex = paint(128, 128, (g, w, h) => {
    g.fillStyle = "#D9C08A"; g.fillRect(0, 0, w, h);
    const cell = 16;
    for (let y = 0; y < h; y += cell) {
      for (let x = 0; x < w; x += cell) {
        const alt = ((x + y) / cell) % 2 === 0;
        g.fillStyle = alt ? "#C8AC74" : "#E4CE9E";
        g.fillRect(x, y, cell, cell);
        g.strokeStyle = "rgba(120,98,60,.35)"; g.lineWidth = 1;
        for (let k = 2; k < cell; k += 4) {
          g.beginPath();
          if (alt) { g.moveTo(x + k, y); g.lineTo(x + k, y + cell); }
          else { g.moveTo(x, y + k); g.lineTo(x + cell, y + k); }
          g.stroke();
        }
      }
    }
  });
  mattingTex.wrapS = mattingTex.wrapT = THREE.RepeatWrapping;
  mattingTex.repeat.set(3, 3);

  // colonne andalouse : bandes rouges et vertes en spirale, liseré blanc
  const columnTex = paint(128, 256, (g, w, h) => {
    g.fillStyle = "#F6F1E6"; g.fillRect(0, 0, w, h);
    g.lineWidth = 13;
    for (let i = -h; i < h * 2; i += 34) {
      g.strokeStyle = "#B33A32";
      g.beginPath(); g.moveTo(-10, i); g.lineTo(w + 10, i + 26); g.stroke();
      g.strokeStyle = "#2F6B43";
      g.beginPath(); g.moveTo(-10, i + 17); g.lineTo(w + 10, i + 43); g.stroke();
    }
  });
  columnTex.wrapS = columnTex.wrapT = THREE.RepeatWrapping;

  const seaTex = paint(512, 512, (g, w, h) => {
    g.fillStyle = "#1A5C89"; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 800; i++) {
      g.fillStyle = "rgba(255,255,255," + (0.04 + Math.random() * 0.1) + ")";
      g.fillRect(Math.random() * w, Math.random() * h, 16 + Math.random() * 30, 1.5);
    }
  });
  seaTex.wrapS = seaTex.wrapT = THREE.RepeatWrapping;
  seaTex.repeat.set(8, 8);

  const skyTex = paint(64, 512, (g, w, h) => {
    const grd = g.createLinearGradient(0, 0, 0, h);
    grd.addColorStop(0, "#1D4E77"); grd.addColorStop(.5, "#8CC0DE");
    grd.addColorStop(.85, "#F2DDB4"); grd.addColorStop(1, "#E8B678");
    g.fillStyle = grd; g.fillRect(0, 0, w, h);
  });

  scene.add(new THREE.Mesh(new THREE.SphereGeometry(700, 32, 20),
    new THREE.MeshBasicMaterial({ map: skyTex, side: THREE.BackSide, fog: false })));

  scene.add(new THREE.HemisphereLight(0xCDE7F7, 0x6B5A44, 0.9));
  const sun = new THREE.DirectionalLight(0xFFE3B0, 1.05);
  sun.position.set(-60, 90, 40);
  sun.castShadow = true;
  sun.shadow.mapSize.set(1024, 1024);
  sun.shadow.camera.left = -60; sun.shadow.camera.right = 60;
  sun.shadow.camera.top = 60; sun.shadow.camera.bottom = -60;
  scene.add(sun);

  // mer, au-delà de la falaise
  const seaGeo = new THREE.PlaneGeometry(900, 900, 60, 60);
  const sea = new THREE.Mesh(seaGeo, new THREE.MeshPhongMaterial({
    map: seaTex, color: 0x2E7BB5, shininess: 110, specular: 0xCFEAFB }));
  sea.rotation.x = -Math.PI / 2;
  sea.position.set(0, -14, 120);
  scene.add(sea);
  const seaBase = seaGeo.attributes.position.array.slice();

  const floorMat = new THREE.MeshLambertMaterial({ map: tileTex });
  const wallMat = new THREE.MeshLambertMaterial({ color: 0xF6F1E6 });
  const blueMat = new THREE.MeshLambertMaterial({ color: 0x2E6FA8 });
  const goldMat = new THREE.MeshLambertMaterial({ color: 0xD4A017 });
  const woodMat = new THREE.MeshLambertMaterial({ color: 0x7A5A38 });

  const mattingMat = new THREE.MeshLambertMaterial({ map: mattingTex });
  const columnMat = new THREE.MeshLambertMaterial({ map: columnTex });
  const beamMat = new THREE.MeshLambertMaterial({ color: 0x7A4A2A });

  const LAYOUT = opts.layout || "cliff";
  const LEVELS = opts.levels || [{ z: -10, y: 4.5 }, { z: 0, y: 2.2 }, { z: 10, y: 0 }];
  const levelY = function (z) {
    const lv = LEVELS.find(function (l) { return l.z === z; });
    return lv ? lv.y : 0;
  };

  function deck(z, y, depth, width) {
    const d = new THREE.Mesh(new THREE.BoxGeometry(width || 34, 1.2, depth || 9.4), floorMat);
    d.position.set(0, y, z);
    d.receiveShadow = true;
    scene.add(d);
    const riser = new THREE.Mesh(new THREE.BoxGeometry(width || 34, 3.4, 0.6), wallMat);
    riser.position.set(0, y - 1.4, z + (depth || 9.4) / 2);
    scene.add(riser);
  }

  if (LAYOUT === "nattes") {
    /* ---------- Café des Nattes : la salle et sa terrasse, en haut du grand escalier ----------
       Éléments retenus parce qu'ils sont documentés : escalier blanc raide, porte jaune
       et noire, doukkanas garnies de nattes, colonnade torsadée rouge et verte,
       plafond à solives. La disposition des tables reste une estimation. */
    const platform = new THREE.Mesh(new THREE.BoxGeometry(34, 3.2, 34), floorMat);
    platform.position.set(0, 1.6, -6);
    platform.receiveShadow = true;
    scene.add(platform);

    // le grand escalier blanc, qui monte de la placette
    for (let i = 0; i < 9; i++) {
      const st = new THREE.Mesh(new THREE.BoxGeometry(15, 0.42, 1.5), wallMat);
      st.position.set(0, 0.2 + i * 0.36, 11 + (8 - i) * 1.5);
      st.receiveShadow = true;
      scene.add(st);
    }

    // façade et salle
    const facadeBack = new THREE.Mesh(new THREE.BoxGeometry(34, 12, 0.8), wallMat);
    facadeBack.position.set(0, 9.2, -23); facadeBack.castShadow = true; scene.add(facadeBack);
    [-1, 1].forEach(function (sx) {
      const side = new THREE.Mesh(new THREE.BoxGeometry(0.8, 12, 26), wallMat);
      side.position.set(sx * 16.6, 9.2, -10); side.castShadow = true; scene.add(side);
    });

    // doukkanas : banquettes maçonnées garnies de nattes, le long des murs
    [[-14.4, -14, 0.6, 22], [14.4, -14, 0.6, 22], [0, -22, 30, 0.6]].forEach(function (b) {
      const bench = new THREE.Mesh(new THREE.BoxGeometry(b[2] === 0.6 ? 2.6 : b[2], 1.1, b[3] === 0.6 ? 2.6 : b[3]), wallMat);
      bench.position.set(b[0], 3.75, b[1]);
      bench.receiveShadow = true;
      const mat = new THREE.Mesh(new THREE.BoxGeometry(
        (b[2] === 0.6 ? 2.6 : b[2]) * 0.96, 0.12, (b[3] === 0.6 ? 2.6 : b[3]) * 0.96), mattingMat);
      mat.position.set(b[0], 4.36, b[1]);
      scene.add(bench, mat);
    });

    // colonnade andalouse + plafond à solives
    [-8, 0, 8].forEach(function (x) {
      [-18, -8].forEach(function (z) {
        const col = new THREE.Mesh(new THREE.CylinderGeometry(0.75, 0.85, 8.4, 14), columnMat);
        col.position.set(x, 7.4, z); col.castShadow = true;
        const cap = new THREE.Mesh(new THREE.BoxGeometry(2.2, 1, 2.2), goldMat);
        cap.position.set(x, 11.8, z);
        scene.add(col, cap);
      });
    });
    for (let i = -4; i <= 4; i++) {
      const beam = new THREE.Mesh(new THREE.BoxGeometry(32, 0.5, 0.5), beamMat);
      beam.position.set(0, 12.6, -22 + (i + 4) * 2.2);
      scene.add(beam);
    }
    const ceiling = new THREE.Mesh(new THREE.BoxGeometry(33, 0.4, 24), wallMat);
    ceiling.position.set(0, 13.1, -13);
    scene.add(ceiling);

    // la porte jaune et noire de la façade
    const door = new THREE.Mesh(new THREE.BoxGeometry(3.6, 6, 0.3),
      new THREE.MeshLambertMaterial({ color: 0xE0B23A }));
    door.position.set(0, 6.4, -6.8);
    const frame = new THREE.Mesh(new THREE.BoxGeometry(4.4, 6.8, 0.2),
      new THREE.MeshLambertMaterial({ color: 0x1C1C1C }));
    frame.position.set(0, 6.6, -6.95);
    scene.add(frame, door);

    // arcs bleus ouvrant la terrasse sur la placette
    [-9, 0, 9].forEach(function (x) {
      const arc = new THREE.Mesh(new THREE.TorusGeometry(3.1, 0.4, 8, 20, Math.PI), blueMat);
      arc.position.set(x, 9.4, -6.6);
      scene.add(arc);
    });

    // toits du village en contrebas : ce que la terrasse regarde vraiment
    for (let i = 0; i < 16; i++) {
      const h = 3 + (i % 4) * 1.4;
      const house = new THREE.Mesh(new THREE.BoxGeometry(5, h, 5), wallMat);
      house.position.set(-26 + (i % 8) * 7.5, h / 2 - 4, 26 + Math.floor(i / 8) * 8);
      scene.add(house);
      const d2 = new THREE.Mesh(new THREE.BoxGeometry(1.2, h * 0.5, 0.2), blueMat);
      d2.position.set(house.position.x, house.position.y - h * 0.2, house.position.z + 2.6);
      scene.add(d2);
    }
    sea.position.set(0, -26, 150);

  } else {
    /* ---------- Café Sidi Chabaane : entrée, gradins, falaise et marina ----------
       Trois plans se répondent : on entre par le haut, on descend de terrasse en
       terrasse, et tout regarde le golfe où les bateaux sont amarrés. */
    LEVELS.forEach(function (lv) { deck(lv.z, lv.y, 9.4, 34); });

    // --- l'entrée, en haut : mur blanc, portail bleu en plein cintre, enseigne, escalier
    const entryWall = new THREE.Mesh(new THREE.BoxGeometry(34, 13, 1), wallMat);
    entryWall.position.set(0, 13, -20); entryWall.castShadow = true;
    scene.add(entryWall);

    const gateArch = new THREE.Mesh(new THREE.TorusGeometry(4.2, 0.62, 10, 24, Math.PI), blueMat);
    gateArch.position.set(0, 11.4, -19.3);
    const gateL = new THREE.Mesh(new THREE.BoxGeometry(0.62, 5.4, 0.62), blueMat);
    gateL.position.set(-4.2, 8.7, -19.3);
    const gateR = gateL.clone(); gateR.position.x = 4.2;
    const gateOpen = new THREE.Mesh(new THREE.BoxGeometry(8.4, 11, 0.4),
      new THREE.MeshBasicMaterial({ color: 0x0B2436 }));
    gateOpen.position.set(0, 11.5, -20.2);
    scene.add(gateArch, gateL, gateR, gateOpen);

    // enseigne au-dessus du portail
    const signBoard = new THREE.Mesh(new THREE.BoxGeometry(11, 2.2, 0.3),
      new THREE.MeshLambertMaterial({ color: 0xF3EFE6 }));
    signBoard.position.set(0, 17.4, -19.2);
    const signFrame = new THREE.Mesh(new THREE.BoxGeometry(11.8, 2.9, 0.18), goldMat);
    signFrame.position.set(0, 17.4, -19.35);
    scene.add(signFrame, signBoard);

    // lanternes de part et d'autre de l'entrée
    [-6.6, 6.6].forEach(function (x) {
      const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 2.2, 6), goldMat);
      arm.position.set(x, 15.4, -19.2);
      const lamp = new THREE.Mesh(new THREE.OctahedronGeometry(0.9),
        new THREE.MeshBasicMaterial({ color: 0xFFD98A }));
      lamp.position.set(x, 14, -19.2);
      scene.add(arm, lamp);
    });

    // escalier qui descend de l'entrée vers la première terrasse
    for (let i = 0; i < 7; i++) {
      const st = new THREE.Mesh(new THREE.BoxGeometry(9, 0.4, 1.3), floorMat);
      st.position.set(0, 8.2 - i * 0.42, -18.6 + i * 1.3);
      st.receiveShadow = true;
      scene.add(st);
    }

    // bougainvilliers en cascade sur le mur d'entrée
    const petalMat = new THREE.MeshLambertMaterial({ color: 0xC4327A });
    [-12, -8, 9, 13].forEach(function (x, bi) {
      for (let k = 0; k < 12; k++) {
        const puff = new THREE.Mesh(new THREE.IcosahedronGeometry(0.8 + (k % 3) * 0.35, 0), petalMat);
        puff.position.set(x + ((k * 7) % 5) - 2, 17 - k * 0.9, -18.6 + ((k + bi) % 3) * 0.5);
        scene.add(puff);
      }
    });

    // --- la falaise sous la dernière terrasse
    const cliffRock = new THREE.Mesh(new THREE.BoxGeometry(40, 30, 12),
      new THREE.MeshLambertMaterial({ color: 0xB9A88C }));
    cliffRock.position.set(0, -15, 28);
    cliffRock.receiveShadow = true;
    scene.add(cliffRock);
    for (let i = 0; i < 7; i++) {
      const ledge = new THREE.Mesh(new THREE.BoxGeometry(6 + (i % 3) * 3, 1.6, 4),
        new THREE.MeshLambertMaterial({ color: 0xA8977C }));
      ledge.position.set(-16 + i * 5.5, -4 - (i % 4) * 3.4, 24 + (i % 2) * 2);
      scene.add(ledge);
    }

    // --- la marina : digue, pontons, bateaux amarrés
    const marina = new THREE.Group();
    const breakwater = new THREE.Mesh(new THREE.BoxGeometry(78, 3, 5),
      new THREE.MeshLambertMaterial({ color: 0x9A8B72 }));
    breakwater.position.set(6, -12.5, 96);
    const breakwater2 = new THREE.Mesh(new THREE.BoxGeometry(5, 3, 34),
      new THREE.MeshLambertMaterial({ color: 0x9A8B72 }));
    breakwater2.position.set(-33, -12.5, 79);
    const lightTower = new THREE.Mesh(new THREE.CylinderGeometry(0.9, 1.2, 6, 10), wallMat);
    lightTower.position.set(-33, -8, 96);
    const lightTop = new THREE.Mesh(new THREE.SphereGeometry(1.1, 12, 8),
      new THREE.MeshBasicMaterial({ color: 0x5FBF7E }));
    lightTop.position.set(-33, -4.6, 96);
    marina.add(breakwater, breakwater2, lightTower, lightTop);

    [62, 76].forEach(function (pz) {
      const pontoon = new THREE.Mesh(new THREE.BoxGeometry(52, 0.7, 2.6), woodMat);
      pontoon.position.set(0, -13.4, pz);
      marina.add(pontoon);
    });

    // les bateaux : coque, roof, mât, bôme, voile ferlée — et un léger balancement
    const boats = [];
    const hullMat = new THREE.MeshLambertMaterial({ color: 0xF3EFE6 });
    const deckMat = new THREE.MeshLambertMaterial({ color: 0xE2D6BE });
    for (let i = 0; i < 16; i++) {
      const side = i < 8 ? -1 : 1;
      const idx = i % 8;
      const bx = -22 + idx * 6.4;
      const bz = (i < 8 ? 62 : 76) + side * 4.6;
      const big = idx % 3 === 0;
      const b = new THREE.Group();

      const hull = new THREE.Mesh(new THREE.BoxGeometry(2.6, 1.3, big ? 9 : 6.4), hullMat);
      hull.position.y = 0.4;
      const bandeau = new THREE.Mesh(new THREE.BoxGeometry(2.7, 0.28, big ? 9.1 : 6.5), blueMat);
      bandeau.position.y = 1.0;
      const cabin = new THREE.Mesh(new THREE.BoxGeometry(1.9, 0.9, big ? 3.4 : 2.4), deckMat);
      cabin.position.set(0, 1.5, -0.4);
      b.add(hull, bandeau, cabin);

      if (idx % 4 !== 2) {   // voiliers : mât + bôme + voile ferlée
        const mast = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.12, big ? 12 : 9, 6), wallMat);
        mast.position.set(0, (big ? 6 : 4.5) + 1.2, 0);
        const boom = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.16, big ? 4.4 : 3.4), wallMat);
        boom.position.set(0, 2.6, 1.4);
        const furled = new THREE.Mesh(new THREE.CylinderGeometry(0.34, 0.34, big ? 4.2 : 3.2, 8),
          new THREE.MeshLambertMaterial({ color: 0xEDE6D6 }));
        furled.rotation.x = Math.PI / 2;
        furled.position.set(0, 2.85, 1.4);
        b.add(mast, boom, furled);
      } else {               // vedette : passerelle et main courante
        const bridge = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.7, 1.6), hullMat);
        bridge.position.set(0, 2.3, -0.4);
        b.add(bridge);
      }

      b.position.set(bx, -13.2, bz);
      b.rotation.y = side > 0 ? 0 : Math.PI;
      b.userData.phase = i * 0.7;
      b.userData.baseY = -13.2;
      boats.push(b);
      marina.add(b);
    }
    scene.add(marina);
    window.__cafeBoats = boats;

    // --- le golfe : ligne d'horizon et Boukornine au loin
    const cape = new THREE.Mesh(new THREE.BoxGeometry(150, 6, 20),
      new THREE.MeshLambertMaterial({ color: 0x7E8E9C }));
    cape.position.set(-90, -11, 210);
    const mountain = new THREE.Mesh(new THREE.ConeGeometry(46, 26, 5),
      new THREE.MeshLambertMaterial({ color: 0x6C7F92 }));
    mountain.position.set(70, -2, 300);
    const mountain2 = new THREE.Mesh(new THREE.ConeGeometry(34, 18, 5),
      new THREE.MeshLambertMaterial({ color: 0x7A8CA0 }));
    mountain2.position.set(112, -6, 320);
    scene.add(cape, mountain, mountain2);

    sea.position.set(0, -14, 80);
  }

  // garde-corps côté vue
  const railZ = LAYOUT === "nattes" ? 10 : 23;
  const railY = LAYOUT === "nattes" ? 3.9 : 1.6;
  const rail = new THREE.Mesh(new THREE.BoxGeometry(34, 0.5, 0.5), goldMat);
  rail.position.set(0, railY, railZ);
  scene.add(rail);
  for (let i = -8; i <= 8; i++) {
    const post = new THREE.Mesh(new THREE.BoxGeometry(0.3, 1.6, 0.3), goldMat);
    post.position.set(i * 2, railY - 0.8, railZ);
    scene.add(post);
  }

  /* ---------- tables sélectionnables ---------- */
  const tableGroup = new THREE.Group();
  const meshes = [];
  const ZY = { terrace: 2.2, belvedere: 0, inside: 6.5 };

  function buildTable(t) {
    const g = new THREE.Group();
    const y = levelY(t.z) + 0.6;

    const low = (t.zone === "inside" && LAYOUT === "nattes");
    const th = low ? 0.85 : 1.5;
    const top = new THREE.Mesh(new THREE.CylinderGeometry(low ? 1.1 : 1.5, low ? 1.1 : 1.5, 0.22, 20), woodMat);
    top.position.y = th; top.castShadow = true;
    const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.3, th, 10), goldMat);
    leg.position.y = th / 2;
    g.add(top, leg);

    for (let s = 0; s < t.seats; s++) {
      const a = (s / t.seats) * Math.PI * 2;
      // dans la salle aux nattes on s'assoit sur des doukkanas garnies, pas sur des tabourets
      const st = t.zone === "inside" && LAYOUT === "nattes"
        ? new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.6, 1.5), mattingMat)
        : new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.55, 0.9, 12), blueMat);
      st.position.set(Math.cos(a) * 2.3, t.zone === "inside" && LAYOUT === "nattes" ? 0.3 : 0.45, Math.sin(a) * 2.3);
      st.castShadow = true;
      g.add(st);
    }

    if (t.power) {
      const box = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.5, 0.2),
        new THREE.MeshBasicMaterial({ color: 0x00B4D8 }));
      box.position.set(0, th + 0.6, 0);
      g.add(box);
      const halo = new THREE.Mesh(new THREE.RingGeometry(1.7, 2.0, 24),
        new THREE.MeshBasicMaterial({ color: 0x00B4D8, transparent: true, opacity: 0.45,
                                      side: THREE.DoubleSide }));
      halo.rotation.x = -Math.PI / 2;
      halo.position.y = 0.05;
      g.add(halo);
      g.userData.halo = halo;
    }

    // disque de sélection : c'est lui qu'on vise au Raycaster
    const pick = new THREE.Mesh(new THREE.CylinderGeometry(2.6, 2.6, 0.1, 20),
      new THREE.MeshBasicMaterial({ color: 0xD4A017, transparent: true, opacity: 0.0 }));
    pick.position.y = 0.06;
    pick.userData.tableId = t.id;
    g.add(pick);
    g.userData.pick = pick;
    g.userData.id = t.id;

    g.position.set(t.x, y, t.z);
    tableGroup.add(g);
    meshes.push(pick);
    return g;
  }

  const byId = {};
  (opts.tables || []).forEach(function (t) { byId[t.id] = buildTable(t); });
  scene.add(tableGroup);

  // parasols sur le niveau ombragé
  (opts.tables || []).filter(function (t) { return t.shade && t.zone !== "inside"; })
    .forEach(function (t) {
      const g = byId[t.id];
      const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 4.4, 8), woodMat);
      pole.position.y = 2.2;
      const top = new THREE.Mesh(new THREE.ConeGeometry(3, 1.1, 12),
        new THREE.MeshLambertMaterial({ color: 0xF3EFE6 }));
      top.position.y = 4.4; top.castShadow = true;
      g.add(pole, top);
    });

  /* ---------- caméra sphérique ---------- */
  const START = (opts.layout === "nattes")
    ? { r: 40, theta: Math.PI / 2, phi: 0.95, ty: 6 }    // on regarde la salle depuis la terrasse
    : { r: 58, theta: -Math.PI / 2, phi: 0.86, ty: 5 };  // depuis l'entrée, la vue plonge sur la mer
  const cam = { r: START.r, theta: START.theta, phi: START.phi };
  let want = { r: START.r, theta: START.theta, phi: START.phi };
  const target = new THREE.Vector3(0, START.ty, 0);
  const wantTarget = new THREE.Vector3(0, START.ty, 0);

  function place() {
    cam.r += (want.r - cam.r) * 0.06;
    cam.theta += (want.theta - cam.theta) * 0.06;
    cam.phi += (want.phi - cam.phi) * 0.06;
    target.lerp(wantTarget, 0.08);
    camera.position.set(
      target.x + cam.r * Math.sin(cam.phi) * Math.cos(cam.theta),
      target.y + cam.r * Math.cos(cam.phi),
      target.z + cam.r * Math.sin(cam.phi) * Math.sin(cam.theta)
    );
    camera.lookAt(target);
  }

  /* ---------- sélection ---------- */
  const ray = new THREE.Raycaster();
  const pointer = new THREE.Vector2();
  let selectedId = null;

  function markSelection(id) {
    selectedId = id;
    Object.keys(byId).forEach(function (k) {
      const g = byId[k];
      g.userData.pick.material.opacity = (k === id) ? 0.55 : 0.0;
      g.scale.setScalar(k === id ? 1.08 : 1);
    });
    if (id && byId[id]) {
      const p = byId[id].position;
      wantTarget.set(p.x, p.y + 2, p.z);
      want.r = 22; want.phi = 1.05;
      want.theta = Math.atan2(p.z + 12, p.x) - Math.PI / 2;
    }
  }

  function pickAt(clientX, clientY) {
    const box = canvas.getBoundingClientRect();
    pointer.x = ((clientX - box.left) / box.width) * 2 - 1;
    pointer.y = -((clientY - box.top) / box.height) * 2 + 1;
    ray.setFromCamera(pointer, camera);
    const hit = ray.intersectObjects(meshes, false)[0];
    if (hit) {
      const id = hit.object.userData.tableId;
      markSelection(id);
      if (opts.onPick) opts.onPick(id);
      return id;
    }
    return null;
  }

  let dragging = null, moved = 0;
  canvas.addEventListener("pointerdown", function (e) {
    dragging = { x: e.clientX, y: e.clientY, th: want.theta, ph: want.phi };
    moved = 0;
  });
  addEventListener("pointerup", function (e) {
    if (dragging && moved < 6) pickAt(e.clientX, e.clientY);
    dragging = null;
  }, { passive: true });
  addEventListener("pointermove", function (e) {
    if (!dragging) return;
    moved += Math.abs(e.movementX || 0) + Math.abs(e.movementY || 0);
    want.theta = dragging.th - (e.clientX - dragging.x) * 0.006;
    want.phi = Math.max(0.5, Math.min(1.35, dragging.ph - (e.clientY - dragging.y) * 0.004));
  }, { passive: true });
  canvas.addEventListener("wheel", function (e) {
    e.preventDefault();
    want.r = Math.max(12, Math.min(90, want.r * (e.deltaY > 0 ? 1.12 : 0.9)));
  });

  /* ---------- boucle ---------- */
  const clock = new THREE.Clock();
  let raf = 0;
  function frame() {
    const el = clock.elapsedTime;
    clock.getDelta();
    const arr = seaGeo.attributes.position.array;
    for (let i = 0; i < arr.length; i += 3) {
      arr[i + 2] = Math.sin((seaBase[i] + el * 22) * 0.02) * 1.1
                 + Math.cos((seaBase[i + 1] + el * 15) * 0.026) * 0.8;
    }
    seaGeo.attributes.position.needsUpdate = true;
    seaTex.offset.x = el * 0.005;

    // les bateaux suivent la houle, sans dériver de leur mouillage
    if (window.__cafeBoats) {
      window.__cafeBoats.forEach(function (b) {
        b.position.y = b.userData.baseY + Math.sin(el * 0.9 + b.userData.phase) * 0.16;
        b.rotation.z = Math.sin(el * 0.7 + b.userData.phase) * 0.03;
        b.rotation.x = Math.cos(el * 0.55 + b.userData.phase) * 0.02;
      });
    }

    Object.keys(byId).forEach(function (k) {
      const h = byId[k].userData.halo;
      if (h) h.material.opacity = 0.28 + Math.sin(el * 2 + k.length) * 0.16;
    });

    place();
    renderer.render(scene, camera);
    raf = requestAnimationFrame(frame);
  }
  frame();

  function resize() {
    const w = canvas.clientWidth || innerWidth, h = canvas.clientHeight || innerHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  addEventListener("resize", resize, { passive: true });
  resize();

  return {
    select: markSelection,
    overview: function () { want = { r: START.r, theta: START.theta, phi: START.phi }; wantTarget.set(0, START.ty, 0); },
    highlight: function (ids) {
      Object.keys(byId).forEach(function (k) {
        byId[k].visible = !ids || ids.indexOf(k) >= 0 || k === selectedId;
      });
    },
    resize: resize,
    stop: function () { cancelAnimationFrame(raf); }
  };
};
