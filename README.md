# Ria’s Happy Cookbook 🍒

An offline-first recipe box for Ria Masson, with vintage pink gingham, strawberries, cherries and bows. No account, subscription, build tools, server database, remote fonts, analytics or automatic uploads.

## Publish this repository

The app source is now maintained in **MassonRia/ria-happy-cookbook**. The repository remains private. This does not by itself create a working website or make a Pages website access-restricted.

1. **Export a ZIP backup from your old downloaded cookbook before moving.** The old `file:///Users/.../index.html` address is a separate storage location and cannot receive updates from GitHub. Your locally stored recipes are not in this source repository.
2. Open this repository’s **Settings → Pages**. For this private repository, GitHub Pages requires an eligible paid GitHub plan. If GitHub requests an upgrade, you can keep the repository private and choose another hosting service instead; the app has not changed your privacy settings.
3. Under **Build and deployment**, choose **GitHub Actions**. The included **Publish cookbook** workflow tests and packages the static app and deploys it. Run it from **Actions → Publish cookbook → Run workflow** once Pages is enabled. Subsequent pushes to `main` trigger it automatically.
4. After a successful deployment, open the exact URL GitHub reports. The usual project URL is `https://massonria.github.io/ria-happy-cookbook/`, but it is not live until deployment succeeds. Pages websites are generally public even when their source repository is private. Use access-controlled hosting if only you should be able to open the website.
5. Open the published HTTPS address, restore your backup, and install it using the iPhone instructions below. Do not continue opening the old Downloads folder.

The connection used for this setup can write repository code but cannot currently access Pages administration. Hosting availability and enablement must be checked in your GitHub account. The app is a dependency-free static site, so it can also be hosted by a service with private access controls; no paid backend is required by the app itself.

## Future updates—no Library checking

Once hosting is enabled, publishing a commit to `main` runs the Pages workflow. Its build generates a cache version from the app’s actual content, so every changed release can be detected without manually renaming caches.

While online, the installed cookbook checks for a new release when it opens, when you return to it, when connectivity returns, and about once a minute while visible. A **“A fresh cookbook is ready 🍒 / Update cookbook”** banner appears after a release downloads. Tap **Update cookbook** to activate it and reload. It saves cooking progress first and retains timer deadlines. Unsaved recipe edits block the update until you save or cancel them; it does not interrupt cooking automatically. **Later** dismisses the prompt for now. iOS background restrictions still apply: update checks happen when the app is running, not while it is closed.

Changes made only in a chat or ZIP do not publish themselves. The changed files must be committed to this repository and successfully deployed. Once the GitHub connection and hosting are available, future development can use this same repository and permanent web address.

## Install on iPhone

1. Open the GitHub Pages HTTPS address in **Safari**, not the Files app or an in-app preview.
2. Tap **Share → Add to Home Screen** (or **More → Share** first, depending on iOS). Keep **Open as Web App** enabled if shown, then tap **Add**.
3. Launch the cookbook from its Home Screen icon while online. Wait for “Your cookbook is ready for offline use”. Then test airplane mode.
4. Add and save a recipe from the installed app. Safari tabs and the installed app can use separate storage on some iOS versions: use ZIP backup/restore to move recipes if needed.

## Use on Mac

Open the same HTTPS address in Safari or Chrome. On supported macOS versions, use Safari **File → Add to Dock**; Chrome offers an install option in its address bar or app menu. A normal browser tab also works. Open online once before relying on offline use.

## Privacy, backup and device transfers

Your **recipe data is private to this browser/app storage on this device**. GitHub Pages publishes the app code, not your saved recipes. The website has no login gate: anyone with its URL can load an empty cookbook of their own. This is not encrypted storage or access-controlled private hosting. Do not save sensitive information on shared devices.

