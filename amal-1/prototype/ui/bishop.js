/* محرّك Bishop المبسّط · moteur Bishop simplifié · simplified Bishop engine — généré/lu par prototype/build_landslide.py · لا تُعدّل الصفحة المبنية مباشرة */
function makeModel(p){
  const tb=Math.tan(p.beta*Math.PI/180), xcr=p.H/tb;
  const layers=p.layers; // [{bot,g,c,phi}] top->bottom
  const zBed=layers[layers.length-1].bot;
  const xmin=-1.5*p.H-10, xmax=xcr+2.5*p.H+10;
  const surf=x=>x<=0?0:(x>=xcr?p.H:x*tb);
  const zwp=Math.min(p.zw,p.H);
  const pz=x=>zwp<=0?zwp:(x<=0?0:Math.min(surf(x),x>=xcr?zwp:zwp*x/xcr));
  return {...p,tb,xcr,zBed,xmin,xmax,surf,pz};
}
function layerAt(m,y){for(const L of m.layers){if(y>=L.bot)return L;}return m.layers[m.layers.length-1];}
function colWeight(m,ys,yb){
  let w=0,top=Infinity;
  for(const L of m.layers){const hi=Math.min(ys,top),lo=Math.max(yb,L.bot);if(hi>lo)w+=(hi-lo)*L.g;top=L.bot;}
  return w;
}
function bishop(m,xc,yc,R,kh,keep){
  const GW=9.81,arc=x=>{const d=R*R-(x-xc)*(x-xc);return d<0?NaN:yc-Math.sqrt(d);};
  const a=Math.max(m.xmin,xc-R),b=Math.min(m.xmax,xc+R),N=300,dx=(b-a)/N;
  let best=null,run=null;
  for(let i=0;i<=N;i++){const x=a+i*dx,y=arc(x),inside=!isNaN(y)&&y<m.surf(x)-1e-6;
    if(inside){if(!run)run={s:i,e:i};else run.e=i;}
    if((!inside||i===N)&&run){if(!best||run.e-run.s>best.e-best.s)best=run;run=null;}}
  if(!best)return null;
  if((best.s===0&&a<=m.xmin)||(best.e===N&&b>=m.xmax))return null;
  const f=x=>{const y=arc(x);return isNaN(y)?1:y-m.surf(x)};
  const bis=(lo,hi)=>{for(let k=0;k<40;k++){const mid=(lo+hi)/2;(f(lo)>0)===(f(mid)>0)?lo=mid:hi=mid;}return (lo+hi)/2;};
  const xl=best.s>0?bis(a+(best.s-1)*dx,a+best.s*dx):a;
  const xr=best.e<N?bis(a+best.e*dx,a+(best.e+1)*dx):b;
  if(xr-xl<2)return null;
  const ylow=(xc>xl&&xc<xr)?yc-R:Math.min(arc(xl),arc(xr));
  if(ylow<m.zBed-1e-6)return null;
  const n=CFG.slices,bw=(xr-xl)/n,S=[];let drive=0;
  for(let i=0;i<n;i++){
    const xm=xl+(i+.5)*bw,yb=arc(xm),ys=m.surf(xm);if(isNaN(yb))return null;
    const h=Math.sqrt(R*R-(xm-xc)*(xm-xc));const al=Math.atan((xm-xc)/h);
    let W=colWeight(m,ys,yb)*bw;
    const ov=Math.max(0,Math.min(xm+bw/2,m.xcr+m.qd+m.qB)-Math.max(xm-bw/2,m.xcr+m.qd));
    W+=m.q*ov;
    const u=GW*Math.max(0,m.pz(xm)-yb),L=layerAt(m,yb);
    const yg=(ys+yb)/2;
    drive+=W*Math.sin(al)+kh*W*(yc-yg)/R;
    S.push({xm,yb,ys,al,W,u,c:L.c,t:Math.tan(L.phi*Math.PI/180)});
  }
  if(drive<=1e-6)return null;
  let F=1.5;
  for(let it=0;it<60;it++){
    let num=0;
    for(const s of S){const ma=Math.cos(s.al)+Math.sin(s.al)*s.t/F;if(ma<0.2)return null;
      num+=(s.c*bw+Math.max(0,s.W-s.u*bw)*s.t)/ma;}
    const Fn=num/drive;if(Math.abs(Fn-F)<1e-5){F=Fn;break;}F=Fn;
  }
  if(!isFinite(F)||F<=0)return null;
  return keep?{F,xc,yc,R,xl,xr,S,bw}:{F,xc,yc,R};
}
function search(m,kh){
  const H=m.H,top=H-0.5;
  const radii=(xc,yc,nr)=>{const r=[Math.hypot(xc,yc)];
    for(let k=0;k<nr;k++){const yt=m.zBed+(top-m.zBed)*k/(nr-1);if(yc>yt)r.push(yc-yt);}return r;};
  const evalC=(xc,yc,nr)=>{let loc=null;for(const R of radii(xc,yc,nr)){const r=bishop(m,xc,yc,R,kh);if(r&&(!loc||r.F<loc.F))loc=r;}return loc;};
  const X0=-0.5*H,X1=m.xcr+0.8*H,Y0=0.5*H,Y1=3.5*H,n=CFG.search.gridSide,grid=[];
  for(let i=0;i<n;i++)for(let j=0;j<n;j++){
    const r=evalC(X0+(X1-X0)*i/(n-1),Y0+(Y1-Y0)*j/(n-1),CFG.search.radiiCoarse);if(r)grid.push(r);}
  if(!grid.length)return {best:null,grid};
  const seeds=[...grid].sort((a,b)=>a.F-b.F).slice(0,CFG.search.seeds);
  let best=seeds[0];
  for(const sd of seeds){
    let c={...sd},sx=(X1-X0)/(n-1),sy=(Y1-Y0)/(n-1);
    for(let round=0;round<CFG.search.refineRounds;round++){
      for(let i=-2;i<=2;i++)for(let j=-2;j<=2;j++){
        const yc=c.yc+j*sy/2;if(yc<0.2*H)continue;
        const r=evalC(c.xc+i*sx/2,yc,CFG.search.radiiFine);if(r&&r.F<c.F)c=r;}
      // local radius polish
      for(let d=-3;d<=3;d+=0.25){const r=bishop(m,c.xc,c.yc,c.R+d,kh);if(r&&r.F<c.F)c=r;}
      sx/=2;sy/=2;
    }
    if(c.F<best.F)best=c;
  }
  let st=1;for(let it=0;it<60&&st>0.02;it++){let imp=false;
    for(const [a,b2,c2] of [[st,0,0],[-st,0,0],[0,st,0],[0,-st,0],[0,0,st],[0,0,-st],[0,st,st],[0,-st,-st]]){
      const r=bishop(m,best.xc+a,best.yc+b2,best.R+c2,kh);if(r&&r.F<best.F-1e-7){best=r;imp=true;}}
    if(!imp)st/=2;}
  return {best:bishop(m,best.xc,best.yc,best.R,kh,true),grid};
}
