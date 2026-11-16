/* Shared, dependency-free recipe calculations. Originals are never mutated. */
(function(root){
const phases=['prep','cook','bake','rest','marinate'];
const fractions={'½':.5,'⅓':1/3,'⅔':2/3,'¼':.25,'¾':.75,'⅛':.125,'⅜':.375,'⅝':.625,'⅞':.875};
function quantity(line){
 const m=String(line).match(/^\s*(\d+\s+\d+\/\d+|\d+\s*[½⅓⅔¼¾⅛⅜⅝⅞]|\d+\/\d+|\d+(?:\.\d+)?|[½⅓⅔¼¾⅛⅜⅝⅞])(?=\s|$)/);if(!m)return null;
 const raw=m[1];let value=0;const unicode=raw.match(/[½⅓⅔¼¾⅛⅜⅝⅞]/);if(unicode)value=(parseFloat(raw)||0)+fractions[unicode[0]];else if(raw.includes('/')){const parts=raw.split(/\s+/),f=parts.pop().split('/').map(Number);if(!f[1])return null;value=(Number(parts[0])||0)+f[0]/f[1]}else value=Number(raw);
 const tail=line.slice(m[0].length);if(/^\s*[-–—]/.test(tail))return null;return {value,tail};
}
function friendly(n){if(!Number.isFinite(n)||n<0)return '';let whole=Math.floor(n),part=n-whole;let candidates=Object.entries(fractions).sort((a,b)=>Math.abs(a[1]-part)-Math.abs(b[1]-part));if(part<.018&&whole>0)return String(whole);if(1-part<.018)return String(whole+1);if(Math.abs(candidates[0][1]-part)<.018)return (whole?whole+' ':'')+candidates[0][0];return String(Number(n.toFixed(2)))}
function scale(line,ratio){const q=quantity(line);return q?friendly(q.value*ratio)+q.tail:line}
function lines(s){return String(s||'').split(/\r?\n/).map(s=>s.trim()).filter(Boolean)}
function ingredientText(item){if(item.originalLine)return item.originalLine;return [item.quantity,item.unit,item.name].filter(Boolean).join(' ')+(item.preparation?' — '+item.preparation:'')}
function ingredients(r){if(Array.isArray(r.ingredientItems))return r.ingredientItems;return lines(r.ingredients).map((line,i)=>{const q=quantity(line);let name=line,amount='',unit='';if(q){amount=line.slice(0,line.length-q.tail.length).trim();name=q.tail.trim();const match=name.match(/^(cups?|tablespoons?|teaspoons?|tbsp|tsp|grams?|kilograms?|g|kg|ml|l|litres?|liters?|oz|ounces?|lbs?|pounds?|cloves?|pinches?|cans?)\s+(.*)$/i);if(match){unit=match[1];name=match[2]}}return {id:'legacy-ingredient-'+i,name,quantity:amount,unit,preparation:'',section:'',originalLine:line}})}
function steps(r){if(Array.isArray(r.stepItems))return r.stepItems;return lines(r.steps).map((text,i)=>({id:'legacy-step-'+i,text,...(r.stepMeta?.[i]||{})}))}
function progress(r,s={}){const ii=ingredients(r),ss=steps(r),ingredientsDone=ii.filter(x=>s.checked?.[x.id]).length,stepsDone=ss.filter(x=>s.done?.[x.id]).length,total=ii.length+ss.length,done=ingredientsDone+stepsDone;return {ingredientsDone,stepsDone,ingredientsTotal:ii.length,stepsTotal:ss.length,total,done,percent:total?Math.round(done/total*100):0,complete:total>0&&done===total}}
function reconcileSession(r,old={}){const s={...old,checked:{},done:{},ingredients:{}};ingredients(r).forEach((x,i)=>{if(old.checked?.[x.id]||(!old.schema&&old.checked?.[i]))s.checked[x.id]=true;const v=old.ingredients?.[x.id]??(!old.schema?old.ingredients?.[i]:undefined);if(typeof v==='string')s.ingredients[x.id]=v});steps(r).forEach((x,i)=>{if(old.done?.[x.id]||(!old.schema&&old.done?.[i]))s.done[x.id]=true});s.schema=2;return s}

// A step can overlap only an explicitly selected earlier step.
function timeline(r){let rows=[],end=0;steps(r).forEach((s,i)=>{const overlap=Number(s.overlap);let start=end;if(s.overlap!==''&&s.overlap!=null&&Number.isInteger(overlap)&&overlap>=0&&overlap<i)start=rows[overlap].start;const row={...s,start,end:start+(Number(s.minutes)||0),index:i};rows.push(row);end=Math.max(end,row.end)});return rows}
function timing(r){const ss=steps(r),complete=ss.length>0&&ss.every(s=>s.minutes!==''&&s.minutes!=null&&Number.isFinite(Number(s.minutes))&&Number(s.minutes)>=0);let amounts=Object.fromEntries(phases.map(k=>[k,0]));let total=null,active=null,rows=[];
 if(complete){rows=timeline(r);rows.forEach(s=>{amounts[phases.includes(s.phase)?s.phase:'prep']+=Number(s.minutes)});total=Math.max(...rows.map(s=>s.end));active=rows.filter(s=>s.active).reduce((n,s)=>n+Number(s.minutes),0)}else if(r.timeKnown){phases.forEach(k=>amounts[k]=Number(r.times?.[k])||0);total=Object.values(amounts).reduce((a,b)=>a+b,0);active=r.times?.active===''||r.times?.active==null?null:Number(r.times.active);let cursor=0;rows=phases.filter(k=>amounts[k]>0).map((k,index)=>{const row={text:k==='rest'?'Rest / chill':k,phase:k,start:cursor,end:cursor+amounts[k],index};cursor=row.end;return row})}
 return {amounts,total,active,rows,fromSteps:complete}}
function duration(n){if(n==null)return 'Time not set';return n>=60?Math.floor(n/60)+'h'+(n%60?' '+Number((n%60).toFixed(1))+'m':''):n+' min'}
function remaining(t,now=Date.now()){return Math.max(0,t.status==='running'?t.end-now:t.remaining)}
function matches(r,{query='',category='',favorites=false,limit=null}={}){const total=timing(r).total;return (!category||r.category===category)&&(!favorites||r.favorite)&&[r.title,r.category,r.ingredients,r.steps].join(' ').toLowerCase().includes(query.toLowerCase())&&(limit==null||(total!=null&&total<=limit))}
const api={ingredientText,ingredients,progress,reconcileSession,phases,quantity,friendly,scale,lines,steps,timeline,timing,duration,remaining,matches};if(typeof module!=='undefined')module.exports=api;root.Cookbook=api;
})(typeof window!=='undefined'?window:globalThis);
