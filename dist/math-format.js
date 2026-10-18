// Conservative presentation changes inside TeX only; ambiguous quotients remain unchanged.
export function improveMath(source){return String(source).replace(/\$\$([\s\S]*?)\$\$|\$([^$\n]+)\$/g,(whole,display,inline)=>{
 let s=display??inline;
 s=s.replace(/\\tfrac(?![A-Za-z])/g,'\\frac');
 s=s.replace(/(?<![A-Za-z0-9_\\.])(\d+)\/(\d+)(?![\d.])/g,'\\frac{$1}{$2}');
 s=s.replace(/\bdy\/dx\b/g,'\\frac{dy}{dx}');
 s=s.replace(/(?<![A-Za-z0-9_\\])([A-Za-z])\/([A-Za-z])(?![A-Za-z0-9_^])/g,'\\frac{$1}{$2}');
 if(/\\(?:frac|dfrac|sum)(?![A-Za-z])/.test(s)&&!s.includes('\\displaystyle'))s='\\displaystyle '+s;
 return display!==undefined?'$$'+s+'$$':'$'+s+'$';
});}
export function renderMath(el){window.renderMathInElement?.(el,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false,strict:'ignore',trust:false});}
