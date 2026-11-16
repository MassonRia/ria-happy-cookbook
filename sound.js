/* Original synthesized kitchen sounds. No recordings or network dependencies. */
const Sound=(()=>{
 let prefs={enabled:true,volume:.3};try{prefs={...prefs,...JSON.parse(localStorage.getItem('ria-audio-v3')||'null')};if(localStorage.getItem('ria-sound-v2')==='false'&&!localStorage.getItem('ria-audio-v3'))prefs.enabled=false}catch{}
 prefs.volume=Math.min(1,Math.max(0,Number(prefs.volume)||0));
 let context=null,voices=[],last=0,lastPriority=0;
 const notes={tick:[[1800,0,.055]],tap:[[460,0,.09]],step:[[360,0,.14],[590,.055,.12]],add:[[1046.5,0,.2]],favorite:[[987.8,0,.23],[1318.5,.13,.3]],save:[[523.25,0,.22],[659.25,.1,.22],[783.99,.2,.22],[1046.5,.32,.4]],start:[[1568,0,.3]],timer:[[659.25,0,.27],[783.99,.18,.27],[1046.5,.36,.5]],shuffle:[[392,0,.08],[523,.06,.08],[440,.12,.08],[698,.18,.16]],celebrate:[[523.25,0,.22],[659.25,.12,.22],[783.99,.24,.24],[1046.5,.42,.35],[1318.5,.66,.55]]};
 const priority={tap:0,tick:1,step:1,add:1,open:1,favorite:2,save:2,start:2,shuffle:2,timer:3,celebrate:4};
 function unlock(){try{context??=new(window.AudioContext||window.webkitAudioContext)();if(context.state==='suspended')context.resume().catch(()=>{})}catch{}}
 function stop(){voices.forEach(node=>{try{node.stop()}catch{}});voices=[]}
 function play(kind='tap'){
  if(!prefs.enabled||prefs.volume===0||document.visibilityState!=='visible'||!context||context.state!=='running')return false;
  const now=performance.now(),rank=priority[kind]??1;if((now-last<90&&rank<=lastPriority)||(now-last<450&&rank<lastPriority))return false;
  stop();last=now;lastPriority=rank;const at=context.currentTime;
  if(kind==='open'){
   const buffer=context.createBuffer(1,Math.floor(context.sampleRate*.15),context.sampleRate),data=buffer.getChannelData(0);for(let i=0;i<data.length;i++)data[i]=(Math.random()*2-1)*Math.sin(Math.PI*i/data.length)*.22;
   const src=context.createBufferSource(),filter=context.createBiquadFilter(),gain=context.createGain();src.buffer=buffer;filter.type='lowpass';filter.frequency.value=1600;gain.gain.value=prefs.volume*.35;src.connect(filter);filter.connect(gain);gain.connect(context.destination);src.start();voices.push(src);
  }else for(const [hz,delay,length] of notes[kind]||notes.tap){const osc=context.createOscillator(),gain=context.createGain();osc.type='sine';osc.frequency.setValueAtTime(kind==='tap'||kind==='step'?hz*1.6:hz,at+delay);if(kind==='tap'||kind==='step')osc.frequency.exponentialRampToValueAtTime(hz*.65,at+delay+length);gain.gain.setValueAtTime(.0001,at+delay);gain.gain.exponentialRampToValueAtTime(Math.max(.0002,prefs.volume*.36),at+delay+.01);gain.gain.exponentialRampToValueAtTime(.0001,at+delay+length);osc.connect(gain);gain.connect(context.destination);osc.start(at+delay);osc.stop(at+delay+length+.02);voices.push(osc)}
  document.dispatchEvent(new CustomEvent('cookbook:sound',{detail:{kind,volume:prefs.volume}}));return true;
 }
 function save(){try{localStorage.setItem('ria-audio-v3',JSON.stringify(prefs))}catch{}sync()}
 function sync(){const b=document.getElementById('headerMute');if(b){b.setAttribute('aria-pressed',String(!prefs.enabled));b.setAttribute('aria-label',prefs.enabled?'Mute kitchen sounds':'Unmute kitchen sounds');b.textContent=prefs.enabled?'🍒 ♫':'🍒 ♫̸'}const v=document.getElementById('soundVolume');if(v)v.value=Math.round(prefs.volume*100);const output=document.getElementById('volumeValue');if(output)output.textContent=Math.round(prefs.volume*100)+'%'}
 function mount(){document.getElementById('soundControls').innerHTML='<button id="headerMute" class="cherry-sound" data-sound="none"></button><details class="sound-settings"><summary aria-label="Sound settings">Sound 🎀</summary><div><label for="soundVolume">Volume <output id="volumeValue"></output></label><input id="soundVolume" type="range" min="0" max="100" step="1"><button id="soundTest" data-sound="none">Try a sparkle ♫</button><small>Sounds play after a tap, when your device permits. No background music.</small></div></details>';document.getElementById('headerMute').onclick=()=>{unlock();prefs.enabled=!prefs.enabled;if(!prefs.enabled)stop();save();if(prefs.enabled)setTimeout(()=>play('favorite'),60)};document.getElementById('soundVolume').oninput=e=>{prefs.volume=Number(e.target.value)/100;save();if(prefs.volume===0)stop()};document.getElementById('soundTest').onclick=()=>{unlock();setTimeout(()=>play('favorite'),60)};sync()}
 document.addEventListener('pointerdown',unlock,{passive:true});document.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' ')unlock()});document.addEventListener('visibilitychange',()=>{if(document.visibilityState!=='visible')stop()});
 return {mount,unlock,play,stop,get enabled(){return prefs.enabled},set enabled(v){prefs.enabled=!!v;if(!v)stop();save()},get volume(){return prefs.volume}};
})();
