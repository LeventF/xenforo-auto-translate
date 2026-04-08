#!/usr/bin/env python3
"""
XenForo Auto Translate - DeepL API
Translates XenForo XML language files to any language supported by DeepL.

Usage:
  python xf_translate.py
  python xf_translate.py path/to/language.xml
  python xf_translate.py --reset-key
"""

import re
import time
import json
import os
import sys
from pathlib import Path

try:
    import deepl
except ImportError:
    print("ERROR: 'deepl' package not found.")
    print("Install it with:  python -m pip install deepl")
    sys.exit(1)

# ── Constants ─────────────────────────────────────────────────────────────────
SCRIPT_DIR    = Path(__file__).parent
CONFIG_FILE   = Path.home() / ".xf_translator_config.json"
BATCH_SIZE    = 40
SLEEP_BETWEEN = 0.3

PHRASE_PATTERN   = re.compile(r'(<phrase\s[^>]+>)<!\[CDATA\[(.*?)\]\]>(</phrase>)', re.DOTALL)
XF_VAR_PATTERN   = re.compile(r'\{[^}]*\}')
HTML_TAG_PATTERN = re.compile(r'<[^>]+>')

HTML_ENTITIES = {
    "&#x27;": "'", "&#39;": "'", "&quot;": '"',
    "&amp;": "&", "&#x2F;": "/", "&#x60;": "`",
}

# ── Terminal helpers ──────────────────────────────────────────────────────────

def clr(code, text):
    return f"\033[{code}m{text}\033[0m"

def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(clr("36;1", "╔══════════════════════════════════════════════════════╗"))
    print(clr("36;1", "║        XenForo Auto Translate  |  DeepL API         ║"))
    print(clr("36;1", "╚══════════════════════════════════════════════════════╝"))
    print()

def section(title):
    print(clr("33;1", f"  {title}"))
    print(clr("33",   "  " + "─" * 46))

# ── Config ────────────────────────────────────────────────────────────────────

def load_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_config(cfg: dict):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)

# ── API Key ───────────────────────────────────────────────────────────────────

