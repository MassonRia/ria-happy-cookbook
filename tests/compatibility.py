"""Legacy IDB upgrade, media safety, stable checklist IDs and atomic restore checks."""
from playwright.sync_api import sync_playwright,expect
from pathlib import Path
import json,os,shutil,tempfile,zipfile
BASE=os.environ.get('COOKBOOK_URL','http://127.0.0.1:4173');ARTIFACTS=Path(tempfile.mkdtemp(prefix='ria-compat-'))
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium') or shutil.which('google-chrome'),headless=True,args=['--no-sandbox']);c=b.new_context();p=c.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 # Seed the exact original database schema on this origin before loading the new code.
 p.goto(BASE+'/legacy-not-found.html');p.evaluate('''async()=>{await new Promise((resolve,reject)=>{const req=indexedDB.open('private-cookbook-v1',1);req.onupgradeneeded=()=>req.result.createObjectStore('recipes',{keyPath:'id'});req.onsuccess=()=>{const db=req.result,tx=db.transaction('recipes','readwrite');tx.objectStore('recipes').put({id:'legacy',title:'Ria’s old cake',category:'Dessert',favorite:true,servings:'4 servings',ingredients:'2 cups flour\\n1 egg',steps:'Mix\\nBake',time:'about 20 minutes',notes:'Keep me',photo:new Blob(['photo bytes'],{type:'image/png'}),video:new Blob(['video bytes'],{type:'video/mp4'})});tx.oncomplete=()=>{db.close();resolve()};tx.onerror=()=>reject(tx.error)}});localStorage.setItem('ria-session-legacy',JSON.stringify({checked:{0:true},done:{1:true},servings:5,ingredients:{1:'2 small eggs'}}))}''')
 p.goto(BASE);p.wait_for_function('!!db && !document.getElementById("add").disabled');p.locator('.card-button').click();expect(p.locator('#progressLabel')).to_have_text('50% complete');expect(p.locator('#ingredientList')).to_contain_text('2 small eggs');assert p.locator('[data-step="1"]').is_checked();assert p.evaluate('db.version')==2;assert p.evaluate('localStorage.getItem("ria-session-legacy")') is None
 p.locator('#edit').click();p.get_by_role('button',name='Move ingredient 2 up',exact=True).click();p.locator('#recipeTitle').fill('Ria’s preserved cake');p.get_by_role('button',name='Save recipe 🎀').click();expect(p.locator('#startCooking')).to_be_visible();expect(p.locator('#progressLabel')).to_have_text('50% complete');assert not p.locator('[data-ingredient]').nth(0).is_checked();assert p.locator('[data-ingredient]').nth(1).is_checked();expect(p.locator('#ingredientList')).to_contain_text('2 small eggs');assert p.evaluate('(async()=>{const r=await get("legacy");return r.notes==="Keep me"&&r.favorite&&r.category==="Dessert"&&await r.photo.text()==="photo bytes"&&await r.video.text()==="video bytes"})()')
 p.locator('#back').click()
 with p.expect_download() as dl:p.locator('#backup').click()
 backup=ARTIFACTS/'legacy.zip';dl.value.save_as(str(backup))
 with zipfile.ZipFile(backup) as z:
  assert z.read('media/legacy-photo.img')==b'photo bytes';assert z.read('media/legacy-video.video')==b'video bytes';data=json.loads(z.read('recipes.json'));assert data['recipes'][0]['time']=='about 20 minutes';assert data['sessions'][0]['checked']['legacy-ingredient-0']
 # Late malformed records must fail before committing any recipe or progress changes.
 broken=ARTIFACTS/'invalid.zip'
 with zipfile.ZipFile(broken,'w') as z:z.writestr('recipes.json',json.dumps({'format':'private-cookbook-v1','recipes':[{'id':'new','title':'Should not import'},{'id':123,'title':'invalid'}]}))
 p.on('dialog',lambda d:d.accept());p.locator('#backupFile').set_input_files(str(broken));p.wait_for_timeout(250);expect(p.locator('.tile')).to_have_count(1);expect(p.locator('.tile')).to_contain_text('Ria’s preserved cake')
 # Old-format backups without sessions or structured fields still restore.
 old=ARTIFACTS/'old.zip'
 with zipfile.ZipFile(old,'w') as z:z.writestr('recipes.json',json.dumps({'format':'private-cookbook-v1','recipes':[{'id':'old-backup','title':'Old ZIP soup','ingredients':'1 cup water','steps':'Simmer','favorite':False}]}))
 p.locator('#backupFile').set_input_files(str(old));expect(p.locator('.tile')).to_have_count(2)
 # No IDB/schema/media/corrupt restore page errors. Invalid media fixtures are byte-preservation only.
 assert not errors,errors
 print('PASS: v1→v2 database upgrade, localStorage→IDB session migration, ingredient reorder retains checks, edit retains metadata/photo/video bytes, old ZIP import, atomic invalid-backup rejection');b.close()
