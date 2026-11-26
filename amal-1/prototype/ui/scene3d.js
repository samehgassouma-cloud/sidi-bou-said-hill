/* العرض ثلاثي الأبعاد (Three.js r128) · vue 3D · 3D view — généré/lu par prototype/build_landslide.py · لا تُعدّل الصفحة المبنية مباشرة */
const V={ok:null,loading:false,r:null,scene:null,cam:null,world:null,th:-0.55,ph:1.12,rad:100,tgt:null,drag:null,
  mode:"idle",t:0,zw:0,F:null,seq:null,rain:null,sea:null,pivot:null,wline:null,wfill:null,dust:null,built:null,last:0,status:"stIdle"};
const COL=[0xC9A06A,0x9C7A55,0x6E5A48];
function has3D(){try{const c=document.createElement("canvas");return !!(window.WebGLRenderingContext&&(c.getContext("webgl")||c.getContext("experimental-webgl")));}catch(e){return false}}
function load3D(cb){
  if(window.THREE)return cb(true);
  let done=false;const fin=v=>{if(!done){done=true;cb(v)}};
  const s=document.createElement("script");s.src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js";
  s.onload=()=>fin(!!window.THREE);s.onerror=()=>fin(false);document.head.appendChild(s);setTimeout(()=>fin(!!window.THREE),9000);
}
function fallback3D(){V.no=true;$("v3").hidden=true;$("s3d").hidden=true;$("cv").hidden=false;$("cv2").hidden=false;
  ["tgl"].forEach(i=>$(i).hidden=true);document.querySelector(".insp").hidden=true;$("storm").disabled=true;$("reset3").disabled=true;
  $("h3s").textContent=T[lang].no3d;if(last)show(last);}
function open3D(){
  const go=()=>{ if(V.no)return; if(!has3D())return fallback3D();
    if(V.ok){if(V.built!==last){build3D(last);buildSens(last);}return;}
    if(V.loading)return;V.loading=true;
    load3D(ok=>{V.loading=false;if(!ok)return fallback3D();try{init3D();initSens();build3D(last);buildSens(last);}catch(e){console.error(e);fallback3D();}});
  };
  if(last)go();else run(go);
}
function init3D(){
  const box=$("v3");
  V.r=new THREE.WebGLRenderer({antialias:true});V.r.setPixelRatio(Math.min(2,devicePixelRatio||1));
  box.prepend(V.r.domElement);V.r.domElement.style.touchAction="none";
  V.scene=new THREE.Scene();V.scene.background=new THREE.Color(0xBFDDF2);
  V.cam=new THREE.PerspectiveCamera(42,1,0.5,3000);
  V.scene.add(new THREE.HemisphereLight(0xEAF4FF,0x6E5A48,0.75));
  const sun=new THREE.DirectionalLight(0xFFF3DA,0.85);sun.position.set(-60,120,90);V.scene.add(sun);
  const el=V.r.domElement;
  el.addEventListener("pointerdown",e=>{V.drag={x:e.clientX,y:e.clientY,th:V.th,ph:V.ph};el.setPointerCapture(e.pointerId);},{passive:true});
  el.addEventListener("pointermove",e=>{if(!V.drag)return;V.th=V.drag.th-(e.clientX-V.drag.x)*0.006;
    V.ph=Math.min(1.45,Math.max(0.35,V.drag.ph-(e.clientY-V.drag.y)*0.005));V.idleT=0;},{passive:true});
  const up=()=>{V.drag=null};el.addEventListener("pointerup",up,{passive:true});el.addEventListener("pointercancel",up,{passive:true});
  $("zin").onclick=()=>V.rad=Math.max(V.rad0*0.45,V.rad*0.85);
  $("zout").onclick=()=>V.rad=Math.min(V.rad0*2,V.rad/0.85);
  new ResizeObserver(size3D).observe(box);size3D();
  V.ok=true;V.last=performance.now();requestAnimationFrame(loop3D);
}
function size3D(){if(!V.r)return;const w=$("v3").clientWidth,h=Math.round(w*(w<700?1.05:0.56));
  V.r.setSize(w,h);V.cam.aspect=w/h;V.cam.updateProjectionMatrix();}
