/* Holo card (vanilla port). Based on the React Bits "Holo Card" shader. Check the React Bits license before public use. */
(function(){
const PRESETS=['bursts','stars','shards','cosmos','rainbow','swirl','glitter','gold'];
const PERSPECTIVE=1100;
const VERTEX=`#version 300 es
in vec2 position;
void main(){gl_Position=vec4(position,0.0,1.0);}`;
const FRAGMENT=`#version 300 es
precision highp float;
uniform sampler2D uArt;uniform vec2 uSize;uniform float uAspect;uniform vec2 uTilt;uniform vec2 uLight;uniform float uDistance;uniform int uPreset;uniform float uIntensity;uniform float uScale;uniform float uEdge;uniform float uFrame;uniform float uRadius;uniform float uGlare;uniform vec3 uFoil;uniform float uReady;
out vec4 outColor;
const float TAU=6.28318530718;
struct Foil{float mask;float angle;float jitter;vec2 facet;};
float hash(vec2 p){p=fract(p*vec2(234.34,435.345));p+=dot(p,p+34.23);return fract(p.x*p.y);}
vec2 hash2(vec2 p){return vec2(hash(p),hash(p+17.31));}
vec3 hue(float t){t=abs(fract(t*0.5)*2.0-1.0);vec3 c=mix(vec3(0.1,0.25,1.0),vec3(0.0,0.85,1.0),smoothstep(0.0,0.25,t));c=mix(c,vec3(0.25,1.0,0.2),smoothstep(0.25,0.45,t));c=mix(c,vec3(1.0,0.92,0.05),smoothstep(0.45,0.65,t));c=mix(c,vec3(1.0,0.45,0.05),smoothstep(0.65,0.85,t));return mix(c,vec3(0.95,0.12,0.3),smoothstep(0.85,1.0,t));}
Foil bursts(vec2 p){vec2 q=mat2(0.7071068,0.7071068,-0.7071068,0.7071068)*(p-vec2(0.5,0.5*uAspect))/(0.283/uScale);vec2 d=fract(q)-0.5;float u=length(d)/0.49;float angle=atan(d.y,d.x);
if(u<0.12){float ring=min(floor(u/0.045+0.5),2.0);float count=max(1.0,ring*6.0);float spot=(floor(angle/TAU*count)+0.5)/count*TAU;vec2 dt=vec2(cos(spot),sin(spot))*ring*0.045;float m=smoothstep(0.024,0.012,length(d/0.49-dt));return Foil(m,angle,0.5,vec2(0.0));}
bool inner=u<0.66;float slot=angle/TAU*(inner?56.0:72.0);bool shifted=mod(floor(slot),2.0)>0.5;vec2 band=inner?(shifted?vec2(0.45,0.61):vec2(0.33,0.49)):(shifted?vec2(0.84,0.99):vec2(0.7,0.85));float across=abs(u-(band.x+band.y)*0.5)/((band.y-band.x)*0.5);float along=abs(fract(slot)-0.5)*2.0;float width=inner?0.72:0.6;float m=smoothstep(1.0,0.78,across)*smoothstep(width,width-0.2,along);return Foil(m,angle,0.5,vec2(0.0));}
Foil stars(vec2 p){Foil best=Foil(0.0,0.0,0.0,vec2(0.0));vec2 g=p/(0.08/uScale);vec2 base=floor(g);
for(int j=-1;j<=1;j++){for(int i=-1;i<=1;i++){vec2 id=base+vec2(float(i),float(j));float pick=hash(id+1.3);vec2 d=g-(id+0.5+(hash2(id)-0.5)*0.55);float m=smoothstep(0.07,0.035,length(d));
if(pick<0.62){float size=mix(0.16,0.5,pow(hash(id+9.0),1.8));float sector=TAU/(pick<0.3?4.0:5.0);float k=abs(fract((atan(d.y,d.x)+hash(id+4.0)*TAU)/sector)-0.5)*2.0;float edge=size*mix(1.0,0.36,pow(k,0.6));m=smoothstep(edge,edge*0.8,length(d));}
if(m>best.mask)best=Foil(m,hash(id+6.0)*TAU,hash(id+8.0),(hash2(id+2.0)-0.5)*0.6);}}
return best;}
Foil shards(vec2 p){vec2 g=p*19.0*uScale;vec2 base=floor(g);float best=9.0;float second=9.0;vec2 id=base;
for(int j=-1;j<=1;j++){for(int i=-1;i<=1;i++){vec2 cell=base+vec2(float(i),float(j));float d=length(cell+0.08+hash2(cell)*0.84-g);if(d<best){second=best;best=d;id=cell;}else if(d<second){second=d;}}}
float crack=smoothstep(0.015,0.07,second-best);float shine=0.25+0.75*pow(hash(id+7.7),2.0);return Foil((0.2+0.8*crack)*shine,hash(id+3.17)*TAU,hash(id+11.73),(hash2(id+5.0)-0.5)*0.5);}
Foil cosmos(vec2 p){Foil best=Foil(0.0,0.0,0.0,vec2(0.0));vec2 g=p/(0.16/uScale);vec2 base=floor(g);
for(int j=-1;j<=1;j++){for(int i=-1;i<=1;i++){vec2 id=base+vec2(float(i),float(j));vec2 d=g-(id+0.5+(hash2(id)-0.5)*0.7);float size=mix(0.16,0.52,hash(id+2.0));float r=length(d);float m=max(smoothstep(0.05,0.0,abs(r-size)),smoothstep(size,size-0.04,r)*0.22);if(m>best.mask)best=Foil(m,hash(id+6.0)*TAU+atan(d.y,d.x)*0.5,hash(id+1.0),(hash2(id+4.0)-0.5)*0.5);}}
vec2 fine=p/(0.035/uScale);vec2 cell=floor(fine);float dots=smoothstep(0.2,0.1,length(fine-cell-0.5-(hash2(cell+9.0)-0.5)*0.6))*step(0.55,hash(cell+2.0));if(dots>best.mask)best=Foil(dots,hash(cell)*TAU,hash(cell+3.0),(hash2(cell+7.0)-0.5)*0.6);return best;}
Foil rainbow(vec2 p){return Foil(0.86+0.14*hash(floor(p*700.0*uScale)),0.2,0.5,vec2(0.0));}
Foil swirl(vec2 p){vec2 d=p-vec2(0.5,0.42*uAspect);float angle=atan(d.y,d.x);float rays=0.55+0.45*smoothstep(0.3,0.7,abs(fract(angle/TAU*60.0*uScale)-0.5)*2.0);return Foil(rays,angle,length(d),vec2(0.0));}
Foil glitter(vec2 p){vec2 g=p*72.0*uScale;vec2 cell=floor(g);float size=mix(0.18,0.4,hash(cell+3.0));float m=smoothstep(size,size*0.55,length(fract(g)-0.5-(hash2(cell)-0.5)*0.5))*step(0.25,hash(cell+5.0));return Foil(m,hash(cell+7.0)*TAU,hash(cell+9.0),(hash2(cell+11.0)-0.5)*0.9);}
Foil gold(vec2 p){Foil flake=glitter(p*0.8);if(flake.mask>0.5)return flake;float etch=0.55+0.45*smoothstep(0.2,0.8,abs(fract((p.x*0.6+p.y)*140.0*uScale)-0.5)*2.0);return Foil(etch,0.9,0.4,vec2(0.0));}
vec3 sparkles(vec2 p,vec3 halfway,vec2 sweep,float awake){vec2 g=p*62.0;vec2 cell=floor(g);vec2 d=fract(g)-0.5-(hash2(cell)-0.5)*0.36;float spin=hash(cell+3.0)*TAU;d=mat2(cos(spin),-sin(spin),sin(spin),cos(spin))*d;vec2 a=abs(d);float hexagon=max(a.x*0.866+a.y*0.5,a.y);float size=mix(0.22,0.38,hash(cell+2.0));float piece=smoothstep(size,size-0.07,hexagon)*step(0.42,hash(cell+4.0));vec3 facet=normalize(vec3((hash2(cell+6.0)-0.5)*0.9,1.0));float flash=pow(max(dot(facet,halfway),0.0),6.0);vec3 tint=hue(dot(sweep,vec2(cos(spin),sin(spin)))*1.2+dot(sweep,vec2(0.8,0.6))*0.8+hash(cell+8.0)*0.5);vec3 color=piece*tint*(0.3+1.6*flash)*awake;vec2 fine=p*210.0;vec2 speckCell=floor(fine);float speck=smoothstep(0.24,0.0,length(fract(fine)-0.5-(hash2(speckCell)-0.5)*0.5))*step(0.72,hash(speckCell+1.0));float speckFlash=pow(max(dot(normalize(vec3((hash2(speckCell+2.0)-0.5)*0.9,1.0)),halfway),0.0),10.0);return color+vec3(1.2)*speck*speckFlash*(1.0-piece);}
void main(){vec2 uv=vec2(gl_FragCoord.x/uSize.x,1.0-gl_FragCoord.y/uSize.y);vec2 p=vec2(uv.x,uv.y*uAspect);vec2 center=vec2(0.5,0.5*uAspect);vec2 q=abs(p-center)-center+uRadius;float outside=length(max(q,0.0))+min(max(q.x,q.y),0.0)-uRadius;float pixel=1.0/uSize.x;float alpha=clamp(0.5-outside/pixel,0.0,1.0);vec4 sampled=texture(uArt,uv);if(uReady>0.5)alpha*=sampled.a;if(alpha<=0.0){outColor=vec4(0.0);return;}
vec3 art=uReady>0.5?pow(sampled.rgb,vec3(2.2)):vec3(0.12);
mat3 rx=mat3(1.0,0.0,0.0,0.0,cos(uTilt.x),sin(uTilt.x),0.0,-sin(uTilt.x),cos(uTilt.x));mat3 ry=mat3(cos(uTilt.y),0.0,-sin(uTilt.y),0.0,1.0,0.0,sin(uTilt.y),0.0,cos(uTilt.y));mat3 turn=rx*ry;vec3 world=turn*vec3(p-center,0.0);vec3 view=normalize(transpose(turn)*(vec3(0.0,0.0,uDistance)-world));vec3 lamp=vec3((uLight-0.5)*vec2(1.1,1.1*uAspect),0.9);vec3 light=normalize(transpose(turn)*(lamp-world));vec3 halfway=normalize(light+view);vec2 sweep=light.xy+view.xy;float sheen=pow(max(halfway.z,0.0),10.0);float shine=pow(max(halfway.z,0.0),80.0);float frame=1.0-smoothstep(uFrame-pixel,uFrame+pixel,-outside);
Foil f;if(uPreset==0)f=bursts(p);else if(uPreset==1)f=stars(p);else if(uPreset==2)f=shards(p);else if(uPreset==3)f=cosmos(p);else if(uPreset==4)f=rainbow(p);else if(uPreset==5)f=swirl(p);else if(uPreset==6)f=glitter(p);else f=gold(p);
vec3 metal=uPreset==7?vec3(1.0,0.74,0.38)*dot(uFoil,vec3(0.3333))*1.15:uFoil;
vec4 look=uPreset==0?vec4(0.25,1.9,0.12,1.0):uPreset==1?vec4(0.6,1.4,0.3,1.0):uPreset==2?vec4(0.9,0.9,0.6,0.5):uPreset==3?vec4(0.7,1.2,0.35,0.85):uPreset==4?vec4(0.0,2.2,0.0,0.45):uPreset==5?vec4(1.6,0.3,0.0,0.4):uPreset==6?vec4(0.9,1.0,0.6,1.0):vec4(0.3,1.0,0.2,0.95);
vec2 dir=vec2(cos(f.angle),sin(f.angle));float phase=dot(sweep,dir)*look.x+dot(sweep,vec2(0.8,0.6))*look.y+f.jitter*look.z;float spoke=1.0;
if(uPreset==5){float facing=dot(normalize(sweep+0.0001),dir);phase=f.jitter*2.4+facing*0.6+length(sweep)*0.8;spoke=0.3+0.7*smoothstep(0.25,0.95,abs(facing));}
vec3 tint=hue(phase);if(uPreset==7)tint=mix(tint,metal,0.65);
float glint=pow(max(dot(normalize(vec3(f.facet,1.0)),halfway),0.0),24.0)*step(0.001,length(f.facet));bool layered=uPreset==2||uPreset==4||uPreset==5||uPreset==7;
vec3 foil=(layered?tint:mix(tint,vec3(1.0),0.12))*(1.15+0.3*sheen)+metal*glint*1.2;float tilted=smoothstep(0.02,0.21,length(sin(uTilt)));float awake=mix(0.2,1.0,tilted);float strength=uIntensity*f.mask*(1.0-frame)*awake;
float band=uPreset==5?spoke:layered?0.25+0.75*smoothstep(0.3,0.95,0.5+0.5*cos(phase*TAU*0.5+1.3)):1.0;
vec3 color=layered?1.0-(1.0-art)*(1.0-clamp(foil*look.w*band*strength,0.0,1.0)):mix(art,foil,clamp(strength*look.w,0.0,1.0));
color+=sparkles(p,halfway,sweep,mix(0.55,1.0,tilted))*uEdge*frame;color+=uFoil*sheen*0.12*frame;color+=vec3(sheen*0.07+shine*0.3)*uGlare;color=pow(clamp(color,0.0,1.0),vec3(1.0/2.2));outColor=vec4(color*alpha,alpha);}`;

const clamp=(v,a,b)=>Math.min(b,Math.max(a,v));
const parseColor=value=>{const fb=[0.78,0.8,0.84];const ctx=document.createElement('canvas').getContext('2d');if(!ctx)return fb;ctx.fillStyle='#000000';ctx.fillStyle=value;const r=ctx.fillStyle;if(!r.startsWith('#')||r.length!==7)return fb;return [1,3,5].map(i=>Math.pow(parseInt(r.slice(i,i+2),16)/255,2.2));};
const compile=(gl,type,src)=>{const s=gl.createShader(type);if(!s)return null;gl.shaderSource(s,src);gl.compileShader(s);if(gl.getShaderParameter(s,gl.COMPILE_STATUS))return s;console.warn(gl.getShaderInfoLog(s));gl.deleteShader(s);return null;};

/* HoloCard(container, {image, backImage, alt, preset, ...}) -> {destroy()} */
function HoloCard(host,o){
 const S=Object.assign({preset:'gold',intensity:0.85,scale:1,edgeSparkle:0.8,frame:4,glare:0.5,foilColor:'#e2e6ec',width:320,radius:14,tiltMax:14,hoverScale:1.04,idle:true,shadow:true},o);
 const flippable=!!S.backImage;
 const root=document.createElement('div');root.className='holo-card';
 root.style.setProperty('--hc-w',S.width+'px');root.style.setProperty('--hc-ratio',63/88);root.style.setProperty('--hc-radius',S.radius+'px');
 root.setAttribute('role',flippable?'button':'img');if(S.alt)root.setAttribute('aria-label',S.alt);if(flippable)root.tabIndex=0;
 root.innerHTML=(S.shadow?'<span class="holo-card__shadow" aria-hidden="true"></span>':'')+
  '<div class="holo-card__rotor"><div class="holo-card__face holo-card__face--front"><img alt="" draggable="false"><canvas></canvas></div>'+
  (flippable?'<div class="holo-card__face holo-card__face--back"><img alt="" draggable="false"><canvas></canvas></div>':'')+'</div>';
 host.appendChild(root);
 const rotor=root.querySelector('.holo-card__rotor'),shadow=root.querySelector('.holo-card__shadow'),canvas=root.querySelector('.holo-card__face--front canvas'),bcanvas=root.querySelector('.holo-card__face--back canvas'),bctx=bcanvas?bcanvas.getContext('2d'):null;
 const frontImg=root.querySelector('.holo-card__face--front img');frontImg.src=S.image;
 if(flippable)root.querySelector('.holo-card__face--back img').src=S.backImage;
 const cfg=()=>({preset:Math.max(0,PRESETS.indexOf(S.preset)),intensity:clamp(S.intensity,0,1),scale:clamp(S.scale,0.25,4),edge:clamp(S.edgeSparkle,0,1),frame:clamp(S.frame,0,20)/100,glare:clamp(S.glare,0,1),foil:parseColor(S.foilColor),radius:Math.max(0,S.radius),tiltMax:clamp(S.tiltMax,0,45),hoverScale:clamp(S.hoverScale,0.8,1.3),idle:S.idle});
 let C=cfg();
 const reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
 const gl=S.preset==='none'?null:canvas.getContext('webgl2',{alpha:true,premultipliedAlpha:true,antialias:false});
 let program=null,texture=null,texture2=null,buffer=null,textureReady=false,backReady=false;const U={};
 if(gl){const v=compile(gl,gl.VERTEX_SHADER,VERTEX),f=compile(gl,gl.FRAGMENT_SHADER,FRAGMENT);
  if(v&&f){program=gl.createProgram();gl.attachShader(program,v);gl.attachShader(program,f);gl.bindAttribLocation(program,0,'position');gl.linkProgram(program);gl.deleteShader(v);gl.deleteShader(f);if(!gl.getProgramParameter(program,gl.LINK_STATUS)){console.warn(gl.getProgramInfoLog(program));gl.deleteProgram(program);program=null;}}
  if(program){buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),gl.STATIC_DRAW);gl.enableVertexAttribArray(0);gl.vertexAttribPointer(0,2,gl.FLOAT,false,0,0);
   texture2=gl.createTexture();gl.bindTexture(gl.TEXTURE_2D,texture2);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR_MIPMAP_LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,1,1,0,gl.RGBA,gl.UNSIGNED_BYTE,new Uint8Array([0,0,0,0]));
   texture=gl.createTexture();gl.bindTexture(gl.TEXTURE_2D,texture);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR_MIPMAP_LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,1,1,0,gl.RGBA,gl.UNSIGNED_BYTE,new Uint8Array([0,0,0,0]));
   ['uArt','uSize','uAspect','uTilt','uLight','uDistance','uPreset','uIntensity','uScale','uEdge','uFrame','uRadius','uGlare','uFoil','uReady'].forEach(n=>U[n]=gl.getUniformLocation(program,n));}}
 const st={tiltX:0,tiltY:0,tiltVX:0,tiltVY:0,lightX:0.36,lightY:0.26,lightVX:0,lightVY:0,lift:1,liftV:0,turn:0,turnV:0,clock:Math.random()*40};
 const pointer={x:0.5,y:0.5,inside:false};let flipped=false,raf=0,last=0,visible=true,alive=true,calm=0;
 const draw=(face)=>{if(!gl||!program)return;const back=face==='b';if(back&&(!backReady||!bctx))return;const w=canvas.width,h=canvas.height;if(!w||!h)return;
  gl.viewport(0,0,w,h);gl.clearColor(0,0,0,0);gl.clear(gl.COLOR_BUFFER_BIT);gl.useProgram(program);gl.activeTexture(gl.TEXTURE0);gl.bindTexture(gl.TEXTURE_2D,back?texture2:texture);
  gl.uniform1i(U.uArt,0);gl.uniform2f(U.uSize,w,h);gl.uniform1f(U.uAspect,h/w);gl.uniform2f(U.uTilt,st.tiltX*Math.PI/180,(st.tiltY+st.turn-(back?180:0))*Math.PI/180);gl.uniform2f(U.uLight,st.lightX,st.lightY);gl.uniform1f(U.uDistance,PERSPECTIVE/Math.max(1,canvas.clientWidth));gl.uniform1i(U.uPreset,C.preset);gl.uniform1f(U.uIntensity,C.intensity*(back?0.3:1));gl.uniform1f(U.uScale,C.scale);gl.uniform1f(U.uEdge,C.edge);gl.uniform1f(U.uFrame,C.frame);gl.uniform1f(U.uRadius,C.radius/Math.max(1,canvas.clientWidth));gl.uniform1f(U.uGlare,C.glare);gl.uniform3f(U.uFoil,C.foil[0],C.foil[1],C.foil[2]);gl.uniform1f(U.uReady,(back?backReady:textureReady)?1:0);gl.drawArrays(gl.TRIANGLES,0,3);if(back){bctx.clearRect(0,0,bcanvas.width,bcanvas.height);bctx.drawImage(canvas,0,0);}};
 const spring=(v,vel,t,k,d,dt)=>{const n=vel+((t-v)*k-vel*d)*dt;return [v+n*dt,n];};
 const tick=now=>{raf=0;if(!alive)return;const dt=Math.min(1/30,Math.max(1/240,(now-last)/1000));last=now;
  let tx=0,ty=0,lx=0.36,ly=0.26,lift=1;const drifting=C.idle&&!reduce&&!pointer.inside;
  if(pointer.inside&&!reduce){tx=(0.5-pointer.y)*2*C.tiltMax;ty=(pointer.x-0.5)*2*C.tiltMax;lx=pointer.x;ly=pointer.y;lift=C.hoverScale;}
  else if(drifting){st.clock+=dt;const t=st.clock;tx=Math.sin(t*0.7)*C.tiltMax*0.28;ty=Math.sin(t*0.53+1.2)*C.tiltMax*0.4;lx=0.5+Math.sin(t*0.41)*0.42;ly=0.38+Math.sin(t*0.33+0.6)*0.3;}
  const steps=Math.ceil(dt/(1/240)),h=dt/steps;
  for(let i=0;i<steps;i++){[st.tiltX,st.tiltVX]=spring(st.tiltX,st.tiltVX,tx,150,16,h);[st.tiltY,st.tiltVY]=spring(st.tiltY,st.tiltVY,ty,150,16,h);[st.lightX,st.lightVX]=spring(st.lightX,st.lightVX,lx,220,30,h);[st.lightY,st.lightVY]=spring(st.lightY,st.lightVY,ly,220,30,h);[st.lift,st.liftV]=spring(st.lift,st.liftV,lift,320,30,h);[st.turn,st.turnV]=reduce?[flipped?180:0,0]:spring(st.turn,st.turnV,flipped?180:0,170,20,h);}
  rotor.style.transform=`perspective(${PERSPECTIVE}px) scale(${st.lift}) rotateX(${st.tiltX}deg) rotateY(${st.tiltY+st.turn}deg)`;
  if(shadow)shadow.style.transform=`translate(${-st.tiltY*0.7}px, ${st.tiltX*0.7}px) scale(${0.9+(st.lift-1)*1.5})`;
  {const cs=Math.cos((st.tiltY+st.turn)*Math.PI/180);if(cs>0)draw('f');else draw('b');}
  const motion=Math.abs(st.tiltVX)+Math.abs(st.tiltVY)+Math.abs(st.liftV)*40+Math.abs(st.turnV)+(Math.abs(st.lightVX)+Math.abs(st.lightVY))*60+Math.abs(st.tiltX-tx)+Math.abs(st.tiltY-ty);
  calm=motion>0.02?0:calm+dt;if(!visible||(!drifting&&!pointer.inside&&calm>0.3))return;raf=requestAnimationFrame(tick);};
 const wake=()=>{if(raf||!alive)return;calm=0;last=performance.now();raf=requestAnimationFrame(tick);};
 const resize=()=>{const dpr=Math.min(window.devicePixelRatio||1,2);const w=Math.max(1,Math.round(canvas.clientWidth*dpr)),h=Math.max(1,Math.round(canvas.clientHeight*dpr));if(canvas.width!==w||canvas.height!==h){canvas.width=w;canvas.height=h;}if(bcanvas&&(bcanvas.width!==canvas.width||bcanvas.height!==canvas.height)){bcanvas.width=canvas.width;bcanvas.height=canvas.height;}draw('f');wake();};
 const img=new Image();img.crossOrigin='anonymous';img.decoding='async';
 img.onload=()=>{if(!alive)return;if(img.naturalWidth)root.style.setProperty('--hc-ratio',img.naturalWidth/img.naturalHeight);if(!gl||!program)return;
  try{gl.bindTexture(gl.TEXTURE_2D,texture);gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL,false);gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL,false);gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,img);gl.generateMipmap(gl.TEXTURE_2D);textureReady=true;root.setAttribute('data-ready','');draw();wake();}catch(e){textureReady=false;}};
 img.src=S.image;
 if(flippable&&gl){const img2=new Image();img2.crossOrigin='anonymous';img2.decoding='async';img2.onload=()=>{if(!alive||!gl||!program)return;try{gl.bindTexture(gl.TEXTURE_2D,texture2);gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL,false);gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL,false);gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,img2);gl.generateMipmap(gl.TEXTURE_2D);backReady=true;root.setAttribute('data-back-ready','');wake();}catch(e){backReady=false;}};img2.src=S.backImage;}
 const ro=new ResizeObserver(resize);ro.observe(canvas);
 const io=new IntersectionObserver(es=>{visible=es.some(e=>e.isIntersecting);if(visible)wake();});io.observe(root);
 const track=e=>{if(e.pointerType==='touch'&&e.type==='pointermove'&&!e.buttons)return;const r=root.getBoundingClientRect();pointer.x=clamp((e.clientX-r.left)/r.width,0,1);pointer.y=clamp((e.clientY-r.top)/r.height,0,1);pointer.inside=true;wake();};
 const leave=()=>{pointer.inside=false;wake();};
 root.addEventListener('pointerenter',track);root.addEventListener('pointermove',track);root.addEventListener('pointerdown',track);root.addEventListener('pointerleave',leave);root.addEventListener('pointercancel',leave);
 const toggle=()=>{if(flippable){flipped=!flipped;wake();}};
 root.addEventListener('click',toggle);
 root.addEventListener('keydown',e=>{if(!flippable||(e.key!=='Enter'&&e.key!==' '))return;e.preventDefault();if(!e.repeat)toggle();});
 resize();
 return {el:root,hasGL:!!program,destroy(){alive=false;cancelAnimationFrame(raf);ro.disconnect();io.disconnect();if(gl&&program){gl.deleteTexture(texture);gl.deleteTexture(texture2);gl.deleteBuffer(buffer);gl.deleteProgram(program);}root.remove();}};
}
window.HoloCard=HoloCard;
})();
