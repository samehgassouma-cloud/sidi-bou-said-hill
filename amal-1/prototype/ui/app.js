/* الواجهة والتحكّم · interface et contrôles · UI and controls — généré/lu par prototype/build_landslide.py · لا تُعدّل الصفحة المبنية مباشرة */
let lang="ar",last=null;
const LD=CFG.layers.map(L=>[L.bot,L.g,L.c,L.phi]);
$("lay").innerHTML=LD.map((r,i)=>`<tr><th class="ln"></th>${r.map((v,k)=>`<td><input type="number" id="L${i}${k}" value="${v}" step="${k===0?0.5:1}" aria-label="L${i+1}-${k}"></td>`).join("")}</tr>`).join("");
function applyLang(l){
  lang=l;const d=T[l];document.documentElement.lang=l;document.documentElement.dir=l==="ar"?"rtl":"ltr";document.title=d.title;
  document.querySelectorAll("[data-i]").forEach(e=>e.textContent=d[e.dataset.i]);
  document.querySelectorAll("[data-list]").forEach(e=>e.innerHTML=d[e.dataset.list].map(x=>`<li>${x}</li>`).join(""));
  document.querySelectorAll("[data-tl]").forEach(e=>e.innerHTML=d.tl.map(x=>`<li><b>${x[0]}</b>${x[1]}</li>`).join(""));
  document.querySelectorAll(".ln").forEach((e,i)=>e.textContent=d.layN[i]);
  document.querySelectorAll("[data-l]").forEach(b=>b.setAttribute("aria-pressed",b.dataset.l===l));
  $("ftr").textContent=l==="ar"?"":" · Sameh Gassouma — "+d.trainer;
  if(last)show(last);
  const L3=T[l].leg,cc=["#C9A06A","#9C7A55","#6E5A48","#2E7BD0","#A8285F"];
  $("leg3").innerHTML=L3.map((t,i)=>`<li><i style="background:${cc[i]}"></i>${t}</li>`).join("");
  if(typeof V!=="undefined"){hud3D();if(V.no)$("h3s").textContent=T[l].no3d;if(V.ok){labels3D();inspect();if(last)buildSens(last);}}
}
document.querySelectorAll("[data-l]").forEach(b=>b.onclick=()=>applyLang(b.dataset.l));
document.querySelectorAll("[role=tab]").forEach(t=>t.onclick=()=>{
  document.querySelectorAll("[role=tab]").forEach(x=>{const on=x===t;x.setAttribute("aria-selected",on);$(x.getAttribute("aria-controls")).hidden=!on;});
  if(t.id==="t2")requestAnimationFrame(open3D);
});
const num=id=>{const v=parseFloat($(id).value);return isFinite(v)?v:NaN};
function read(){
  const p={H:num("H"),beta:num("beta"),zw:num("zw"),q:num("q"),qd:num("qd"),qB:num("qB"),kh:num("kh"),
    layers:[0,1,2].map(i=>({bot:num(`L${i}0`),g:num(`L${i}1`),c:num(`L${i}2`),phi:num(`L${i}3`)}))};
  const vals=[p.H,p.beta,p.zw,p.q,p.qd,p.qB,p.kh,...p.layers.flatMap(L=>[L.bot,L.g,L.c,L.phi])];
  if(vals.some(isNaN)||p.H<3||p.H>150||p.beta<10||p.beta>75||p.kh<0||p.kh>0.5||p.q<0||p.qd<0||p.qB<0||
     p.layers.some(L=>L.g<CFG.limits.g[0]||L.g>CFG.limits.g[1]||L.c<CFG.limits.c[0]||L.phi<CFG.limits.phi[0]||L.phi>CFG.limits.phi[1]))return {e:"errVal"};
  const b=p.layers.map(L=>L.bot);
  if(!(b[0]>b[1]&&b[1]>b[2]&&b[2]<=0))return {e:"errLay"};
  return {p};
}
function computeAll(p){
  const m=makeModel(p);
  const st=search(m,0),se=p.kh>0?search(m,p.kh):st;
  const levels=CFG.waterLevels.map(f=>f<0?-1:Math.round(f*p.H*10)/10);
  const sens=levels.map(z=>{const b=search(makeModel({...p,zw:z}),0).best;return {z,F:b?b.F:null}});
  return {m,st,se,sens,kh:p.kh,p};
}
function run(cb){
  const r=read();$("err").textContent=r.e?T[lang][r.e]:"";if(r.e)return;
  $("run").disabled=true;$("run").textContent=T[lang].calc;$("busy").textContent=T[lang].calc;$("busy").hidden=false;
  setTimeout(()=>{
    last=computeAll(r.p);show(last);
    if(V.ok&&V.mode!=="prep"){build3D(last);buildSens(last);}
    $("run").disabled=false;$("run").textContent=T[lang].run;$("busy").hidden=true;
    if(typeof cb==="function")cb();
  },30);
}
$("run").onclick=()=>run();
let deb=null;document.querySelectorAll(".eng input[type=number]").forEach(i=>i.addEventListener("input",()=>{clearTimeout(deb);deb=setTimeout(()=>run(),900);}));
function kpi(k,v,s,F,target){
  const d=T[lang];$(v).textContent=F==null?"—":F.toFixed(2);
  const c=F==null?"":F<1?"bad":F<target?"warn":"ok";$(k).className="kpi "+c;
  $(s).textContent=F==null?d.none:F<1?d.lo:F<target?d.mid:d.hi;
}
function fit(cv,ratio){const r=cv.getBoundingClientRect(),dpr=devicePixelRatio||1;cv.width=r.width*dpr;cv.height=r.width*ratio*dpr;const c=cv.getContext("2d");c.setTransform(dpr,0,0,dpr,0,0);c.direction="ltr";cv.dir="ltr";return {c,w:r.width,h:r.width*ratio}}
function css(v){return getComputedStyle(document.documentElement).getPropertyValue(v).trim()}
function show(o){
  const d=T[lang],{m,st,se}=o,B=st.best;
  kpi("k1","v1","s1",B?B.F:null,CFG.targets.static);
  if(o.kh>0)kpi("k2","v2","s2",se.best?se.best.F:null,CFG.targets.seismic);else{$("v2").textContent="—";$("k2").className="kpi";$("s2").textContent="kh = 0";}
  $("circ").textContent=B?d.circ.replace("{x}",B.xc.toFixed(1)).replace("{y}",B.yc.toFixed(1)).replace("{r}",B.R.toFixed(1)).replace("{a}",B.xl.toFixed(1)).replace("{b}",B.xr.toFixed(1)):d.none;
  if(!V.no){ $("slices").innerHTML=sliceRows(B,d); return; }
  // section
  const cv=$("cv");const {c,w,h}=fit(cv,0.62);
  const x0=-0.6*m.H,x1=m.xcr+1.8*m.H,y0=m.zBed-2;let y1=m.H*1.25;
  if(B)y1=Math.max(y1,Math.min(B.yc+2,m.H*3));
  const k=Math.min((w-20)/(x1-x0),(h-20)/(y1-y0)),ox=10+((w-20)-(x1-x0)*k)/2,oy=h-10;
  const X=x=>ox+(x-x0)*k,Y=y=>oy-(y-y0)*k;
  c.clearRect(0,0,w,h);
  const cols=["#C9A06A","#9C7A55","#6E5A48"];
  let top=null;
  m.layers.forEach((L,i)=>{c.beginPath();
    const tp=x=>Math.min(m.surf(x),top===null?1e9:top);
    const xs=[];for(let x=x0;x<=x1;x+=(x1-x0)/200)xs.push(x);
    xs.forEach((x,j)=>{const y=Math.max(tp(x),L.bot);j?c.lineTo(X(x),Y(y)):c.moveTo(X(x),Y(y));});
    c.lineTo(X(x1),Y(L.bot));c.lineTo(X(x0),Y(L.bot));c.closePath();c.fillStyle=cols[i];c.fill();top=L.bot;});
  c.fillStyle="rgba(28,90,134,.55)";c.fillRect(X(x0),Y(0),X(0)-X(x0),Y(y0)-Y(0));
  // water line
  if(m.zw>y0){c.setLineDash([6,5]);c.strokeStyle="#2E7BD0";c.lineWidth=2;c.beginPath();
    for(let x=x0,j=0;x<=x1;x+=(x1-x0)/200,j++){const y=m.pz(x);j?c.lineTo(X(x),Y(y)):c.moveTo(X(x),Y(y));}c.stroke();c.setLineDash([]);}
  // surcharge
  if(m.q>0&&m.qB>0){const a=X(m.xcr+m.qd),b=X(m.xcr+m.qd+m.qB),hh=Math.min(40,8+m.q/4);
    c.fillStyle="#F4F6F8";c.strokeStyle="#1F5FA8";c.lineWidth=1.5;c.fillRect(a,Y(m.H)-hh,b-a,hh);c.strokeRect(a,Y(m.H)-hh,b-a,hh);}
  // grid
  st.grid.forEach(g=>{c.fillStyle=g.F<1?"#A8285F":g.F<CFG.targets.static?"#D09A1E":"#3F7A3A";c.globalAlpha=.55;c.beginPath();c.arc(X(g.xc),Y(g.yc),2.2,0,7);c.fill();});
  c.globalAlpha=1;
  if(B){
    c.fillStyle="rgba(168,40,95,.18)";c.beginPath();
    B.S.forEach((s,i)=>{i?c.lineTo(X(s.xm),Y(s.yb)):c.moveTo(X(s.xm),Y(s.yb))});
    for(let i=B.S.length-1;i>=0;i--)c.lineTo(X(B.S[i].xm),Y(B.S[i].ys));c.fill();
    c.strokeStyle="rgba(168,40,95,.35)";c.lineWidth=1;
    B.S.forEach((s,i)=>{if(i%3===0){c.beginPath();c.moveTo(X(s.xm-B.bw/2),Y(s.yb));c.lineTo(X(s.xm-B.bw/2),Y(s.ys));c.stroke();}});
    c.strokeStyle="#A8285F";c.lineWidth=2.5;c.beginPath();
    const a0=Math.atan2(-(Math.sqrt(Math.max(0,B.R*B.R-(B.xl-B.xc)**2))),B.xl-B.xc),a1=Math.atan2(-(Math.sqrt(Math.max(0,B.R*B.R-(B.xr-B.xc)**2))),B.xr-B.xc);
    for(let i=0;i<=60;i++){const t=a0+(a1-a0)*i/60,x=B.xc+B.R*Math.cos(t),y=B.yc+B.R*Math.sin(t);i?c.lineTo(X(x),Y(y)):c.moveTo(X(x),Y(y));}
    c.stroke();
    c.setLineDash([3,4]);c.lineWidth=1;c.beginPath();c.moveTo(X(B.xc),Y(B.yc));c.lineTo(X(B.xl),Y(m.surf(B.xl)));c.moveTo(X(B.xc),Y(B.yc));c.lineTo(X(B.xr),Y(m.surf(B.xr)));c.stroke();c.setLineDash([]);
    c.fillStyle="#A8285F";c.beginPath();c.arc(X(B.xc),Y(B.yc),4,0,7);c.fill();
    c.font="bold 14px sans-serif";c.fillText("F = "+B.F.toFixed(2),X(B.xc)+8,Y(B.yc)-6);
  }
  c.save();c.font="bold 13px sans-serif";c.fillStyle=css("--muted");c.textAlign="right";
  c.fillText({ar:"تقديري — غير معتمد",fr:"Indicatif — non certifié",en:"Indicative — not certified"}[lang],w-12,20);c.restore();
  // sensitivity
  const {c:c2,w:w2,h:h2}=fit($("cv2"),innerWidth<700?0.6:0.34),S=o.sens,maxF=Math.max(2,...S.map(s=>s.F||0));
  c2.clearRect(0,0,w2,h2);const bw=(w2-40)/S.length,base=h2-28;
  const yF=f=>base-(f/maxF)*(base-14);
  c2.strokeStyle=css("--muted");c2.setLineDash([4,4]);
  [[1,"#A8285F"],[CFG.targets.static,"#3F7A3A"]].forEach(([f,col])=>{c2.strokeStyle=col;c2.beginPath();c2.moveTo(30,yF(f));c2.lineTo(w2-6,yF(f));c2.stroke();c2.fillStyle=col;c2.font="11px sans-serif";c2.fillText(f.toFixed(1),2,yF(f)+4);});
  c2.setLineDash([]);
  S.forEach((s,i)=>{const x=34+i*bw;if(s.F!=null){c2.fillStyle=s.F<1?"#A8285F":s.F<CFG.targets.static?"#D09A1E":"#3F7A3A";c2.fillRect(x+bw*.2,yF(s.F),bw*.6,base-yF(s.F));
    c2.fillStyle=css("--ink");c2.font="bold 12px sans-serif";c2.textAlign="center";c2.fillText(s.F.toFixed(2),x+bw/2,yF(s.F)-4);}
    c2.fillStyle=css("--muted");c2.font="11px sans-serif";c2.textAlign="center";c2.fillText(s.z<0?({ar:"جاف",fr:"sec",en:"dry"})[lang]:"zw="+s.z,x+bw/2,h2-10);c2.textAlign="start";});
  $("slices").innerHTML=sliceRows(B,d);
}
function sliceRows(B,d){return B?`<tr>${d.th.map(t=>`<th>${t}</th>`).join("")}</tr>`+B.S.map(s=>`<tr><td>${s.xm.toFixed(1)}</td><td>${(s.al*180/Math.PI).toFixed(1)}</td><td>${s.W.toFixed(0)}</td><td>${(s.u).toFixed(1)}</td><td>${s.c}</td><td>${(Math.atan(s.t)*180/Math.PI).toFixed(0)}</td></tr>`).join(""):"";}
addEventListener("resize",()=>{if(last&&!$("p2").hidden)show(last)});
$("storm").onclick=()=>storm();$("reset3").onclick=()=>reset3D();
applyLang("ar");
