/* Published releases are checked online; updates never interrupt an editor/session. */
(()=>{
 if(!('serviceWorker'in navigator)||!(location.protocol==='https:'||['localhost','127.0.0.1'].includes(location.hostname)))return;
 let registration,applying=false;
 const banner=()=>{if(registration?.waiting)$('updateBanner').classList.remove('hidden')};
 async function check(){if(registration&&navigator.onLine&&document.visibilityState==='visible'){try{await registration.update();banner()}catch{/* Offline use remains available. */}}}
 navigator.serviceWorker.addEventListener('controllerchange',()=>{if(applying)location.reload()});
 $('laterUpdate').onclick=()=>$('updateBanner').classList.add('hidden');
 $('applyUpdate').onclick=async()=>{
  if(!$('editor').classList.contains('hidden')){toast('Save your recipe or cancel editing before applying this update.');return}
  if(!registration?.waiting){$('updateBanner').classList.add('hidden');return}
  $('applyUpdate').disabled=true;
  try{await sessionWrites;if(current&&viewRecipe)await sessionRequest('readwrite',s=>s.put({...structuredClone(session),id:current}));saveLocal('ria-timers-v2',timers);applying=true;registration.waiting.postMessage({type:'APPLY_UPDATE'});setTimeout(()=>{if(applying){$('applyUpdate').disabled=false;toast('The update is taking longer than expected. Close and reopen the cookbook when convenient.')}},15000)}catch{applying=false;$('applyUpdate').disabled=false;toast('Could not save progress. Finish saving before updating.')}
 };
 window.addEventListener('load',async()=>{try{registration=await navigator.serviceWorker.register('./sw.js',{updateViaCache:'none'});const watch=worker=>{if(!worker)return;worker.addEventListener('statechange',()=>{if(worker.state==='installed'&&navigator.serviceWorker.controller)banner()})};watch(registration.installing);registration.addEventListener('updatefound',()=>watch(registration.installing));await navigator.serviceWorker.ready;toast('Your cookbook is ready for offline use 🍒');banner();check()}catch{toast('Offline setup failed. Reopen online before relying on offline mode.')}});
 document.addEventListener('visibilitychange',check);window.addEventListener('online',check);setInterval(check,60000);
})();