def get_api_key(cfg: dict, reset: bool = False) -> tuple[str, "deepl.Translator"]:
    if reset:
        cfg.pop("api_key", None)
        save_config(cfg)
        print(clr("33", "  API key cleared.\n"))

    api_key = cfg.get("api_key") or os.environ.get("DEEPL_API_KEY")

    while True:
        if api_key:
            masked = api_key[:8] + "*" * 20
            print(f"  Using saved API key: {clr('32', masked)}")
        else:
            print(f"  {clr('33', 'A DeepL API key is required.')}")
            print("  Free key (500,000 chars/month): https://www.deepl.com/pro-api\n")
            api_key = input("  Enter API key: ").strip()
            if not api_key:
                print(clr("31", "  Key cannot be empty.\n"))
                continue

        try:
            translator = deepl.Translator(api_key)
            usage = translator.get_usage()
            if usage.character.limit:
                remaining = usage.character.limit - usage.character.count
                pct = remaining * 100 // usage.character.limit
                bar = ("█" * (pct // 10)).ljust(10)
                print(clr("32", f"  Connected!  [{bar}] {remaining:,} / {usage.character.limit:,} chars remaining\n"))
            else:
                print(clr("32", "  Connected!  (Pro plan — unlimited)\n"))

            cfg["api_key"] = api_key
            save_config(cfg)
            return api_key, translator

        except deepl.exceptions.AuthorizationException:
            print(clr("31", "  Invalid API key. Please try again.\n"))
            api_key = None
            cfg.pop("api_key", None)

        except Exception as e:
            print(clr("31", f"  Connection error: {e}"))
            sys.exit(1)

# ── Language Selection ────────────────────────────────────────────────────────

def select_language(translator: "deepl.Translator", cfg: dict) -> tuple[str, str]:
    section("Select Target Language")
    print()

    try:
        langs = sorted(translator.get_target_languages(), key=lambda l: l.name)
    except Exception:
        # Fallback static list
        langs = [type("L", (), {"code": c, "name": n})() for c, n in [
            ("AR","Arabic"), ("BG","Bulgarian"), ("CS","Czech"), ("DA","Danish"),
            ("DE","German"), ("EL","Greek"), ("ES","Spanish"), ("ET","Estonian"),
            ("FI","Finnish"), ("FR","French"), ("HU","Hungarian"), ("ID","Indonesian"),
            ("IT","Italian"), ("JA","Japanese"), ("KO","Korean"), ("LT","Lithuanian"),
            ("LV","Latvian"), ("NB","Norwegian (Bokmål)"), ("NL","Dutch"), ("PL","Polish"),
            ("PT-BR","Portuguese (Brazil)"), ("PT-PT","Portuguese (Europe)"),
            ("RO","Romanian"), ("RU","Russian"), ("SK","Slovak"), ("SL","Slovenian"),
            ("SV","Swedish"), ("TR","Turkish"), ("UK","Ukrainian"), ("ZH","Chinese (Simplified)"),
        ]]

    last_code = cfg.get("last_lang", "TR")
    last_idx  = 1
    cols      = 2
    col_w     = 28

    rows = []
    for i, lang in enumerate(langs, 1):
        marker = clr("32", " ◄") if lang.code == last_code else ""
        rows.append(f"  {i:2}. {lang.name:<{col_w}} [{lang.code}]{marker}")
        if lang.code == last_code:
            last_idx = i

    # Print in 2 columns
    half = (len(rows) + 1) // 2
    for i in range(half):
        left  = rows[i]
        right = rows[i + half] if i + half < len(rows) else ""
        print(f"{left:<55}{right}")

    print()
    while True:
        try:
            choice = input(f"  Enter number [{last_idx}]: ").strip()
            idx = int(choice) - 1 if choice else last_idx - 1
            if 0 <= idx < len(langs):
                sel = langs[idx]
                cfg["last_lang"] = sel.code
                save_config(cfg)
                print(clr("32", f"\n  Selected: {sel.name} [{sel.code}]\n"))
                return sel.code, sel.name
            print(clr("31", f"  Invalid choice. Enter 1–{len(langs)}."))
        except (ValueError, KeyboardInterrupt):
            print(clr("31", "  Invalid input."))

# ── File Selection ────────────────────────────────────────────────────────────

def select_file(argv_file: str | None) -> Path:
    if argv_file:
        p = Path(argv_file)
        if p.exists():
            return p
        print(clr("31", f"  File not found: {argv_file}"))

    section("Select Source XML File")
    print()

    # Look for XML files in script directory and parent
    search_dirs = [SCRIPT_DIR, SCRIPT_DIR.parent]
    xml_files   = []
    for d in search_dirs:
        xml_files.extend(sorted(d.glob("language-*.xml")))
    # Remove duplicates
    seen = set()
    xml_files = [f for f in xml_files if not (f in seen or seen.add(f))]

    if xml_files:
        for i, f in enumerate(xml_files, 1):
            size_kb = f.stat().st_size // 1024
            print(f"  {i}. {f.name:<50} ({size_kb:,} KB)")
        print(f"  {len(xml_files)+1}. Enter path manually")
        print()
    else:
        print(clr("33", "  No XML language files found in this folder.\n"))
        print("  To get the file:")
        print("  1. Log in to your XenForo Admin Panel")
        print("  2. Go to:  Appearance > Languages")
        print("  3. Click the download icon next to 'English (US)'")
        print(f"  4. Save the file into this folder:")
        print(f"     {clr('36', str(SCRIPT_DIR))}")
        print("  5. Re-run this tool\n")
        input("  Press Enter to exit...")
        sys.exit(0)

        while True:
            try:
                choice = input(f"  Enter number [1]: ").strip()
                idx = int(choice) - 1 if choice else 0
                if idx == len(xml_files):
                    break  # manual entry
                if 0 <= idx < len(xml_files):
                    print(clr("32", f"\n  Using: {xml_files[idx].name}\n"))
                    return xml_files[idx]
                print(clr("31", f"  Invalid choice."))
            except (ValueError, KeyboardInterrupt):
                break

    # Manual entry
    while True:
        path = input("  File path: ").strip().strip('"')
        p = Path(path)
        if p.exists():
            print(clr("32", f"\n  Using: {p.name}\n"))
            return p
        print(clr("31", "  File not found. Try again."))

# ── Translation Engine ────────────────────────────────────────────────────────

def load_progress(progress_file: Path) -> dict:
    if progress_file.exists():
        try:
            with open(progress_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"  Resuming — {len(data):,} phrases already translated.\n")
            return data
        except Exception:
            pass
    return {}

def save_progress(progress: dict, path: Path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

def protect_variables(text: str) -> tuple[str, dict]:
    tokens, counter = {}, [0]
    def rep(m):
        t = f"XFPH{counter[0]}PH"
        tokens[t] = m.group(0)
        counter[0] += 1
        return t
    return XF_VAR_PATTERN.sub(rep, text), tokens

def restore_variables(text: str, tokens: dict) -> str:
    for t, v in tokens.items():
        text = text.replace(t, v)
    return text

def decode_entities(text: str) -> str:
    for ent, ch in HTML_ENTITIES.items():
        text = text.replace(ent, ch)
    return text

def needs_translation(text: str) -> bool:
    s = text.strip()
    if len(s) < 2:
        return False
    if re.fullmatch(r'[\d\s\W]+', s):
        return False
    if not HTML_TAG_PATTERN.sub('', s).strip():
        return False
    return True

def run_translation(translator, content, progress, progress_file, target_lang):
    matches = list(PHRASE_PATTERN.finditer(content))
    unique  = list(dict.fromkeys(
        m.group(2) for m in matches
        if m.group(2) not in progress and needs_translation(m.group(2))
    ))

    section("Translation Progress")
    print(f"  Total phrases    : {len(matches):,}")
    print(f"  Already done     : {len(progress):,}")
    print(f"  To translate     : {len(unique):,}")
    print()

    if not unique:
        print(clr("32", "  All phrases already translated!\n"))
        return

    errors = 0
    start  = time.time()

    for i in range(0, len(unique), BATCH_SIZE):
        batch_orig = unique[i:i + BATCH_SIZE]
        batch_prot, batch_tok = [], []

        for text in batch_orig:
            p, t = protect_variables(text)
            batch_prot.append(p)
            batch_tok.append(t)

        try:
            results = translator.translate_text(
                batch_prot,
                source_lang="EN",
                target_lang=target_lang,
                tag_handling="html",
                preserve_formatting=True,
            )
            res_list = results if isinstance(results, list) else [results]

            for orig, res, tok in zip(batch_orig, res_list, batch_tok):
                translated = decode_entities(res.text)
                translated = restore_variables(translated, tok)
                progress[orig] = translated

            save_progress(progress, progress_file)

            done    = min(i + BATCH_SIZE, len(unique))
            pct     = done * 100 // len(unique)
            bar     = ("█" * (pct // 5)).ljust(20)
            elapsed = time.time() - start
            eta     = (elapsed / done * (len(unique) - done)) if done else 0
            eta_str = f"ETA {int(eta//60)}m{int(eta%60):02d}s" if eta > 5 else "almost done"
            print(f"  [{bar}] {pct:3d}%  {done:,}/{len(unique):,}  {eta_str}    ", end="\r")

            time.sleep(SLEEP_BETWEEN)

        except deepl.exceptions.QuotaExceededException:
            print(f"\n\n  {clr('31', 'DeepL character quota exceeded!')}")
            print("  Progress saved — re-run to continue from where it stopped.")
            save_progress(progress, progress_file)
            sys.exit(1)

        except Exception as e:
            errors += 1
            print(f"\n  {clr('33', f'Warning (batch {i//BATCH_SIZE+1}): {e}')}")
            if errors > 5:
                print(clr("31", "  Too many errors, stopping."))
                save_progress(progress, progress_file)
                sys.exit(1)
            time.sleep(2)

    print(f"\n  {clr('32', f'Done! {len(unique):,} phrases translated.')}\n")

# ── Build Output XML ──────────────────────────────────────────────────────────

def build_output(content, progress, target_lang, lang_name, input_file) -> Path:
    output = content

    output = re.sub(r'(<language\s[^>]*?)title="[^"]*"',
                    rf'\1title="{lang_name}"', output)
    output = re.sub(r'(<language\s[^>]*?)language_code="[^"]*"',
                    rf'\1language_code="{target_lang.lower()}"', output)

    def replace_cdata(m):
        orig = m.group(2)
        if orig in progress:
            t = progress[orig].replace(']]>', ']]]]><![CDATA[>')
            return f"{m.group(1)}<![CDATA[{t}]]>{m.group(3)}"
        return m.group(0)

    output = PHRASE_PATTERN.sub(replace_cdata, output)

    safe_name = lang_name.replace(" ", "-").replace("(", "").replace(")", "")
    out_path  = SCRIPT_DIR / f"language-{safe_name}-XF.xml"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output)

    return out_path

# ── Entry Point ───────────────────────────────────────────────────────────────

def main():
    if os.name == "nt":
        os.system("color")

    reset_key = "--reset-key" in sys.argv
    argv_file = next((a for a in sys.argv[1:] if not a.startswith("--")), None)

    banner()

    cfg = load_config()

    # Step 1 — API key
    section("DeepL API Key")
    print()
    _, translator = get_api_key(cfg, reset=reset_key)

    # Step 2 — Target language
    target_lang, lang_name = select_language(translator, cfg)

    # Step 3 — Source file
    input_file = select_file(argv_file)

    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Step 4 — Progress file (per language)
    progress_file = SCRIPT_DIR / f".progress_{target_lang.lower()}.json"
    progress      = load_progress(progress_file)

    # Step 5 — Translate
    run_translation(translator, content, progress, progress_file, target_lang)

    # Step 6 — Build output
    print("  Building output XML...")
    out_path = build_output(content, progress, target_lang, lang_name, input_file)

    print(clr("32;1", "  ╔══════════════════════════════════════════╗"))
    print(clr("32;1", "  ║            TRANSLATION COMPLETE!         ║"))
    print(clr("32;1", "  ╚══════════════════════════════════════════╝"))
    print(f"\n  Output : {clr('36', str(out_path))}")
    print(f"  Phrases: {len(progress):,} total translated\n")

    if progress_file.exists():
        progress_file.unlink()

    input("  Press Enter to exit...")

if __name__ == "__main__":
    main()
