/* Diorama cinématique de Sidi Bou Saïd — Three.js r128.
   Tout est procédural : aucune texture ni modèle importé, les matières sont
   peintes dans des <canvas> à l'exécution. Contraintes respectées :
   pas d'OrbitControls (caméra sphérique maison), pas de CapsuleGeometry,
   écouteurs passifs, et la scène ne se charge que si WebGL répond. */
window.buildScene = function (THREE, canvas) {
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: false });
  } catch (err) { return null; }
  // r128 a retiré renderer.context : on interroge le contexte par getContext().
  let ctx = null;
  try { ctx = renderer.getContext(); } catch (err) { ctx = null; }
  if (!ctx) return null;

  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.setSize(innerWidth, innerHeight);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(42, innerWidth / innerHeight, 0.5, 3000);
  scene.fog = new THREE.FogExp2(0x9DC2DC, 0.0032);

  /* ---------- matières peintes au canvas ---------- */
  function paint(w, h, draw) {
    const c = document.createElement("canvas");
    c.width = w; c.height = h;
    draw(c.getContext("2d"), w, h);
    const tex = new THREE.CanvasTexture(c);
    tex.anisotropy = 4;
    return tex;
  }

  const whitewash = paint(256, 256, (g, w, h) => {
    g.fillStyle = "#F4EFE4"; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 2600; i++) {
      const v = 218 + Math.random() * 34;
      g.fillStyle = `rgba(${v},${v - 4},${v - 14},0.35)`;
      g.fillRect(Math.random() * w, Math.random() * h, 2.2, 2.2);
    }
    g.strokeStyle = "rgba(190,182,166,0.35)"; g.lineWidth = 1;
    for (let y = 16; y < h; y += 34) { g.beginPath(); g.moveTo(0, y); g.lineTo(w, y + (Math.random() * 4 - 2)); g.stroke(); }
  });
  whitewash.wrapS = whitewash.wrapT = THREE.RepeatWrapping;

  // porte cloutée : le motif emblématique, dessiné point par point
  const doorTex = paint(256, 384, (g, w, h) => {
    g.fillStyle = "#2E6FA8"; g.fillRect(0, 0, w, h);
    g.fillStyle = "rgba(0,0,0,0.16)";
    for (let x = 8; x < w; x += 30) g.fillRect(x, 0, 3, h);
    g.strokeStyle = "#1B4B73"; g.lineWidth = 6; g.strokeRect(10, 10, w - 20, h - 20);
    g.fillStyle = "#E7D6A8";
    const rows = 9, cols = 6;
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const stagger = (r % 2) * 18;
        const x = 34 + c * 34 + stagger, y = 52 + r * 34;
        if (x > w - 24) continue;
        g.beginPath(); g.arc(x, y, 4.6, 0, Math.PI * 2); g.fill();
      }
    }
    g.strokeStyle = "#E7D6A8"; g.lineWidth = 3;
    g.beginPath(); g.arc(w / 2, h * 0.30, 62, Math.PI, 0); g.stroke();
    g.beginPath(); g.arc(w / 2, h * 0.30, 40, Math.PI, 0); g.stroke();
  });

  const seaTex = paint(512, 512, (g, w, h) => {
    g.fillStyle = "#12496F"; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 900; i++) {
      g.fillStyle = `rgba(255,255,255,${0.03 + Math.random() * 0.10})`;
      g.fillRect(Math.random() * w, Math.random() * h, 14 + Math.random() * 26, 1.4);
    }
  });
  seaTex.wrapS = seaTex.wrapT = THREE.RepeatWrapping;
  seaTex.repeat.set(6, 6);

  // zellige : damier d'étoiles à huit branches, peint au trait
  const zelligeTex = paint(256, 256, (g, w, h) => {
    g.fillStyle = "#F1EADC"; g.fillRect(0, 0, w, h);
    const cell = 64;
    for (let y = 0; y < h; y += cell) {
      for (let x = 0; x < w; x += cell) {
        const cx = x + cell / 2, cy = y + cell / 2, r = cell * 0.36;
        g.fillStyle = ((x + y) / cell) % 2 ? "#2E6FA8" : "#D4A017";
        g.beginPath();
        for (let k = 0; k < 16; k++) {
          const rad = k % 2 ? r * 0.46 : r;
          const a = (k / 16) * Math.PI * 2;
          const px = cx + Math.cos(a) * rad, py = cy + Math.sin(a) * rad;
          k ? g.lineTo(px, py) : g.moveTo(px, py);
        }
        g.fill();
      }
    }
    g.strokeStyle = "rgba(255,255,255,0.5)"; g.lineWidth = 2;
    for (let x = 0; x <= w; x += cell) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, h); g.stroke(); }
    for (let y = 0; y <= h; y += cell) { g.beginPath(); g.moveTo(0, y); g.lineTo(w, y); g.stroke(); }
  });
  zelligeTex.wrapS = zelligeTex.wrapT = THREE.RepeatWrapping;
  zelligeTex.repeat.set(4, 4);

  const skyTex = paint(64, 512, (g, w, h) => {
    const grd = g.createLinearGradient(0, 0, 0, h);
    grd.addColorStop(0.00, "#0B2A4A");
    grd.addColorStop(0.34, "#2E7BB5");
    grd.addColorStop(0.62, "#9FC8E2");
    grd.addColorStop(0.82, "#F3D9A4");
    grd.addColorStop(1.00, "#E9B26A");
    g.fillStyle = grd; g.fillRect(0, 0, w, h);
  });

  /* ---------- ciel + soleil ---------- */
  const sky = new THREE.Mesh(
    new THREE.SphereGeometry(1400, 32, 20),
    new THREE.MeshBasicMaterial({ map: skyTex, side: THREE.BackSide, fog: false })
  );
  scene.add(sky);

  const sunSprite = new THREE.Mesh(
    new THREE.CircleGeometry(46, 32),
    new THREE.MeshBasicMaterial({ color: 0xFFE6B0, transparent: true, opacity: 0.92, fog: false })
  );
  sunSprite.position.set(-620, 190, -900);
  sunSprite.lookAt(0, 60, 0);
  scene.add(sunSprite);

  /* ---------- lumières ---------- */
  scene.add(new THREE.HemisphereLight(0xBFE0F5, 0x6E5B44, 0.85));
  const sun = new THREE.DirectionalLight(0xFFD9A0, 1.15);
  sun.position.set(-180, 150, -140);
  sun.castShadow = true;
  sun.shadow.mapSize.set(1024, 1024);
  sun.shadow.camera.near = 20;
  sun.shadow.camera.far = 640;
  sun.shadow.camera.left = -200; sun.shadow.camera.right = 200;
  sun.shadow.camera.top = 200; sun.shadow.camera.bottom = -200;
  scene.add(sun);
  const bounce = new THREE.PointLight(0x9FD3F0, 0.5, 400);
  bounce.position.set(60, 20, 80);
  scene.add(bounce);

  /* ---------- mer animée ---------- */
  const seaGeo = new THREE.PlaneGeometry(2400, 2400, 90, 90);
  const sea = new THREE.Mesh(seaGeo, new THREE.MeshPhongMaterial({
    map: seaTex, color: 0x2E7BB5, shininess: 90, specular: 0xBFE6FF
  }));
  sea.rotation.x = -Math.PI / 2;
  sea.position.y = -46;
  sea.receiveShadow = false;
  scene.add(sea);
  const seaBase = seaGeo.attributes.position.array.slice();

  /* ---------- promontoire ---------- */
  const rockMat = new THREE.MeshLambertMaterial({ color: 0xB9A88C });
  const cliffGeo = new THREE.CylinderGeometry(120, 168, 92, 32, 6);
  const cp = cliffGeo.attributes.position;
  for (let i = 0; i < cp.count; i++) {
    const x = cp.getX(i), y = cp.getY(i), z = cp.getZ(i);
    const n = Math.sin(x * 0.06) * Math.cos(z * 0.05) * 5.5 + Math.sin(y * 0.14) * 3.2;
    cp.setXYZ(i, x + n, y, z + n);
  }
  cliffGeo.computeVertexNormals();
  const cliff = new THREE.Mesh(cliffGeo, rockMat);
  cliff.position.y = -50;
  cliff.receiveShadow = true;
  scene.add(cliff);

  const plateau = new THREE.Mesh(
    new THREE.CylinderGeometry(122, 122, 6, 32),
    new THREE.MeshLambertMaterial({ color: 0xD9CDB4 })
  );
  plateau.position.y = -3;
  plateau.receiveShadow = true;
  scene.add(plateau);

  /* ---------- maisons procédurales, en rendu instancié ----------
     Chaque type de pièce (mur, parapet, merlon, porte, fenêtre, linteau) forme un seul
     InstancedMesh : le village entier coûte une poignée d'appels de rendu au lieu de
     plusieurs centaines, ce qui le garde fluide sur un téléphone. */
  const wallMat = new THREE.MeshLambertMaterial({ map: whitewash, color: 0xFFFFFF });
  const blueMat = new THREE.MeshLambertMaterial({ color: 0x2E6FA8 });
  const doorMat = new THREE.MeshLambertMaterial({ map: doorTex });
  const goldMat = new THREE.MeshLambertMaterial({ color: 0xD4A017 });
  const stoneMat = new THREE.MeshLambertMaterial({ color: 0xD9CDB4 });

  function archGeo(width, height, depth) {
    // ouverture en plein cintre : forme dessinée puis extrudée
    const sh = new THREE.Shape();
    const w = width / 2, straight = height - w;
    sh.moveTo(-w, 0); sh.lineTo(-w, straight);
    sh.absarc(0, straight, w, Math.PI, 0, true);
    sh.lineTo(w, 0); sh.lineTo(-w, 0);
    return new THREE.ExtrudeGeometry(sh, { depth: depth, bevelEnabled: false, curveSegments: 14 });
  }

  const unitBox = new THREE.BoxGeometry(1, 1, 1);
  const doorGeo = archGeo(3.4, 5.6, 0.5);
  const bigDoorGeo = archGeo(13, 22, 1.4);
  const puffGeo = new THREE.IcosahedronGeometry(1.6, 0);

  const parentObj = new THREE.Object3D();
  const childObj = new THREE.Object3D();
  const tmpMat = new THREE.Matrix4();
  const IDENT = new THREE.Matrix4();

  function slot(list, px, py, pz, ry, sx, sy, sz, host) {
    childObj.position.set(px, py, pz);
    childObj.rotation.set(0, ry, 0);
    childObj.scale.set(sx, sy, sz);
    childObj.updateMatrix();
    list.push(tmpMat.multiplyMatrices(host, childObj.matrix).clone());
  }

  function instanced(geo, mat, mats, shadow) {
    const mesh = new THREE.InstancedMesh(geo, mat, mats.length);
    mats.forEach(function (m, i) { mesh.setMatrixAt(i, m); });
    mesh.instanceMatrix.needsUpdate = true;
    mesh.castShadow = !!shadow;
    mesh.receiveShadow = true;
    return mesh;
  }

  const M = { wall: [], parapet: [], merlon: [], door: [], window: [], lintel: [], step: [] };
  const rings = [
    { r: 44, n: 14, h: [13, 19], drop: 0 },
    { r: 70, n: 20, h: [10, 15], drop: 3 },
    { r: 96, n: 26, h: [8, 12], drop: 7 }
  ];
  let seed = 1;
  rings.forEach(function (ring, ri) {
    for (let i = 0; i < ring.n; i++) {
      const a = (i / ring.n) * Math.PI * 2 + ri * 0.21;
      const h = ring.h[0] + (((seed * 37) % 100) / 100) * (ring.h[1] - ring.h[0]);
      const w = 9 + (seed % 3) * 1.7, d = 9;

      parentObj.position.set(Math.cos(a) * ring.r, -ring.drop, Math.sin(a) * ring.r);
      parentObj.rotation.set(0, -a + Math.PI / 2, 0);
      parentObj.updateMatrix();
      const host = parentObj.matrix;

      slot(M.wall, 0, h / 2, 0, 0, w, h, d, host);
      slot(M.parapet, 0, h + 0.8, 0, 0, w + 0.6, 1.6, d + 0.6, host);
      for (let k = 0; k < 4; k++) {
        slot(M.merlon, -w / 2 + 0.8 + (k * (w - 1.6)) / 3, h + 2.2, d / 2 + 0.1, 0, 1.2, 1.5, 1.2, host);
      }
      slot(M.door, 0, 0.05, d / 2 + 0.02, 0, 1, 1, 1, host);
      slot(M.lintel, 0, 6.2, d / 2 + 0.25, 0, 4.6, 0.5, 0.8, host);
      slot(M.step, 0, 0.3, d / 2 + 1.4, 0, 5.2, 0.6, 2.6, host);
      const wins = h > 12 ? 3 : 2;
      for (let k = 0; k < wins; k++) {
        slot(M.window, -w / 2 + 2.4 + k * 2.9, 8.6 + (seed % 2) * 1.3, d / 2 + 0.08, 0, 2.2, 2.6, 0.4, host);
      }
      seed++;
    }
  });

  const village = new THREE.Group();
  village.add(
    instanced(unitBox, wallMat, M.wall, true),
    instanced(unitBox, wallMat, M.parapet, true),
    instanced(unitBox, wallMat, M.merlon, false),
    instanced(unitBox, stoneMat, M.step, false),
    instanced(doorGeo, doorMat, M.door, false),
    instanced(unitBox, goldMat, M.lintel, false),
    instanced(unitBox, blueMat, M.window, false)
  );
  scene.add(village);

  /* ---------- zaouïa : coupole, minaret, patio ---------- */
  const shrine = new THREE.Group();
  const base = new THREE.Mesh(new THREE.BoxGeometry(30, 14, 30), wallMat);
  base.position.y = 7; base.castShadow = true; base.receiveShadow = true;
  shrine.add(base);
  const dome = new THREE.Mesh(
    new THREE.SphereGeometry(13, 32, 20, 0, Math.PI * 2, 0, Math.PI / 2),
    new THREE.MeshLambertMaterial({ map: whitewash, color: 0xFFF6E2 })
  );
  dome.position.y = 14; dome.castShadow = true;
  shrine.add(dome);
  const drum = new THREE.Mesh(new THREE.CylinderGeometry(13.4, 13.4, 2.4, 32), goldMat);
  drum.position.y = 13.6;
  shrine.add(drum);
  const finial = new THREE.Mesh(new THREE.SphereGeometry(1.7, 16, 12), goldMat);
  finial.position.y = 28;
  shrine.add(finial);
  const spike = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 5, 8), goldMat);
  spike.position.y = 30.5;
  shrine.add(spike);
  const minaret = new THREE.Mesh(new THREE.BoxGeometry(7, 40, 7), wallMat);
  minaret.position.set(20, 20, -12); minaret.castShadow = true;
  shrine.add(minaret);
  const mcap = new THREE.Mesh(new THREE.SphereGeometry(4.6, 20, 14, 0, Math.PI * 2, 0, Math.PI / 2), goldMat);
  mcap.position.set(20, 40, -12);
  shrine.add(mcap);
  for (let i = 0; i < 3; i++) {
    const a = new THREE.Mesh(archGeo(4, 7, 1), blueMat);
    a.position.set(-9 + i * 9, 0.2, 15.2);
    shrine.add(a);
  }
  shrine.position.set(0, 0, 0);
  scene.add(shrine);

  /* ---------- végétation instanciée ---------- */
  const V = { trunk: [], crown: [], puff: [], palmTrunk: [], frond: [] };

  for (let i = 0; i < 26; i++) {
    const a = (i / 26) * Math.PI * 2 + 0.3, r = 52 + ((i * 17) % 58);
    const sc = 0.75 + ((i * 13) % 50) / 100;
    const x = Math.cos(a) * r, z = Math.sin(a) * r;
    slot(V.trunk, x, 2 * sc, z, 0, 0.6 * sc, 4 * sc, 0.6 * sc, IDENT);
    slot(V.crown, x, 11 * sc, z, 0, sc, sc, sc, IDENT);
  }
  for (let i = 0; i < 34; i++) {
    const a = (i / 34) * Math.PI * 2 + 1.1, r = 40 + ((i * 23) % 64);
    const bx = Math.cos(a) * r, bz = Math.sin(a) * r, by = 5 + ((i * 31) % 90) / 10;
    for (let k = 0; k < 6; k++) {
      const s3 = 0.9 + ((i + k * 7) % 8) / 10;
      slot(V.puff, bx + ((k * 13) % 7) - 3, by + ((k * 19) % 5) - 2, bz + ((k * 11) % 6) - 3, 0, s3, s3, s3, IDENT);
    }
  }
  [[-62, 44], [68, -36], [20, 84]].forEach(function (p) {
    slot(V.palmTrunk, p[0], 8, p[1], 0, 1, 1, 1, IDENT);
    for (let k = 0; k < 7; k++) {
      childObj.position.set(p[0], 16, p[1]);
      childObj.rotation.set(0, (k / 7) * Math.PI * 2, Math.PI / 2.4);
      childObj.scale.set(1, 1, 1);
      childObj.updateMatrix();
      V.frond.push(childObj.matrix.clone());
    }
  });

  const frondGeo = new THREE.ConeGeometry(1.6, 11, 4, 1, true);
  frondGeo.translate(0, -4.5, 0);

  village.add(
    instanced(new THREE.CylinderGeometry(0.5, 0.7, 1, 6), new THREE.MeshLambertMaterial({ color: 0x6B5238 }), V.trunk, false),
    instanced(new THREE.ConeGeometry(2.6, 15, 9), new THREE.MeshLambertMaterial({ color: 0x2F5540 }), V.crown, true),
    instanced(puffGeo, new THREE.MeshLambertMaterial({ color: 0xC4327A }), V.puff, false),
    instanced(new THREE.CylinderGeometry(0.7, 1.1, 16, 8), new THREE.MeshLambertMaterial({ color: 0x8A7350 }), V.palmTrunk, true),
    instanced(frondGeo, new THREE.MeshLambertMaterial({ color: 0x3E7A4C, side: THREE.DoubleSide }), V.frond, false)
  );

  function bougainCluster(x, y, z) {
    // buisson isolé, réservé au gros plan de la scène « portes »
    const mats = [];
    for (let i = 0; i < 10; i++) {
      slot(mats, (i % 4) - 2, ((i * 7) % 6) - 3, ((i * 5) % 4) - 2, 0, 1.1, 1.1, 1.1, IDENT);
    }
    const g = new THREE.Group();
    g.add(instanced(puffGeo, new THREE.MeshLambertMaterial({ color: 0xC4327A }), mats, false));
    g.position.set(x, y, z);
    return g;
  }

  /* ---------- صحن النجمة الزهراء : arcades sur deux niveaux, zellige, fontaine ----------
     Le patio est construit côté par côté : une rotation d'un quart de tour par face,
     et toutes les pièces d'une face sont posées dans le repère de cette rotation. */
  const palace = new THREE.Group();

  const marbleMat = new THREE.MeshLambertMaterial({ map: zelligeTex });
  const plasterMat = new THREE.MeshLambertMaterial({ map: whitewash, color: 0xFFF6E8 });
  const woodMat = new THREE.MeshLambertMaterial({ color: 0x6B4A2B });

  const floor = new THREE.Mesh(new THREE.BoxGeometry(70, 1, 70), marbleMat);
  floor.position.y = 0.5; floor.receiveShadow = true;
  palace.add(floor);

  const P = { base: [], shaft: [], capital: [], dado: [], wall: [], spandrel: [],
              beam: [], lantern: [], chain: [], rail: [], orange: [] };

  const SIDE = 26;      // ligne d'arcade
  const BACK = 34;      // mur du fond de la galerie
  const colX = [-26, -13, 0, 13, 26];
  const archX = [-19.5, -6.5, 6.5, 19.5];

  for (let s = 0; s < 4; s++) {
    parentObj.position.set(0, 0, 0);
    parentObj.rotation.set(0, (s * Math.PI) / 2, 0);
    parentObj.updateMatrix();
    const host = parentObj.matrix;

    colX.forEach(function (x) {
      slot(P.base, x, 0.9, SIDE, 0, 3, 1.8, 3, host);
      slot(P.shaft, x, 8.6, SIDE, 0, 1, 1, 1, host);
      slot(P.capital, x, 16.3, SIDE, 0, 3.4, 2.4, 3.4, host);
    });

    // mur du fond + soubassement de zellige + galerie couverte
    slot(P.wall, 0, 13, BACK, 0, 70, 26, 1.6, host);
    slot(P.dado, 0, 4, BACK - 0.9, 0, 70, 8, 0.5, host);
    slot(P.spandrel, 0, 19.6, SIDE, 0, 70, 4.4, 1.6, host);

    // poutres du plafond de galerie, entre l'arcade et le mur
    for (let b = -4; b <= 4; b++) {
      slot(P.beam, b * 7, 17.6, (SIDE + BACK) / 2, Math.PI / 2, 8.6, 0.9, 0.9, host);
    }

    // garde-corps du niveau haut
    slot(P.rail, 0, 22.8, SIDE, 0, 70, 1.8, 1.2, host);

    // lanternes suspendues sous chaque arc
    archX.forEach(function (x) {
      slot(P.chain, x, 16.4, SIDE + 2.4, 0, 0.16, 4.4, 0.16, host);
      slot(P.lantern, x, 13.2, SIDE + 2.4, 0, 1, 1, 1, host);
    });
  }

  palace.add(
    instanced(unitBox, plasterMat, P.base, true),
    instanced(new THREE.CylinderGeometry(1.05, 1.25, 13.6, 14), plasterMat, P.shaft, true),
    instanced(unitBox, goldMat, P.capital, false),
    instanced(unitBox, marbleMat, P.dado, false),
    instanced(unitBox, plasterMat, P.wall, true),
    instanced(unitBox, plasterMat, P.spandrel, true),
    instanced(unitBox, woodMat, P.beam, false),
    instanced(unitBox, goldMat, P.rail, false),
    instanced(new THREE.CylinderGeometry(0.08, 0.08, 1, 6), goldMat, P.chain, false),
    instanced(new THREE.OctahedronGeometry(1.5), new THREE.MeshBasicMaterial({ color: 0xFFD98A }), P.lantern, false)
  );

  // arcades : un maillage par arc, la géométrie extrudée n'a que quelques centaines de faces
  const galleryArch = archGeo(12, 16.5, 1.4);
  for (let s = 0; s < 4; s++) {
    archX.forEach(function (x) {
      const a = new THREE.Mesh(galleryArch, plasterMat);
      a.position.set(x, 1, SIDE).applyAxisAngle(new THREE.Vector3(0, 1, 0), (s * Math.PI) / 2);
      a.rotation.y = (s * Math.PI) / 2;
      a.castShadow = true;
      palace.add(a);
    });
  }

  /* fontaine octogonale */
  const basin = new THREE.Mesh(new THREE.CylinderGeometry(9, 9.8, 2.6, 8), marbleMat);
  basin.position.y = 1.8; basin.castShadow = true; basin.receiveShadow = true;
  const rim = new THREE.Mesh(new THREE.CylinderGeometry(9.3, 9.3, 0.6, 8), plasterMat);
  rim.position.y = 3.1;
  const water = new THREE.Mesh(new THREE.CircleGeometry(8.4, 8),
    new THREE.MeshPhongMaterial({ color: 0x2E7BB5, shininess: 140, specular: 0xFFFFFF,
                                  transparent: true, opacity: 0.86 }));
  water.rotation.x = -Math.PI / 2; water.position.y = 3.0;
  const stem = new THREE.Mesh(new THREE.CylinderGeometry(0.7, 1.3, 5.5, 10), marbleMat);
  stem.position.y = 5.4;
  const bowl = new THREE.Mesh(new THREE.CylinderGeometry(3.2, 1.4, 1.4, 12), plasterMat);
  bowl.position.y = 8.4;
  const jetMat = new THREE.MeshBasicMaterial({ color: 0xCFEAFB, transparent: true, opacity: 0.7 });
  const jets = [];
  for (let i = 0; i < 6; i++) {
    const j = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.05, 5, 6), jetMat);
    const a = (i / 6) * Math.PI * 2;
    j.position.set(Math.cos(a) * 2.6, 10.6, Math.sin(a) * 2.6);
    j.rotation.z = Math.cos(a) * 0.28;
    j.rotation.x = -Math.sin(a) * 0.28;
    jets.push(j);
  }
  const ripples = [];
  for (let i = 0; i < 3; i++) {
    const r = new THREE.Mesh(new THREE.RingGeometry(1, 1.5, 24),
      new THREE.MeshBasicMaterial({ color: 0xEAF6FF, transparent: true, opacity: 0.5, side: THREE.DoubleSide }));
    r.rotation.x = -Math.PI / 2; r.position.y = 3.06;
    r.userData.t = i / 3;
    ripples.push(r);
  }
  palace.add(basin, rim, water, stem, bowl);
  jets.forEach(function (j) { palace.add(j); });
  ripples.forEach(function (r) { palace.add(r); });

  /* orangers des quatre coins */
  const trunkM = [], crownM = [], fruitM = [];
  [[-19, -19], [19, -19], [-19, 19], [19, 19]].forEach(function (c, ci) {
    slot(trunkM, c[0], 3, c[1], 0, 1, 1, 1, IDENT);
    slot(crownM, c[0], 8.4, c[1], 0, 1, 1, 1, IDENT);
    for (let k = 0; k < 7; k++) {
      const a = ((k + ci) / 7) * Math.PI * 2;
      slot(fruitM, c[0] + Math.cos(a) * 3.4, 7.4 + ((k * 13) % 30) / 10, c[1] + Math.sin(a) * 3.4,
           0, 0.5, 0.5, 0.5, IDENT);
    }
  });
  palace.add(
    instanced(new THREE.CylinderGeometry(0.6, 0.9, 6, 8), woodMat, trunkM, true),
    instanced(new THREE.IcosahedronGeometry(4.6, 1), new THREE.MeshLambertMaterial({ color: 0x2F6B43 }), crownM, true),
    instanced(new THREE.IcosahedronGeometry(1, 0), new THREE.MeshLambertMaterial({ color: 0xE08A1E }), fruitM, false)
  );

  // lumière propre au patio : un ciel ouvert au-dessus de la cour
  const patioLight = new THREE.PointLight(0xFFE9C4, 0.9, 180);
  patioLight.position.set(0, 34, 0);
  palace.add(patioLight);

  /* ---------- surfaces d'affichage des médias de l'utilisateur ----------
     Trois surfaces reçoivent une image animée ou une vidéo : deux cadres accrochés
     dans la galerie du palais, un grand écran sur la place du programme. */
  const screenMat = function () {
    return new THREE.MeshBasicMaterial({ color: 0x11202E });
  };

  function mediaFrame(w, h, x, y, z, ry) {
    const g = new THREE.Group();
    const border = new THREE.Mesh(new THREE.BoxGeometry(w + 1.6, h + 1.6, 0.6), goldMat);
    const surface = new THREE.Mesh(new THREE.PlaneGeometry(w, h), screenMat());
    surface.position.z = 0.42;
    g.add(border, surface);
    g.position.set(x, y, z);
    g.rotation.y = ry;
    g.userData.surface = surface;
    return g;
  }

  const palaceFrames = [
    mediaFrame(16, 10, -0.4, 13, -32.4, 0),
    mediaFrame(16, 10, -32.4, 13, -0.4, Math.PI / 2)
  ];
  palaceFrames.forEach(function (f) { palace.add(f); });

  palace.position.set(0, 0, -260);
  palace.visible = false;
  scene.add(palace);

  /* ---------- scène « programme » : bannières et lanternes ---------- */
  const eventGroup = new THREE.Group();
  for (let i = 0; i < 8; i++) {
    const a = (i / 8) * Math.PI * 2;
    const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.3, 12, 6), goldMat);
    pole.position.set(Math.cos(a) * 30, 6, Math.sin(a) * 30);
    const flag = new THREE.Mesh(new THREE.PlaneGeometry(7, 4),
      new THREE.MeshLambertMaterial({ color: i % 2 ? 0x2E6FA8 : 0xD4A017, side: THREE.DoubleSide }));
    flag.position.set(Math.cos(a) * 33.5, 10, Math.sin(a) * 33.5);
    flag.rotation.y = -a;
    eventGroup.add(pole, flag);
  }
  const lanterns = [];
  for (let i = 0; i < 26; i++) {
    const l = new THREE.Mesh(new THREE.OctahedronGeometry(1.2),
      new THREE.MeshBasicMaterial({ color: 0xFFD98A }));
    l.position.set((Math.random() - 0.5) * 120, 16 + Math.random() * 26, (Math.random() - 0.5) * 120);
    l.userData.phase = Math.random() * Math.PI * 2;
    lanterns.push(l);
    eventGroup.add(l);
  }
  const eventScreen = mediaFrame(46, 26, 0, 22, -52, 0);
  eventGroup.add(eventScreen);
  const stand = new THREE.Mesh(new THREE.BoxGeometry(4, 20, 4), goldMat);
  stand.position.set(0, 10, -52);
  eventGroup.add(stand);

  eventGroup.visible = false;
  scene.add(eventGroup);

  /* ---------- porte en gros plan (scène 2) ---------- */
  const doorSet = new THREE.Group();
  const facade = new THREE.Mesh(new THREE.BoxGeometry(46, 40, 4), wallMat);
  facade.position.set(0, 20, 0); facade.castShadow = true; facade.receiveShadow = true;
  const bigDoor = new THREE.Mesh(bigDoorGeo, doorMat);
  bigDoor.position.set(0, 0.4, 2.1);
  const lintel = new THREE.Mesh(new THREE.BoxGeometry(17, 1.6, 2.4), goldMat);
  lintel.position.set(0, 23.6, 2.6);
  const step = new THREE.Mesh(new THREE.BoxGeometry(20, 1.2, 6), new THREE.MeshLambertMaterial({ color: 0xD9CDB4 }));
  step.position.set(0, 0.4, 4.6);
  doorSet.add(facade, bigDoor, lintel, step);
  doorSet.add(bougainCluster(-19, 26, 3), bougainCluster(21, 22, 3));
  doorSet.position.set(0, 0, 150);
  doorSet.visible = false;
  scene.add(doorSet);

  /* ---------- oiseaux ---------- */
  const birds = new THREE.Group();
  const birdMat = new THREE.MeshBasicMaterial({ color: 0x27384A, side: THREE.DoubleSide });
  for (let i = 0; i < 14; i++) {
    const shape = new THREE.Shape();
    shape.moveTo(-2, 0); shape.quadraticCurveTo(0, 1.4, 2, 0);
    shape.quadraticCurveTo(0, 0.4, -2, 0);
    const b = new THREE.Mesh(new THREE.ShapeGeometry(shape), birdMat);
    b.userData.a = Math.random() * Math.PI * 2;
    b.userData.r = 120 + Math.random() * 90;
    b.userData.y = 55 + Math.random() * 45;
    b.userData.sp = 0.0018 + Math.random() * 0.0022;
    birds.add(b);
  }
  scene.add(birds);

  /* ---------- caméra : plans cinématiques par scène ---------- */
  const SHOTS = [
    { pos: [190, 96, 190], look: [0, 12, 0], fov: 40, sun: 0xFFD9A0, exposure: 1.0 },   // panorama
    { pos: [0, 20, 196], look: [0, 16, 150], fov: 34, sun: 0xFFE7C2, exposure: 1.0 },   // porte en gros plan
    { pos: [46, 26, 62], look: [0, 18, 0], fov: 38, sun: 0xFFCB8A, exposure: 1.0 },     // zaouïa
    { pos: [17, 13, -239], look: [0, 5, -262], fov: 58, sun: 0xFFF0D2, exposure: 1.0 }, // patio, vue depuis la cour
    { pos: [120, 62, 130], look: [0, 14, 0], fov: 46, sun: 0xFFE0B0, exposure: 1.0 }    // programme
  ];

  const cur = {
    pos: new THREE.Vector3(320, 180, 320),
    look: new THREE.Vector3(0, 10, 0),
    fov: 46
  };
  const tgt = {
    pos: new THREE.Vector3().fromArray(SHOTS[0].pos),
    look: new THREE.Vector3().fromArray(SHOTS[0].look),
    fov: SHOTS[0].fov
  };
  let tiltY = 0, tiltX = 0, orbit = 0, current = 0;

  function focus(i) {
    current = i % SHOTS.length;
    const s = SHOTS[current];
    tgt.pos.fromArray(s.pos);
    tgt.look.fromArray(s.look);
    tgt.fov = s.fov;
    sun.color.setHex(s.sun);
    doorSet.visible = current === 1;
    palace.visible = current === 3;
    eventGroup.visible = current === 4;
    const wide = current !== 1 && current !== 3;
    shrine.visible = wide;
    village.visible = wide;
  }

  function tilt(y, x) { tiltY = y; tiltX = x; }

  /* ---------- médias de l'utilisateur : image, image animée, vidéo ----------
     Une image animée (WebP/GIF) ne s'anime pas seule dans une texture : on la
     redessine dans un <canvas> à chaque image, ce qui la fait vivre à l'écran.
     Pour la vidéo, la lecture est déclenchée par le geste de l'utilisateur —
     l'autoplay muet est bloqué dans beaucoup d'environnements. */
  const animatedSources = [];

  function disposeSurface(surface) {
    if (surface.material.map) surface.material.map.dispose();
  }

  function applyTexture(surface, texture) {
    disposeSurface(surface);
    surface.material = new THREE.MeshBasicMaterial({ map: texture });
    surface.material.needsUpdate = true;
  }

  function targetSurfaces(sceneIndex) {
    if (sceneIndex === 3) return palaceFrames.map(function (f) { return f.userData.surface; });
    if (sceneIndex === 4) return [eventScreen.userData.surface];
    return [eventScreen.userData.surface].concat(palaceFrames.map(function (f) { return f.userData.surface; }));
  }

  function loadMedia(file, sceneIndex, onState) {
    const url = URL.createObjectURL(file);
    const surfaces = targetSurfaces(sceneIndex);
    const isVideo = /^video\//.test(file.type);

    if (isVideo) {
      const v = document.createElement("video");
      v.src = url; v.loop = true; v.muted = true; v.playsInline = true;
      v.setAttribute("playsinline", ""); v.setAttribute("muted", "");
      v.oncanplay = function () {
        const tex = new THREE.VideoTexture(v);
        tex.minFilter = THREE.LinearFilter;
        surfaces.forEach(function (s2) { applyTexture(s2, tex); });
        const played = v.play();
        if (played && played.catch) {
          played.catch(function () {
            onState("blocked");
            const resume = function () { v.play(); removeEventListener("pointerdown", resume); };
            addEventListener("pointerdown", resume, { passive: true });
          });
        }
        onState("ok");
      };
      v.onerror = function () { onState("error"); };
      return;
    }

    const img = new Image();
    img.onload = function () {
      const c = document.createElement("canvas");
      c.width = img.naturalWidth; c.height = img.naturalHeight;
      const g2 = c.getContext("2d");
      g2.drawImage(img, 0, 0);
      const tex = new THREE.CanvasTexture(c);
      tex.minFilter = THREE.LinearFilter;
      surfaces.forEach(function (s2) { applyTexture(s2, tex); });
      // WebP/GIF animés : on rafraîchit le canvas depuis l'<img> qui, lui, joue tout seul
      if (/webp|gif/i.test(file.type) || /\.(webp|gif)$/i.test(file.name)) {
        animatedSources.push({ img: img, ctx: g2, tex: tex, w: c.width, h: c.height });
      }
      onState("ok");
    };
    img.onerror = function () { onState("error"); };
    img.src = url;
  }

  const clock = new THREE.Clock();
  let raf = 0;

  function frame() {
    const dt = clock.getDelta();
    const el = clock.elapsedTime;

    // houle
    const arr = seaGeo.attributes.position.array;
    for (let i = 0; i < arr.length; i += 3) {
      const x = seaBase[i], y = seaBase[i + 1];
      arr[i + 2] = Math.sin((x + el * 26) * 0.018) * 1.5 + Math.cos((y + el * 18) * 0.023) * 1.2;
    }
    seaGeo.attributes.position.needsUpdate = true;
    seaTex.offset.x = el * 0.006;

    // oiseaux
    birds.children.forEach((b) => {
      b.userData.a += b.userData.sp;
      b.position.set(Math.cos(b.userData.a) * b.userData.r, b.userData.y + Math.sin(el + b.userData.a) * 3,
                     Math.sin(b.userData.a) * b.userData.r);
      b.rotation.set(Math.PI / 2.6, 0, -b.userData.a);
      b.scale.y = 0.7 + Math.sin(el * 6 + b.userData.a) * 0.3;
    });

    // fontaine : eau, jets et ondes concentriques
    if (palace.visible) {
      water.material.opacity = 0.78 + Math.sin(el * 1.6) * 0.08;
      jets.forEach(function (j, i) {
        j.scale.y = 0.85 + Math.sin(el * 3.4 + i) * 0.15;
      });
      ripples.forEach(function (r) {
        r.userData.t = (r.userData.t + dt * 0.35) % 1;
        const k = 0.6 + r.userData.t * 7.4;
        r.scale.set(k, k, 1);
        r.material.opacity = 0.45 * (1 - r.userData.t);
      });
    }

    // images animées : on repousse la frame courante dans la texture
    for (let i = 0; i < animatedSources.length; i++) {
      const a = animatedSources[i];
      a.ctx.drawImage(a.img, 0, 0, a.w, a.h);
      a.tex.needsUpdate = true;
    }

    // lanternes
    lanterns.forEach((l) => {
      l.position.y += Math.sin(el * 1.2 + l.userData.phase) * 0.02;
      l.rotation.y += 0.01;
    });

    // orbite lente + inclinaison au pointeur
    orbit += dt * 0.045;
    const swing = (current === 1 || current === 3) ? 4 : 16;
    const px = tgt.pos.x + Math.cos(orbit) * swing + tiltY * 2.2;
    const pz = tgt.pos.z + Math.sin(orbit) * swing;
    const py = tgt.pos.y + tiltX * 1.6;

    cur.pos.lerp(new THREE.Vector3(px, py, pz), 0.028);
    cur.look.lerp(tgt.look, 0.05);
    cur.fov += (tgt.fov - cur.fov) * 0.05;

    camera.position.copy(cur.pos);
    camera.lookAt(cur.look);
    camera.fov = cur.fov;
    camera.updateProjectionMatrix();

    renderer.render(scene, camera);
    raf = requestAnimationFrame(frame);
  }
  frame();

  addEventListener("resize", () => {
    renderer.setSize(innerWidth, innerHeight);
    camera.aspect = innerWidth / innerHeight;
    camera.updateProjectionMatrix();
  }, { passive: true });

  focus(0);

  return {
    focus: focus,
    tilt: tilt,
    loadMedia: loadMedia,
    stop: function () { cancelAnimationFrame(raf); }
  };
};