- **Save Backup** downloads a ZIP containing recipes and attached photos/videos. Save to iCloud Drive and keep an independent second copy. Backups contain private data: never commit them to GitHub.
- On another device, open the cookbook and use **Restore Backup** to select the ZIP. Confirm to import. Existing recipes are preserved: matching IDs become separate recipes labeled “(restored copy)”. Recipes and their backed-up cooking progress are validated and committed together in a single transaction; an invalid backup does not partially change the cookbook.
- This is manual transfer, **not automatic iCloud sync**. Export before moving devices, changing the hosted URL, deleting the app or clearing Safari data.
- Recipes, source serving counts, structured ingredient sections/quantities/units/preparation notes, individual steps, timing fields, attached media and cooking session progress are backed up. Sessions include ingredient/step checkmarks, serving adjustments, manual ingredient overrides and the once-per-session celebration flag. Running timers and device sound preferences are not transferred in backups.
- Browser/iOS storage can be cleared or evicted, even for installed apps. Large videos can exceed quota. A save only succeeds when the database transaction commits; failures appear on screen.
- Original `private-cookbook-v1` ZIP backups remain supported. Existing IndexedDB records at the **same origin/browser storage** are retained. Moving to a new GitHub Pages origin requires backup/restore.
- Linked videos need internet. Videos/photos attached as files stay on your device and work offline after saving.

## Cooking with your cookbook

### Recipes, ingredients and servings

Use **＋ New Recipe**, give the recipe a name, and tap **＋ Add ingredient** for each ingredient. Enter its name, quantity, unit, preparation note and section (Cake, Frosting, Toppings…). Edit any field, remove a row, or reorder it with the accessible **↑ / ↓** buttons—no dragging required on iPhone. Add one instruction per line; on save, every instruction is stored as an individual step with a stable ID. Attach a photo or cooking video if you wish. Categories are free-form. Favorite any recipe to find it again. **Surprise Me** chooses a saved recipe matching your current search and filters.

Set original servings as a positive number, e.g. `4`. In a saved recipe, use **− / ＋**, type a count, or reset to **Original**. Quantities starting with whole numbers, decimals, slash fractions or common Unicode fractions scale automatically. Originals remain visible under every ingredient. Friendly fractions are used where close; other amounts use up to two decimals. Ranges (`1–2 lemons`), “salt to taste” and other unmeasured items remain unchanged. Open **Adjust ingredient** to enter a practical amount for eggs, leavening or seasonings. Manual overrides never edit the source recipe. Changing servings clears those overrides; checkmarks remain.

Temperatures and timings do not automatically scale with servings. Pan size, batch size and safe doneness need your judgment.

Check ingredients as you gather them and mark completed steps. Each ingredient has a 44px pink checkbox, a ready counter and an all-ready strawberry message. Ingredient rows retain their stable IDs when reordered, so checks stay with the correct ingredient.

Tap **Start Cooking** for a focused cooking view. At the top, overall progress includes **both ingredients and cooking steps**, with equal weight per checkbox: 3 of 6 ingredients + 2 of 4 steps = 50%. The bar and both counts update immediately. Use **Previous Step**, **Next Step**, the step picker, or **Show all steps** to move around and check/uncheck steps in any order. Current-step selection does not mark a step complete. Serving controls, ingredient overrides, timers and the expandable plan/timeline remain available in Cooking Mode.

Progress is saved separately per recipe in the IndexedDB `cookingSessions` store and survives reloads and closing the app. Existing older localStorage progress migrates automatically after the database upgrades from version 1 to version 2, without deleting recipes or media. Recipe edits preserve checks for retained ingredient and step IDs; newly added or changed instruction text gets a new step ID. Reordered ingredient rows preserve their IDs.

When all ingredients and steps are checked, **“Yay, Chef Ria! You did it! 🍒🎉”** appears with a celebration melody, hearts, strawberries and soft confetti. It triggers only once per cooking session, including after reload or unchecking/rechecking. Use **Back to My Recipes**, **Review my recipe**, or **Cook Again**. **Cook Again** and **Reset Cooking Session** require confirmation and clear ingredient/step checks and the celebration flag; they never modify the recipe or delete media. Serving adjustments and running timers stay. Reduced-motion preferences turn off checkmark, sparkle, confetti and bar animations.

