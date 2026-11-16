"""End-to-end checks. Run a static server first: python3 -m http.server 4173."""
from playwright.sync_api import sync_playwright, expect
from pathlib import Path
import json, os, shutil, tempfile, zipfile
ARTIFACTS=Path(tempfile.mkdtemp(prefix='ria-cookbook-test-'))
BROWSER=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium') or shutil.which('google-chrome')
BASE=os.environ.get('COOKBOOK_URL','http://127.0.0.1:4173')
ROOT=Path(__file__).resolve().parent.parent
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path=BROWSER,headless=True,args=['--no-sandbox'])
 c=b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,accept_downloads=True)
 p=c.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)));p.goto(BASE);p.wait_for_function('!!db');p.evaluate("window.heard=[];document.addEventListener('cookbook:sound',e=>heard.push(e.detail.kind))")
 expect(p.get_by_text('Welcome, Ria Masson!')).to_be_visible();assert p.locator('#soundVolume').input_value()=='30'
 p.locator('#add').click();p.locator('#recipeTitle').fill('Cherry celebration cake');p.locator('#recipeCategory').fill('Dessert');p.locator('#baseServings').fill('4')
 values=[('Flour','1 ½','cups','sifted','Cake'),('Eggs','2','','beaten','Cake'),('Milk','½','cup','','Cake'),('Sugar','1','cup','','Frosting'),('Cream','¼','cup','chilled','Frosting'),('Cherries','6','','halved','Toppings')]
 for i,fields in enumerate(values):
  p.locator('#addIngredient').click()
  row=p.locator('.ingredient-editor-row').nth(i)
  for key,value in zip(['name','quantity','unit','preparation','section'],fields):row.locator('[data-field='+key+']').fill(value)
 # Reorder by real controls, preserving all ingredient fields.
 p.get_by_role('button',name='Move ingredient 6 up',exact=True).click();p.get_by_role('button',name='Move ingredient 5 down',exact=True).click()
 p.locator('#recipeSteps').fill('Mix the batter\nBake gently\nRest the cake\nAdd the frosting')
 for i,n in enumerate(['10','20','25','5']):p.locator('.step-config .minutes').nth(i).fill(n)
 p.locator('.step-config .phase').nth(1).select_option('bake');p.locator('.step-config .phase').nth(2).select_option('rest');p.locator('.step-config .hands').nth(0).check();p.locator('#photo').set_input_files(str(ROOT/'icon-192.png'))
 p.get_by_role('button',name='Save recipe 🎀').click();expect(p.locator('#startCooking')).to_be_visible();expect(p.locator('.total')).to_contain_text('1h');expect(p.locator('.ingredient-group')).to_have_count(3)
 # Per-recipe structured storage, preserving quantities and numbered steps.
 saved=p.evaluate('(async()=>{const r=(await all())[0];return {items:r.ingredientItems,steps:r.stepItems,id:r.id}})()');rid=saved['id'];assert len(saved['items'])==6 and len(saved['steps'])==4 and saved['items'][0]['preparation']=='sifted'
 p.locator('#plusServings').click();expect(p.locator('#ingredientList')).to_contain_text('1 ⅞ cups Flour — sifted');expect(p.locator('#ingredientList')).to_contain_text('Original: 1 ½ cups Flour — sifted')
 p.locator('#ingredientList summary').nth(1).click();p.locator('.override').nth(1).fill('3 small eggs');p.locator('.override').nth(1).press('Tab');expect(p.locator('#ingredientList')).to_contain_text('3 small eggs')
 for i in range(3):p.locator('[data-ingredient]').nth(i).check();p.wait_for_timeout(110)
 p.locator('[data-step="0"]').check();p.wait_for_timeout(150);p.locator('[data-step="2"]').check();expect(p.locator('#progressLabel')).to_have_text('50% complete');expect(p.locator('#ingredientCount')).to_have_text('3 of 6 ingredients ready!');assert p.locator('#cookingProgress').get_attribute('value')=='50'
 # Dedicated cooking mode, Previous/Next and any-order selection/unchecking.
 p.locator('#startCooking').click();expect(p.locator('#detail')).to_have_class('cooking-mode');expect(p.locator('#stepList .cooking-step:visible')).to_have_count(1);p.locator('#nextStep').click();assert p.locator('#stepPicker').input_value()=='1';p.locator('#previousStep').click();assert p.locator('#stepPicker').input_value()=='0';p.locator('#stepPicker').select_option('2');p.locator('[data-step="2"]').uncheck();expect(p.locator('#progressLabel')).to_have_text('40% complete');p.locator('[data-step="2"]').check();expect(p.locator('#progressLabel')).to_have_text('50% complete');p.locator('#showAllSteps').click()
 # Timers and plan remain available within cooking mode.
 p.locator('#cookingPlan summary').click();p.locator('#serveAt').fill('2030-01-01T18:00');expect(p.locator('#startEstimate')).to_contain_text('start:');assert '17:00' in p.locator('#startEstimate').inner_text() or '5:00' in p.locator('#startEstimate').inner_text();p.locator('#timerMinutes0').fill('0.03');p.locator('[data-timer-start="0"]').click();p.locator('#timerMinutes1').fill('2');p.locator('[data-timer-start="1"]').click();expect(p.locator('.timer-card')).to_have_count(2);p.locator('[data-action=toggle]').nth(1).click();expect(p.locator('.timer-card').nth(1)).to_contain_text('Paused');p.locator('[data-action=toggle]').nth(1).click();p.wait_for_timeout(2100);expect(p.locator('.timer-card').nth(0)).to_contain_text('Ready!');p.locator('[data-action=reset]').nth(0).click();expect(p.locator('.timer-card').nth(0)).to_contain_text('Paused')
 p.reload();p.wait_for_function('!!db');p.locator('.card-button').click();expect(p.locator('#progressLabel')).to_have_text('50% complete');expect(p.locator('#detail')).to_have_class('cooking-mode');assert p.locator('[data-ingredient]').nth(0).is_checked();expect(p.locator('#ingredientList')).to_contain_text('3 small eggs')
 assert p.evaluate('db.objectStoreNames.contains("cookingSessions")');assert p.evaluate('(async()=>{await sessionWrites;return (await sessionRequest("readonly",s=>s.get(current))).schema})()')==2
 # Progress included in exported ZIP and restored on a separate empty device.
 p.locator('#back').click()
 with p.expect_download() as dl:p.locator('#backup').click()
 backup=ARTIFACTS/'progress-backup.zip';dl.value.save_as(str(backup))
 with zipfile.ZipFile(backup) as z:
  data=json.loads(z.read('recipes.json'));assert len(data['sessions'])==1 and len(data['sessions'][0]['checked'])==3 and len(data['sessions'][0]['done'])==2
  assert z.read('media/'+rid+'-photo.img')==(ROOT/'icon-192.png').read_bytes()
 c2=b.new_context();q=c2.new_page();q.goto(BASE);q.wait_for_function('!!db');q.on('dialog',lambda d:d.accept());q.locator('#backupFile').set_input_files(str(backup));expect(q.locator('.tile')).to_have_count(1);q.locator('.card-button').click();expect(q.locator('#progressLabel')).to_have_text('50% complete');expect(q.locator('.hero')).not_to_be_visible();q.locator('#startCooking').click();expect(q.locator('.hero')).to_be_visible();q.locator('#back').click();q.locator('#backupFile').set_input_files(str(backup));expect(q.locator('.tile')).to_have_count(2);expect(q.locator('.card-button').filter(has_text='restored copy')).to_have_count(1)
 # Celebration once per session; persisted flag prevents replay after reload or recheck.
 p.locator('.card-button').click()
 for i in range(3,6):p.locator('[data-ingredient]').nth(i).check()
 expect(p.locator('#ingredientsReady')).to_have_text('Everything’s ready, Chef Ria! 🍓');expect(p.locator('#progressLabel')).to_have_text('80% complete')
 p.locator('[data-step="1"]').check();p.locator('[data-step="3"]').check();expect(p.get_by_text('Yay, Chef Ria! You did it! 🍒🎉')).to_be_visible();expect(p.locator('#progressLabel')).to_have_text('100% complete');p.locator('#reviewCooking').click();p.locator('[data-step="3"]').uncheck();p.locator('[data-step="3"]').check();expect(p.locator('#completionScreen')).not_to_be_visible();p.reload();p.wait_for_function('!!db');p.locator('.card-button').click();expect(p.locator('#completionScreen')).not_to_be_visible();expect(p.locator('#progressLabel')).to_have_text('100% complete')
 # Reset can be cancelled and never changes the recipe.
 before=p.evaluate('(async()=>{const r=await get(current);return JSON.stringify({...r,photo:!!r.photo})})()');p.once('dialog',lambda d:d.dismiss());p.locator('#resetProgress').click();expect(p.locator('#progressLabel')).to_have_text('100% complete');p.once('dialog',lambda d:d.accept());p.locator('#resetProgress').click();expect(p.locator('#progressLabel')).to_have_text('0% complete');after=p.evaluate('(async()=>{const r=await get(current);return JSON.stringify({...r,photo:!!r.photo})})()');assert before==after
 # Sound settings work globally, persist, and volume zero/mute silences sound calls.
 p.locator('#headerMute').click();assert p.locator('#headerMute').get_attribute('aria-pressed')=='true';assert p.evaluate('Sound.play("tick")')==False;p.reload();p.wait_for_function('!!db');assert p.locator('#headerMute').get_attribute('aria-pressed')=='true';p.locator('#headerMute').click();p.locator('.sound-settings summary').click();p.locator('#soundVolume').fill('45');assert p.evaluate('Sound.volume')==.45;p.locator('#soundTest').click();p.wait_for_timeout(150);p.reload();p.wait_for_function('!!db');assert p.locator('#soundVolume').input_value()=='45'
 # Verify every original sound graph schedules without throwing after interaction.
 p.locator('#add').click();p.wait_for_timeout(500);p.evaluate('window.soundChecks=[];document.addEventListener("cookbook:sound",e=>soundChecks.push(e.detail.kind))')
 for kind in ['tap','tick','step','add','open','favorite','save','start','timer','shuffle','celebrate']:
  p.evaluate('(kind)=>Sound.play(kind)',kind);p.wait_for_timeout(600)
 assert len(p.evaluate('soundChecks'))==11
 p.once('dialog',lambda d:d.accept());p.locator('#cancel').click()
 # Filters, responsive widths, reduced motion and full offline reload/create.
 p.locator('[data-limit="30"]').click();expect(p.locator('.tile')).to_have_count(0);p.locator('[data-limit="60"]').click();expect(p.locator('.tile')).to_have_count(1);p.locator('#search').fill('nonexistent');expect(p.locator('.tile')).to_have_count(0);p.locator('#search').fill('');p.locator('[data-limit=""]').click()
 p.evaluate('navigator.serviceWorker.ready');p.reload();p.wait_for_function('navigator.serviceWorker.controller !== null');c.set_offline(True);p.reload();p.wait_for_function('!!db');p.locator('#add').click();p.locator('#recipeTitle').fill('Offline toast');p.locator('#addIngredient').click();p.locator('[data-field=name]').fill('Toast');p.locator('#recipeSteps').fill('Toast until golden');p.get_by_role('button',name='Save recipe 🎀').click();expect(p.locator('#startCooking')).to_be_visible();p.locator('[data-ingredient]').check();p.locator('[data-step="0"]').check();expect(p.locator('#completionScreen')).to_be_visible();p.once('dialog',lambda d:d.accept());p.locator('#cookAgain').click();expect(p.locator('#progressLabel')).to_have_text('0% complete');expect(p.locator('#detail')).to_have_class('cooking-mode');p.locator('#back').click();expect(p.locator('.tile')).to_have_count(2)
 for width in [320,390,768,1440]:
  p.set_viewport_size({'width':width,'height':900});assert p.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'Overflow {width}'
 p.emulate_media(reduced_motion='reduce');p.locator('.card-button').filter(has_text='Offline toast').click();p.locator('[data-ingredient]').check();assert p.locator('.sparkle-burst:visible').count()==0
 p.set_viewport_size({'width':390,'height':844});p.screenshot(path=str(ARTIFACTS/'cooking-mode.png'),full_page=True)
 assert not errors,errors
 print(json.dumps({'result':'PASS','browser':'Chromium mobile viewport','checks':['structured ingredient add/edit/reorder/sections','individual stored steps','servings/manual override','50% combined progress','Cooking Mode and Previous/Next/any-order checks','IndexedDB reload persistence','timer concurrency/pause/resume/reset/completion','progress and photo backup restore','collision copies preserve existing recipes','once-per-session celebration and safe reset','11 original sound graphs and saved mute/volume','time/search filtering','offline reload/create/celebration','responsive 320/390/768/1440','reduced motion'],'page_errors':errors,'artifacts':str(ARTIFACTS)},indent=2));b.close()