function disposeTree(o){o.traverse(n=>{n.geometry&&n.geometry.dispose();if(n.material)[].concat(n.material).forEach(m=>m.dispose());});}
function rng(seed){return()=>{seed=(seed*16807)%2147483647;return seed/2147483647;};}
function makeHouse(w,h,dome,rand){
  const g=new THREE.Group(),white=new THREE.MeshLambertMaterial({color:0xFBFCFD}),blue=new THREE.MeshLambertMaterial({color:0x1F5FA8});
  const b=new THREE.Mesh(new THREE.BoxGeometry(w,h,w*0.9),white);b.position.y=h/2;g.add(b);
  const d=new THREE.Mesh(new THREE.BoxGeometry(0.15,2.1,1.1),blue);d.position.set(-w/2-0.05,1.05,0);g.add(d);
  for(const zz of [-w*0.28,w*0.28])if(h>3.5){const wi=new THREE.Mesh(new THREE.BoxGeometry(0.15,0.8,0.7),blue);wi.position.set(-w/2-0.05,h-1.3,zz);g.add(wi);}
  if(dome){const s=new THREE.Mesh(new THREE.SphereGeometry(w*0.3,14,8,0,Math.PI*2,0,Math.PI/2),white);s.position.y=h;g.add(s);}
  g.rotation.y=(rand()-0.5)*0.12;return g;
}
function shapeFrom(pts){const s=new THREE.Shape();pts.forEach((p,i)=>i?s.lineTo(p[0],p[1]):s.moveTo(p[0],p[1]));return s;}
function extrude(pts,z0,depth,color,parent,off){
  const geo=new THREE.ExtrudeGeometry(shapeFrom(pts),{depth,bevelEnabled:false});
  const m=new THREE.Mesh(geo,new THREE.MeshLambertMaterial({color}));m.position.set(off?off[0]:0,off?off[1]:0,z0);parent.add(m);return m;
}
function build3D(o,circle){
  const m=o.m,C=circle||(o.st.best);V.o=o;V.built=o;V.model=m;V.circle=C;V.mode="idle";V.seq=null;V.status="stIdle";
  if(V.world){V.scene.remove(V.world);disposeTree(V.world);}
  const W=new THREE.Group();V.world=W;V.scene.add(W);
  const G={};["grid","slices","water","houses","labels"].forEach(k=>{G[k]=new THREE.Group();});V.G=G;
  const x0=-0.6*m.H,x1=m.xcr+1.6*m.H,L=x1-x0,D=Math.max(30,L*0.75);
  V.D=D;V.x0=x0;V.x1=x1;
  const arc=C?x=>{const q=C.R*C.R-(x-C.xc)**2;return q>0?C.yc-Math.sqrt(q):Infinity}:()=>Infinity;
  const xs=[];for(let i=0;i<=180;i++)xs.push(x0+L*i/180);
  [0,m.xcr,...m.layers.map(Ly=>Ly.bot/m.tb-1e-4)].concat(C?[C.xl,C.xr]:[]).forEach(v=>{if(v>x0&&v<x1)xs.push(v)});xs.sort((a,b)=>a-b);
  const slipW=C?Math.min(D*0.5,Math.max(8,(C.xr-C.xl)*0.9)):0,zf=D/2-slipW;
  const layersFor=(top,z0,dep)=>{let prev=Infinity;m.layers.forEach((Ly,i)=>{
      const tp=x=>Math.min(top(x),prev);let run=[];
      const flush=()=>{if(run.length>1){const pts=run.concat([[run[run.length-1][0],Ly.bot],[run[0][0],Ly.bot]]);extrude(pts,z0,dep,COL[i],W);}run=[];};
      xs.forEach(x=>{const y=tp(x);if(y>Ly.bot+1e-3)run.push([x,y]);else flush();});flush();
      prev=Ly.bot;});};
  const cutTop=x=>(C&&x>C.xl&&x<C.xr)?Math.min(m.surf(x),arc(x)):m.surf(x);
  layersFor(m.surf,-D/2,zf+D/2);
  if(C)layersFor(cutTop,zf,slipW);
  // bedrock base slab
  extrude([[x0,m.zBed],[x1,m.zBed],[x1,m.zBed-3],[x0,m.zBed-3]],-D/2,D,0x4E3F33,W);
  // sliding mass on a pivot at the circle centre
  V.pivot=null;
  if(C){
    const pv=new THREE.Group();pv.position.set(C.xc,C.yc,0);W.add(pv);V.pivot=pv;
    const top=xs.filter(x=>x>=C.xl&&x<=C.xr).map(x=>[x,m.surf(x)]);
    const bot=[];for(let i=40;i>=0;i--){const x=C.xl+(C.xr-C.xl)*i/40;bot.push([x,Math.min(arc(x),m.surf(x))]);}
    const pts=[[C.xl,m.surf(C.xl)],...top,[C.xr,m.surf(C.xr)],...bot];
    extrude(pts.map(p=>[p[0]-C.xc,p[1]-C.yc]),zf,slipW,0xD2A86F,pv);
    // slip surface tube on the front face
    const cp=[];for(let i=0;i<=48;i++){const x=C.xl+(C.xr-C.xl)*i/48;cp.push(new THREE.Vector3(x,Math.min(arc(x),m.surf(x)),D/2+0.12));}
    W.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(cp),96,Math.max(0.18,m.H*0.008),6,false),new THREE.MeshBasicMaterial({color:0xA8285F})));
    const ctr=new THREE.Mesh(new THREE.SphereGeometry(Math.max(0.5,m.H*0.018),12,10),new THREE.MeshBasicMaterial({color:0xA8285F}));ctr.position.set(C.xc,C.yc,D/2);W.add(ctr);
    const lg=new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(C.xl,m.surf(C.xl),D/2+0.1),new THREE.Vector3(C.xc,C.yc,D/2),new THREE.Vector3(C.xr,m.surf(C.xr),D/2+0.1)]);
    const ln=new THREE.Line(lg,new THREE.LineDashedMaterial({color:0xA8285F,dashSize:1.2,gapSize:0.8}));ln.computeLineDistances();W.add(ln);
  }
  // houses
  W.add(G.houses);
  if(V.pivot){V.hp=new THREE.Group();V.hp.name="hp";V.pivot.add(V.hp);}
  const rand=rng(7);
  if(m.q>0&&m.qB>0){
    const step=6.5,dens=Math.min(1,0.35+m.q/100);
    for(let x=m.xcr+m.qd+2.5;x<=m.xcr+m.qd+m.qB-1;x+=step)
      for(let z=-D/2+4;z<=D/2-3;z+=step){
        if(rand()>dens)continue;
        const w=3.6+rand()*1.6,h=3.5+rand()*4,hs=makeHouse(w,h,rand()<0.3,rand);
        const onMass=C&&z>zf+w/2&&z<D/2-w/2&&x-w/2>C.xl&&x+w/2<C.xr;
        if(onMass){hs.position.set(x-C.xc,m.H-C.yc,z);V.hp.add(hs);}else{hs.position.set(x,m.H,z);G.houses.add(hs);}
      }
  }
  // lighthouse-like minaret landmark at the back of the plateau
  const mn=new THREE.Mesh(new THREE.CylinderGeometry(1,1.3,12,12),new THREE.MeshLambertMaterial({color:0xFBFCFD}));
  mn.position.set(Math.min(x1-3,m.xcr+m.qd+m.qB+8),m.H+6,-D/2+6);W.add(mn);
  // trial centres (instanced)
  const grid=circle?[]:o.st.grid;
  if(grid.length){
    const im=new THREE.InstancedMesh(new THREE.SphereGeometry(Math.max(0.3,m.H*0.011),8,6),new THREE.MeshBasicMaterial(),grid.length);
    const mt=new THREE.Matrix4(),col=new THREE.Color();
    grid.forEach((g,i)=>{mt.makeTranslation(g.xc,g.yc,D/2);im.setMatrixAt(i,mt);
      col.set(g.F<1?0xA8285F:g.F<1.5?0xD09A1E:0x3F7A3A);im.setColorAt(i,col);});
    im.instanceMatrix.needsUpdate=true;if(im.instanceColor)im.instanceColor.needsUpdate=true;G.grid.add(im);
  }
  W.add(G.grid);
  // slices (move with the mass)
  if(C&&C.S&&V.pivot){
    const pts=[];C.S.forEach((sl,i)=>{if(i===0)return;const x=sl.xm-C.bw/2;
      const yb=C.yc-Math.sqrt(Math.max(0,C.R*C.R-(x-C.xc)**2));pts.push(x-C.xc,yb-C.yc,D/2+0.15-0,x-C.xc,m.surf(x)-C.yc,D/2+0.15);});
    const lg=new THREE.BufferGeometry();lg.setAttribute("position",new THREE.Float32BufferAttribute(pts,3));
    G.slices.add(new THREE.LineSegments(lg,new THREE.LineBasicMaterial({color:0x5A3A20})));
    V.pivot.add(G.slices);V.sel=new THREE.Group();G.slices.add(V.sel);
  }
  W.add(G.labels);
  // sea
  const sx0=x0-80,sw=-sx0+2;
  const sg=new THREE.PlaneGeometry(sw,D+160,60,40);sg.rotateX(-Math.PI/2);
  const sea=new THREE.Mesh(sg,new THREE.MeshLambertMaterial({color:0x1C5A86,transparent:true,opacity:0.9}));
  sea.position.set(sx0+sw/2,0.9,0);W.add(sea);V.sea=sea;V.seaBase=Float32Array.from(sg.attributes.position.array);
  // water table ribbon + translucent fill on the front face
  V.wline=new THREE.Mesh(new THREE.BufferGeometry(),new THREE.MeshBasicMaterial({color:0x2E7BD0,side:THREE.DoubleSide}));
  V.wfill=new THREE.Mesh(new THREE.BufferGeometry(),new THREE.MeshBasicMaterial({color:0x2E7BD0,transparent:true,opacity:0.28,side:THREE.DoubleSide,depthWrite:false}));
  V.wline.position.z=D/2+0.08;V.wfill.position.z=D/2+0.05;G.water.add(V.wline,V.wfill);W.add(G.water);
  V.xsW=xs;V.zw=m.zw;V.F=C?C.F:null;setWater(m.zw);
  // rain
  const N=innerWidth<700?700:1800,rp=new Float32Array(N*3);
  for(let i=0;i<N;i++){rp[i*3]=x0-20+rand()*(L+40);rp[i*3+1]=rand()*m.H*2.5;rp[i*3+2]=-D/2+rand()*D;}
  const rg=new THREE.BufferGeometry();rg.setAttribute("position",new THREE.BufferAttribute(rp,3));
  V.rain=new THREE.Points(rg,new THREE.PointsMaterial({color:0x5F8FB8,size:Math.max(0.25,m.H*0.012),transparent:true,opacity:0}));W.add(V.rain);
  // dust burst
  const dp=new Float32Array(400*3);const dg=new THREE.BufferGeometry();dg.setAttribute("position",new THREE.BufferAttribute(dp,3));
  V.dust=new THREE.Points(dg,new THREE.PointsMaterial({color:0xD9C3A0,size:Math.max(0.5,m.H*0.02),transparent:true,opacity:0}));V.dustV=new Float32Array(400*3);W.add(V.dust);
  // camera
  V.tgt=new THREE.Vector3((x0+x1)/2-L*0.08,m.H*0.35,0);V.rad0=V.rad=Math.max(L,D)*1.25*(V.cam.aspect<1?1.75:1);V.th=-0.55;V.ph=1.12;
  labels3D();inspect();applyToggles();hud3D();
}
function setWater(zw){
  const m=V.model,xs=V.xsW,t=Math.max(0.15,m.H*0.01),mm={...m,zw};
  const pz=x=>{const z=Math.min(zw,m.H);return z<=0?z:(x<=0?0:Math.min(m.surf(x),x>=m.xcr?z:z*x/m.xcr));};
  if(zw<=m.zBed){V.wline.visible=V.wfill.visible=false;return;}
  V.wline.visible=V.wfill.visible=true;
  const a=[],f=[];
  xs.forEach(x=>{const y=pz(x);a.push(x,y-t,0,x,y+t,0);f.push(x,y,0,x,m.zBed,0);});
  const idx=[];for(let i=0;i<xs.length-1;i++){const k=i*2;idx.push(k,k+1,k+2,k+1,k+3,k+2);}
  [[V.wline,a],[V.wfill,f]].forEach(([mesh,arr])=>{const g=new THREE.BufferGeometry();g.setAttribute("position",new THREE.Float32BufferAttribute(arr,3));g.setIndex(idx);mesh.geometry.dispose();mesh.geometry=g;});
}
function hud3D(){
  const d=T[lang];if(!$("h3w"))return;
  $("h3w").textContent=(V.zw<=0?"—":V.zw.toFixed(1)+" m");
  $("h3f").textContent=V.F==null?"—":V.F.toFixed(2);
  $("h3f").className=V.F==null?"":V.F<1?"cbad":V.F<1.5?"cwarn":"cok";
  $("h3s").textContent=d[V.status];
  const o=V.o;$("h3e").textContent=o&&o.kh>0&&o.se.best&&V.mode==="idle"?o.se.best.F.toFixed(2):"—";
}
function storm(){
  if(!V.ok||V.mode==="prep")return;
  const base=V.built,p=base.p;
  build3D(base);V.mode="prep";V.status="stPrep";hud3D();$("storm").disabled=true;
  const z0=Math.max(0,p.zw),z1=p.H*0.96,n=7,seq=[];
  let i=0;
  const step=()=>{
    const z=z0+(z1-z0)*i/(n-1),r=search(makeModel({...p,zw:z}),0);
    seq.push({z,F:r.best?r.best.F:null,b:r.best});
    const failed=r.best&&r.best.F<1;
    if(failed||i===n-1){
      V.seq=seq;
      if(failed)build3D(base,r.best);
      V.seq=seq;V.fail=failed;V.mode="rain";V.t=0;V.zw=z0;V.F=seq[0].F;V.status="stRain";hud3D();$("storm").disabled=false;
      return;}
    i++;setTimeout(step,0);
  };
  setTimeout(step,30);
}
function interpSeq(u){ // u in [0,1] along seq
  const s=V.seq,k=u*(s.length-1),i=Math.min(s.length-2,Math.floor(k)),f=k-i;
  if(s.length===1)return s[0];
  const a=s[i],b=s[i+1];return {z:a.z+(b.z-a.z)*f,F:(a.F!=null&&b.F!=null)?a.F+(b.F-a.F)*f:(b.F??a.F)};
}
function loop3D(now){
  requestAnimationFrame(loop3D);
  const dt=Math.min(0.05,(now-V.last)/1000);V.last=now;
  if($("p2").hidden||!V.world)return;
  sensFrame(now);
  V.t+=dt;const m=V.model;
  // sea waves
  const pa=V.sea.geometry.attributes.position;
  for(let i=0;i<pa.count;i++){const bx=V.seaBase[i*3],bz=V.seaBase[i*3+2];pa.array[i*3+1]=Math.sin(bx*0.08+now*0.0012)*0.25+Math.cos(bz*0.06+now*0.0009)*0.2;}
  pa.needsUpdate=true;
  // storm phases
  const RAIN=6.5;
  if(V.mode==="rain"){
    const u=Math.min(1,V.t/RAIN),v=interpSeq(u);V.zw=v.z;V.F=v.F;setWater(v.z);
    V.rain.material.opacity=Math.min(0.8,V.t*0.6);
    if(u>=1){ if(V.fail){V.mode="slide";V.t=0;V.status="stFail";burst();}else{V.mode="done";V.status="stOk";} }
    hud3D();
  }else if(V.mode==="slide"){
    const u=Math.min(1,V.t/3.2),e=u*u*(3-2*u);
    if(V.pivot){V.pivot.rotation.z=-0.55*e;V.pivot.position.y=V.circle.yc-m.H*0.25*e*e;V.pivot.position.x=V.circle.xc-m.H*0.15*e;}
    if(u>=1){V.mode="done";}
  }else if(V.mode==="done"){V.rain.material.opacity=Math.max(0,V.rain.material.opacity-dt*0.2);}
  // rain motion
  if(V.rain.material.opacity>0){const rp=V.rain.geometry.attributes.position;
    for(let i=0;i<rp.count;i++){rp.array[i*3+1]-=dt*m.H*1.6;if(rp.array[i*3+1]<0)rp.array[i*3+1]+=m.H*2.5;}rp.needsUpdate=true;}
  // dust
  if(V.dust.material.opacity>0){const dp=V.dust.geometry.attributes.position;
    for(let i=0;i<dp.count;i++){V.dustV[i*3+1]-=dt*9;for(let k=0;k<3;k++)dp.array[i*3+k]+=V.dustV[i*3+k]*dt;}
    dp.needsUpdate=true;V.dust.material.opacity=Math.max(0,V.dust.material.opacity-dt*0.25);}
  // camera: gentle idle sway
  const th=V.th+(V.drag?0:Math.sin(now*0.00018)*0.12);
  V.cam.position.set(V.tgt.x+V.rad*Math.sin(V.ph)*Math.sin(th),V.tgt.y+V.rad*Math.cos(V.ph),V.tgt.z+V.rad*Math.sin(V.ph)*Math.cos(th));
  V.cam.lookAt(V.tgt);
  V.r.render(V.scene,V.cam);
}
function burst(){
  const C=V.circle,m=V.model,dp=V.dust.geometry.attributes.position,D=V.D;
  for(let i=0;i<dp.count;i++){const lft=Math.random()<0.6,x=lft?C.xl:C.xr;
    dp.array[i*3]=x+(Math.random()-.5)*3;dp.array[i*3+1]=m.surf(x)+Math.random()*2;dp.array[i*3+2]=D/2-Math.random()*Math.min(D*0.5,(C.xr-C.xl)*0.9);
    V.dustV[i*3]=(Math.random()-.8)*10;V.dustV[i*3+1]=4+Math.random()*10;V.dustV[i*3+2]=(Math.random()-.5)*6;}
  dp.needsUpdate=true;V.dust.material.opacity=0.85;
}
function reset3D(){if(V.ok&&(last||V.built)){build3D(last||V.built);}}
function applyToggles(){if(!V.G)return;document.querySelectorAll("#tgl input").forEach(c=>{const g=V.G[c.dataset.g];if(g)g.visible=c.checked;if(c.dataset.g==="houses"&&V.hp)V.hp.visible=c.checked;});}
document.querySelectorAll("#tgl input").forEach(c=>c.addEventListener("change",applyToggles));
function makeLabel(text,opt){
  opt=opt||{};const fs=48,pad=18,cv=document.createElement("canvas"),cx=cv.getContext("2d");
  const font=`700 ${fs}px "IBM Plex Sans Arabic","Segoe UI",Tahoma,Arial,sans-serif`;cx.font=font;
  const w=Math.ceil(cx.measureText(text).width)+pad*2,h=fs+pad*1.4;cv.width=w;cv.height=h;
  cx.font=font;cx.fillStyle=opt.bg||"rgba(10,22,40,.82)";
  const r=16;cx.beginPath();cx.moveTo(r,0);cx.arcTo(w,0,w,h,r);cx.arcTo(w,h,0,h,r);cx.arcTo(0,h,0,0,r);cx.arcTo(0,0,w,0,r);cx.fill();
  cx.fillStyle=opt.color||"#FFFFFF";cx.textBaseline="middle";cx.textAlign="center";
  cx.direction=/[\u0600-\u06FF]/.test(text)?"rtl":"ltr";cx.fillText(text,w/2,h/2+2);
  const tx=new THREE.CanvasTexture(cv);tx.minFilter=THREE.LinearFilter;
  const sp=new THREE.Sprite(new THREE.SpriteMaterial({map:tx,depthTest:false,transparent:true}));
  const k=(opt.size||V.model.H*0.055)/h;sp.scale.set(w*k,h*k,1);sp.renderOrder=10;return sp;
}
function labels3D(){
  if(!V.G)return;const G=V.G.labels,m=V.model,C=V.circle,D=V.D,d=T[lang];
  while(G.children.length){const c=G.children.pop();c.material.map.dispose();c.material.dispose();}
  const add=(t,x,y,z,o)=>{const s=makeLabel(t,o);s.position.set(x,y,z);G.add(s);};
  let top=m.H;m.layers.forEach((Ly,i)=>{const mid=(Math.min(top,m.H)+Ly.bot)/2;
    add(`${d.layN[i]} · c′=${Ly.c} · φ′=${Ly.phi}°`,V.x1-m.H*0.55,mid,D/2+0.5,{size:m.H*0.16,bg:"rgba(255,255,255,.85)",color:"#12304A"});top=Ly.bot;});
  add(`H = ${m.H} m`,m.xcr+1,m.H*0.5,D/2+1,{size:m.H*0.1});
  add(`β = ${m.beta}°`,m.H*0.35,m.H*0.06,D/2+1.5,{size:m.H*0.1});
  if(m.q>0)add(`q = ${m.q} kPa`,m.xcr+m.qd+m.qB/2,m.H+m.H*0.35,D/2-2,{size:m.H*0.11,color:"#F5C74E"});
  if(C)add(`F = ${C.F.toFixed(2)}`,C.xc,C.yc+m.H*0.12,D/2,{size:m.H*0.14,color:C.F<1?"#FF8DB8":C.F<1.5?"#F5C74E":"#8CE08A"});
  if(m.zw>0)add(lang==="ar"?`${d.hudW} ${m.zw} م`:`${d.hudW} ${m.zw} m`,V.x1-m.H*0.1,Math.min(m.zw,m.H)+m.H*0.06,D/2+0.5,{size:m.H*0.14,color:"#9CCBFF"});
}
function inspect(){
  const n=+$("slc").value;$("slcN").textContent=n;
  const C=V.circle,d=T[lang];
  if(!V.sel||!C||!C.S){$("slcR").textContent="";return;}
  while(V.sel.children.length){const c=V.sel.children.pop();disposeTree(c);}
  const sl=C.S[n-1],m=V.model,D=V.D,x0=sl.xm-C.bw/2,x1=sl.xm+C.bw/2;
  const arc=x=>C.yc-Math.sqrt(Math.max(0,C.R*C.R-(x-C.xc)**2));
  const pts=[[x0,m.surf(x0)],[x1,m.surf(x1)],[x1,arc(x1)],[x0,arc(x0)]].map(p=>[p[0]-C.xc,p[1]-C.yc]);
  const geo=new THREE.ExtrudeGeometry(shapeFrom(pts),{depth:1.2,bevelEnabled:false});
  const mesh=new THREE.Mesh(geo,new THREE.MeshLambertMaterial({color:0xD4A017,emissive:0x3A2A00}));mesh.position.z=D/2-0.2;V.sel.add(mesh);
  const cx=sl.xm-C.xc,cy=(sl.ys+sl.yb)/2-C.yc,z=D/2+1.2,Lm=m.H*0.35,wMax=Math.max(...C.S.map(s=>s.W));
  const L=v=>Math.max(m.H*0.08,Lm*v/wMax);
  const arr=(dir,len,col,ox,oy)=>{const a=new THREE.ArrowHelper(dir.normalize(),new THREE.Vector3(ox,oy,z),len,col,len*0.25,len*0.15);V.sel.add(a);};
  arr(new THREE.Vector3(0,-1,0),L(sl.W),0x12304A,cx,cy);
  const kh=V.o.kh||0;if(kh>0)arr(new THREE.Vector3(-1,0,0),L(sl.W*kh)*1.5,0xE08A00,cx,cy);
  const by=sl.yb-C.yc,al=sl.al;
  arr(new THREE.Vector3(Math.cos(al),Math.sin(al),0),m.H*0.12,0x3F7A3A,cx,by);
  $("slcR").textContent=d.inspR.replace("{a}",(al*180/Math.PI).toFixed(1)).replace("{w}",sl.W.toFixed(0)).replace("{u}",sl.u.toFixed(1)).replace("{c}",sl.c).replace("{p}",(Math.atan(sl.t)*180/Math.PI).toFixed(0));
}
$("slc").addEventListener("input",inspect);
/* ---- 3D sensitivity bars ---- */
const SV={};
function initSens(){
  const box=$("s3d");SV.r=new THREE.WebGLRenderer({antialias:true});SV.r.setPixelRatio(Math.min(2,devicePixelRatio||1));box.appendChild(SV.r.domElement);
  SV.scene=new THREE.Scene();SV.scene.background=new THREE.Color(0x0A1628);
  SV.cam=new THREE.PerspectiveCamera(38,2,0.1,200);
  SV.scene.add(new THREE.HemisphereLight(0xffffff,0x223344,0.9));const dl=new THREE.DirectionalLight(0xffffff,0.6);dl.position.set(5,10,8);SV.scene.add(dl);
  new ResizeObserver(()=>{const w=box.clientWidth,h=Math.round(w*(w<500?0.7:0.42));SV.r.setSize(w,h);SV.cam.aspect=w/h;SV.cam.updateProjectionMatrix();}).observe(box);
}
function buildSens(o){
  if(!SV.r)return;if(SV.g){SV.scene.remove(SV.g);SV.g.traverse(n=>{n.geometry&&n.geometry.dispose();if(n.material){n.material.map&&n.material.map.dispose();n.material.dispose();}});}
  const g=new THREE.Group();SV.g=g;SV.scene.add(g);const S=o.sens,n=S.length,sp=2.2,maxF=Math.max(2,...S.map(s=>s.F||0)),k=6/maxF;
  const lab=(t,x,y,z,col,size)=>{const s=makeLabelS(t,col,size);s.position.set(x,y,z);g.add(s);};
  S.forEach((s,i)=>{const x=(i-(n-1)/2)*sp;if(s.F==null)return;const h=Math.max(0.05,s.F*k);
    const b=new THREE.Mesh(new THREE.BoxGeometry(1.3,h,1.3),new THREE.MeshLambertMaterial({color:s.F<1?0xA8285F:s.F<CFG.targets.static?0xD4A017:0x3F9A5A}));
    b.position.set(x,h/2,0);b.userData.h=h;g.add(b);
    lab(s.F.toFixed(2),x,h+0.6,0,"#FFFFFF",0.8);
    lab(s.z<0?T[lang].dry:"zw="+s.z,x,-0.6,1.1,"#C9D6E2",0.7);});
  [[1,0xFF6FA8],[CFG.targets.static,0x7FE0A0]].forEach(([f,c])=>{const p=new THREE.Mesh(new THREE.PlaneGeometry(n*sp+1,2.6),new THREE.MeshBasicMaterial({color:c,transparent:true,opacity:.16,side:THREE.DoubleSide,depthWrite:false}));
    p.rotation.x=-Math.PI/2;p.position.y=f*k;g.add(p);lab("F = "+f,-(n*sp)/2-0.6,f*k,0,"#"+c.toString(16),0.7);});
  const base=new THREE.Mesh(new THREE.BoxGeometry(n*sp+1,0.12,2.8),new THREE.MeshLambertMaterial({color:0x1A3550}));base.position.y=-0.06;g.add(base);
  SV.t0=performance.now();
}
function makeLabelS(t,col,size){const s=makeLabel(t,{bg:"rgba(0,0,0,0)",color:col,size:1});s.scale.multiplyScalar(size);return s;}
function sensFrame(now){
  if(!SV.r||!SV.g)return;const a=Math.sin(now*0.0003)*0.35;
  SV.cam.position.set(Math.sin(a)*14,5.5,Math.cos(a)*14);SV.cam.lookAt(0,2.6,0);
  const u=Math.min(1,(now-SV.t0)/900);SV.g.children.forEach(c=>{if(c.userData.h){c.scale.y=u;c.position.y=c.userData.h*u/2;}});
  SV.r.render(SV.scene,SV.cam);
}