### Timeframes and timeline

Two supported ways to enter a known total:

1. **Time every step**, including `0` for instant actions. Choose each step's phase (prep, cook, bake, rest/chill or marinate) and whether it is hands-on work. The total is calculated from the step schedule. Select **Alongside step N** only for intentional overlap: it starts at that earlier step's start. Otherwise each step waits until **all** earlier steps have ended. Check timing metadata whenever you reorder steps. Timers remain independent and are not automatically launched by the timeline.
2. If step durations are incomplete, enter whole-recipe phase minutes and check **These phases include the complete elapsed time**. Prep + cook + bake + rest/chill + marinate are summed sequentially. Active minutes are informational and are not added again. Leave unused phases blank. Phase-based timelines cannot infer overlap; time every step to describe overlapping work.

Complete step timing takes precedence over whole-recipe phase fields. Untimed recipes show **Time not set**. Old free-text timing notes are preserved but are not guessed into a total. Unused phases show **N/A**; unknown phases show a dash. Active time is the sum of steps marked hands-on, or your explicit active minutes in phase mode.

The visual timeline shows elapsed offsets. Choose a desired serving date/time for **estimated start = serving time − total elapsed**. Estimates use your device's local time. A past start is flagged. It does not schedule an alarm or silently assume steps can overlap.

### Individual kitchen timers and sound

Each cooking step has an optional minutes input and **Start timer**. Several step timers, even from different recipes, can run together in the kitchen timer panel. Each supports **Pause**, **Resume**, **Reset** (restores the original countdown, paused), **Start again** after completion, and **Dismiss**. Timer state persists locally. Reset or dismiss timers before repeating an edited recipe if step numbers changed.

The countdown uses an absolute deadline, so it catches up when the app is reopened. The original Web Audio effects all work offline: soft button bubble, delicate ingredient tick, bubbly step pop, cheerful ingredient plink, gentle recipe page flip, sparkly favorite chime, magical save melody, tiny timer bell, three-note timer-completion chime, playful Surprise Me shuffle, and a happy completion melody. There are no remote sound dependencies or background music.

Use the **cherry mute button** in the header, or open **Sound 🎀** for the volume slider and a test button. Volume defaults to 30%; mute and volume preferences persist on this device. Short sound bursts are prioritized and do not pile up; quick taps can be quiet while a more important sound plays. A tap/keyboard interaction must unlock audio first. Device volume, silent mode and browser policies can still prevent sound. Muting or backgrounding the app stops its current sound.

**iPhone PWA limitation:** iOS can suspend JavaScript and audio in the background, on screen lock, or when the app is closed. This app does **not** promise background/closed-app alerts. Completion sounds are attempted only while the app is visible; reopening updates overdue timers to Ready. Keep the app open or use the native iPhone Clock app for reliable background alarms. Desktop sleep also delays in-app alerts.

### What Do We Have Time For? ⏰

Pick **15, 30, 45 or 60 min**, enter custom minutes, or return to **Any time**. These are maximum total elapsed times including required rest/chill and marinating, using explicit overlaps only. Time filters combine with category, favorites and search. Recipe cards show duration. Recipes with unknown total are excluded from duration-limited results. Serving changes do not change time estimates.

## Updating the app safely

Export backups regularly. Keep the same hosted origin and path to retain browser storage. Use the update banner described above; recipe data is stored separately from cached app files. Never clear website data as a routine update step. If updating manually without the workflow, change the service worker `CACHE` value whenever application assets change.

## Local development and tests

No installation or build step is required. Serve over localhost; do not double-click the HTML file:

```sh
python3 -m http.server 4173
```

Open `http://localhost:4173`. Service workers work on localhost and HTTPS, not arbitrary plain HTTP phone LAN addresses.

Run the calculation tests with Node 18+:

```sh
node --test tests/core.test.cjs
```

See `TEST_REPORT.md` for actual verification and remaining device checks. The browser test is included for developers and requires Python Playwright and Chromium. It only creates test recipes in an isolated browser context.
