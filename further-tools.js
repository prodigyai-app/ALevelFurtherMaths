(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.FurtherTools=api;})(typeof window==='undefined'?globalThis:window,()=>{
 'use strict';const first=['fp1','fs1','fm1','d1'];
 function validRoute(a,b){return first.includes(a)&&((first.includes(b)&&a!==b)||b===a.replace('1','2'));}
 function secondOptions(a){return first.includes(a)?[...first.filter(x=>x!==a),a.replace('1','2')]:[];}
 function complex(a,b,c,d){if(![a,b,c,d].every(Number.isFinite))return null;const den=c*c+d*d;return{sum:[a+c,b+d],product:[a*c-b*d,a*d+b*c],quotient:den?[(a*c+b*d)/den,(b*c-a*d)/den]:null,modulus:Math.hypot(a,b),argument:a||b?Math.atan2(b,a):null};}
 function matrix(a,b,c,d,x=1,y=0){if(![a,b,c,d,x,y].every(Number.isFinite))return null;const det=a*d-b*c;return{det,inverse:det?[d/det,-b/det,-c/det,a/det]:null,image:[a*x+b*y,c*x+d*y],trace:a+d};}
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const math=s=>esc(s).replace(/([a-zA-Z0-9π]+)\^\(([^()<>]*)\)/g,'$1<sup>$2</sup>').replace(/([a-zA-Z0-9π]+)\^(-?\d+)/g,'$1<sup>$2</sup>');
 return{first,validRoute,secondOptions,complex,matrix,esc,math};
});
