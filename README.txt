============================================================
  XenForo Auto Translate
  Powered by DeepL API
============================================================

STEP 1 — DOWNLOAD THE LANGUAGE FILE FROM XENFORO
-------------------------------------------------
You need to export the English language XML file from your
XenForo admin panel first.

  a) Log in to your XenForo Admin Panel
  b) Go to:  Appearance > Languages
  c) Find "English (US)" in the list
  d) Click the download icon (arrow pointing down) next to it
  e) Save the file into this folder
     The file will be named something like:
       language-English-(US)-XF.xml


STEP 2 — GET A FREE DEEPL API KEY (first run only)
----------------------------------------------------
  - Go to: https://www.deepl.com/pro-api
  - Sign up and choose the Free plan
  - Copy your API key from the account dashboard
  - Free plan includes 500,000 characters/month
    (enough for a full XenForo language file)

  Your key is saved automatically after the first run —
  you will never be asked again.


STEP 3 — RUN THE TRANSLATOR
----------------------------
  Double-click  run.bat

  On first run:
    1. Enter your DeepL API key
    2. Select the target language from the list
    3. Select the XML file you downloaded in Step 1
    4. Wait for translation to finish
       (roughly 5–15 minutes depending on connection)

  The translated XML file will appear in this folder.


STEP 4 — IMPORT INTO XENFORO
------------------------------
  a) Go to your XenForo Admin Panel
  b) Navigate to:  Appearance > Languages
  c) Click "Import" (top right corner)
  d) Choose the output XML file from this folder
     (e.g. language-Turkish-XF.xml)
  e) Click "Import"

  Optional — set as the default language for all users:
    Click the pencil icon next to the language
    Check "Set as default" and save.

  Optional — allow users to switch language themselves:
    Setup > Options > User Registration
    Enable "Allow users to change language"


------------------------------------------------------------

COMMAND LINE OPTIONS
--------------------
  python xf_translate.py                  (interactive mode)
  python xf_translate.py myfile.xml       (specify a file)
  python xf_translate.py --reset-key      (change saved API key)


NOTES
-----
- Supports all 30 DeepL target languages
- XenForo variables like {username} and {count} are never translated
- HTML tags inside phrases are preserved
- Progress is auto-saved — if interrupted, re-run to continue from
  where it left off
- Each target language has its own separate progress file


FILES IN THIS FOLDER
--------------------
  xf_translate.py        — Main Python script
  run.bat                — Windows launcher
  README.txt             — This file

  language-*-XF.xml      — Input / output language XML files
  .progress_*.json       — Temporary files (auto-deleted when done)


TROUBLESHOOTING
---------------
"deepl package not found"
  -> Run:  python -m pip install deepl

"Invalid API key"
  -> Double-check your key at deepl.com/account
  -> Or run with --reset-key to enter a new one

"Quota exceeded"
  -> Your 500,000 char/month free limit was reached
  -> Progress is saved; re-run next month to continue

"The uploaded file is not a valid language XML"  (XenForo error)
  -> The output file may be incomplete; re-run the translation

"No XML files found" (in the tool)
  -> Make sure you copied the exported XML file into this folder

============================================================
