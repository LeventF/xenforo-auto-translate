<div align="center">

# 🌐 XenForo Auto Translate

**Automatically translate XenForo 2.x language files into any language — powered by [studyo.gg](https://studyo.gg)**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![DeepL](https://img.shields.io/badge/DeepL-API-0F2B46?logo=deepl&logoColor=white)](https://www.deepl.com/pro-api)
[![XenForo](https://img.shields.io/badge/XenForo-2.x-orange)](https://xenforo.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Languages](https://img.shields.io/badge/Languages-30%2B-purple)](https://www.deepl.com/docs-api/translate-text/translate-text/)

</div>

---

## ✨ Features

- 🔄 Translates **11,000+ XenForo phrases** automatically
- 🛡️ Preserves XenForo variables (`{username}`, `{count}`, `{board}`, etc.)
- 🏷️ Preserves HTML tags inside phrases
- 💾 **Auto-saves progress** — safely resume if interrupted
- 🔑 **Remembers your API key** — enter once, never again
- 🌍 Remembers your last used language
- 🖥️ Simple interactive menu — no command-line knowledge needed
- ⚡ Batch processing with real-time progress bar

---

## 📋 Requirements

| Requirement | Details |
|-------------|---------|
| **Python** | 3.10 or higher — [download](https://www.python.org/downloads/) |
| **DeepL API Key** | Free plan: 500,000 chars/month — [get key](https://www.deepl.com/pro-api) |
| **XenForo** | Version 2.x |

> The free DeepL plan (500,000 chars/month) is enough to translate a full XenForo language file.

---

## 🚀 Getting Started

### Step 1 — Export your XenForo language file

1. Log in to your **XenForo Admin Panel**
2. Navigate to **Appearance → Languages**
3. Click the **download icon** next to *English (US)*
4. Save the `.xml` file into this folder

### Step 2 — Run the tool

**Windows** — double-click `run.bat`

**Terminal:**
```bash
python xf_translate.py
```

### Step 3 — Select target language

```
╔══════════════════════════════════════════════════════╗
║        XenForo Auto Translate  |  DeepL API         ║
╚══════════════════════════════════════════════════════╝

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

### Step 4 — Watch it translate

```
  [████████████████████] 100%  11,141/11,141  almost done

  ╔══════════════════════════════════════════╗
  ║          TRANSLATION COMPLETE!           ║
  ╚══════════════════════════════════════════╝

  Output : language-Turkish-XF.xml
  Phrases: 11,141 total translated
```

### Step 5 — Import into XenForo

1. Go to **Appearance → Languages → Import**
2. Select the output `.xml` file
3. Click **Import** ✅

---

## 🌍 Supported Languages

<div align="center">

| Code | Language | Code | Language |
|------|----------|------|----------|
| AR | Arabic | NB | Norwegian |
| BG | Bulgarian | NL | Dutch |
| CS | Czech | PL | Polish |
| DA | Danish | PT-BR | Portuguese (Brazil) |
| DE | German | PT-PT | Portuguese (Europe) |
| EL | Greek | RO | Romanian |
| ES | Spanish | RU | Russian |
| ET | Estonian | SK | Slovak |
| FI | Finnish | SL | Slovenian |
| FR | French | SV | Swedish |
| HU | Hungarian | **TR** | **Turkish** |
| ID | Indonesian | UK | Ukrainian |
| IT | Italian | ZH | Chinese (Simplified) |
| JA | Japanese | KO | Korean |
| LT | Lithuanian | LV | Latvian |

</div>

---

## ⚙️ Command-line Options

```bash
python xf_translate.py                  # interactive mode
python xf_translate.py myfile.xml       # specify source file directly
python xf_translate.py --reset-key      # change your saved API key
```

---

## 📁 File Structure

```
XenForo Auto Translate/
├── xf_translate.py        # main script
├── run.bat                # Windows one-click launcher
├── README.md              # documentation
└── .gitignore

# Generated files (git-ignored):
├── language-*-XF.xml      # translated output files
└── .progress_*.json       # auto-save files (deleted on completion)
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| `deepl package not found` | Run `python -m pip install deepl` |
| `Invalid API key` | Check your key at [deepl.com](https://www.deepl.com/account) or use `--reset-key` |
| `Quota exceeded` | Free limit reached — progress is saved, re-run next month |
| No XML files found in tool | Export the language file from XenForo admin panel first |
| XenForo: *not a valid XML file* | Re-run — output may have been incomplete |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

Made with ❤️ using [studyo.gg](https://studyo.gg)

</div>
