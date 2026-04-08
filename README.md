# XenForo Auto Translate

Automatically translate XenForo 2.x language files into any language using the **DeepL API**.

Supports all 30 DeepL target languages including Turkish, German, French, Spanish, Japanese, and more.

---

## Features

- Translates all 11,000+ XenForo phrases automatically
- Preserves XenForo variables (`{username}`, `{count}`, etc.)
- Preserves HTML tags inside phrases
- Saves progress — safely resume if interrupted
- Remembers your API key (no re-entry on next run)
- Remembers your last used language
- Simple interactive menu — no command-line knowledge needed

---

## Requirements

- Python 3.10+  →  https://www.python.org/downloads/
- DeepL API key (free) →  https://www.deepl.com/pro-api
  - Free plan: **500,000 characters/month** (enough for a full XenForo file)

---

## Usage

### Step 1 — Export the language file from XenForo

1. Log in to your **XenForo Admin Panel**
2. Go to **Appearance → Languages**
3. Click the **download icon** next to *English (US)*
4. Save the `.xml` file into this folder

### Step 2 — Run the tool

**Windows:** double-click `run.bat`

**Terminal:**
```bash
python xf_translate.py
```

On first run you will be asked for your DeepL API key — it is saved automatically for future runs.

### Step 3 — Select target language

```
  Select Target Language
  ──────────────────────────────────────────────────
   1. Arabic        [AR]    16. Norwegian   [NB]
   2. Bulgarian     [BG]    17. Dutch        [NL]
   3. Czech         [CS]    18. Polish       [PL]
   ...
  28. Turkish       [TR] ◄  (last used)
  ...
  Enter number [28]:
```

### Step 4 — Wait for completion

Progress is displayed in real time:

```
  [████████████████████] 100%  11,141/11,141  almost done
  Done! 11,141 phrases translated.
```

The output file (`language-Turkish-XF.xml`) will appear in this folder.

### Step 5 — Import into XenForo

1. Go to **Appearance → Languages → Import**
2. Select the output XML file
3. Click **Import**

---

## Command-line options

```bash
python xf_translate.py                  # interactive mode
python xf_translate.py myfile.xml       # specify source file
python xf_translate.py --reset-key      # change saved API key
```

---

## File structure

```
XenForo Auto Translate/
├── xf_translate.py        # main script
├── run.bat                # Windows launcher
├── README.md              # this file
└── .gitignore
```

> XML language files and progress files are excluded from version control via `.gitignore`.

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| `deepl package not found` | Run `python -m pip install deepl` |
| `Invalid API key` | Check your key at deepl.com or run with `--reset-key` |
| `Quota exceeded` | Free limit reached; progress is saved, re-run next month |
| No XML files found | Export the language file from XenForo admin panel first |
| XenForo: *not a valid XML file* | Re-run the translation — output may be incomplete |

---

## License

MIT
