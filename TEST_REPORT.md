# Cooking Mode verification report

## Passed

- Nine Node calculation tests, including combined ingredient + step completion (the specified 6 ingredients / 4 steps example produces 50%), immutable fraction scaling, structured ingredient text, stable identity reconciliation, required-rest elapsed totals, explicit overlap scheduling and deadline-based countdowns.
- Chromium touch/mobile end-to-end tests at 390 × 844: structured ingredient add/edit/reorder, quantity/unit/preparation notes and section headings; individually stored steps; serving scaling and manual overrides; ingredient ready counter; step check/uncheck in any order; immediate combined progress.
- Dedicated Cooking Mode, Previous/Next navigation, step picker, Show all steps, and local persistence after reload.
- Multiple timers, pause/resume/reset and completion; serving-time estimate and timeline access in Cooking Mode.
- Cooking sessions stored in IndexedDB and included in ZIP exports. Import into an empty browser restores 50% progress, manual overrides, ingredient checks, step checks and photo bytes. Matching recipe IDs import as restored copies without overwriting existing recipes.
- Once-per-session completion screen; uncheck/recheck and reload do not retrigger celebration. Confirmation can cancel reset; confirmed reset and Cook Again leave recipe records unchanged.
- All 11 original Web Audio sound graphs schedule without errors after user interaction. Mute and volume persist, default volume is 30%, and mute suppresses sound scheduling. No external sound files or background music.
- Full offline reload, new recipe creation, checklist progress, completion celebration and reset after service worker caching.
- Layout has no horizontal page overflow at widths 320, 390, 768 and 1440. Mobile Cooking Mode screenshot visually inspected. Reduced-motion mode suppresses visible sparkle effects and progress/checkmark animations.
- Original version-1 IndexedDB database upgrades to version 2 without losing recipe records. Older localStorage checklists migrate to IndexedDB. Recipe editing and ingredient reordering retain the correct checks, notes, favorite/category metadata and original photo/video bytes.
- Original-format backups without structured ingredients or sessions still import. Malformed backup rejection is atomic and leaves existing records intact.
- JavaScript syntax checks pass; no uncaught page errors in the main mobile browser test or compatibility test.

- Update lifecycle test passed: downloaded new release detected; banner shown; unsaved recipe edits blocked activation; explicit apply/reload retained cooking checks and a running timer; updated app reopened offline.
- Pages packaging script ran successfully and generated an asset-content-based cache identifier.

## Limits and device checks

These checks used Chromium on Linux with mobile/touch emulation, not a physical iPhone or macOS Safari. Web Audio scheduling was exercised; physical speaker output was not listened to. iPhone installation, silent-mode behavior, Safari storage and native file pickers still need a real-device check. GitHub Pages deployed successfully at https://massonria.github.io/ria-happy-cookbook/; workflow run 43801158761 passed its calculation tests, packaging and deployment.

On your iPhone and Mac, open the deployed HTTPS app, test New Recipe, a short audible timer while visible, backup/restore and offline reopen. iOS can suspend background/locked/closed-app audio and timers: the app does not promise alerts in those states. Use the native Clock app for reliable background alarms.

The previous package's GitHub Pages repository-subpath offline check passed; the updated package uses the same relative asset paths and adds the four new JavaScript modules to the versioned service worker cache.

## Reproduce

From the app root:

```sh
node --test tests/core.test.cjs
python3 -m http.server 4173
```

In a separate terminal with Python Playwright and Chromium available:

```sh
python3 tests/browser.py
python3 tests/compatibility.py
```

`CHROMIUM_PATH` selects a browser executable. `COOKBOOK_URL` selects a different base URL. Test data uses isolated browser storage and temporary directories; it does not alter your personal cookbook.
