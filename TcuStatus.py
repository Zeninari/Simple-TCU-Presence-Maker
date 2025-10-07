import os
import sys
import atexit
import subprocess
import time
import json
import threading
from datetime import datetime
from difflib import get_close_matches
from rapidfuzz import process, fuzz
import re
import pyautogui
import pytesseract
from PIL import Image, ImageEnhance
import keyboard
from pypresence import Presence
import tkinter as tk
import unicodedata

# =====================================================
# ---------------- Runtime Globals --------------------
# =====================================================
running = True                # master loop control
pause_ocr = False             # pause flag (when overlay active)
overlay_enabled = False       # prevent multiple overlay windows

current_main = None           # current confirmed main area
current_sub = None            # current confirmed sub area
main_buffer = None            # buffer for disambiguating multi-main subs
last_confirmed_sub = None     # used for transition overrides
previous_main_context = None  # backup for context-sensitive mapping

all_sub_areas_list = []       # flat list of all sub areas
sub_areas_map = {}            # sub → [main, ...]
main_images = {}              # dynamic large images
sub_to_mains_list = {}        # uppercase sub → [main, ...]
transition_overrides = []     # list of override rules

# OCR global defaults
ZONE_COORDS = (1655, 772, 208, 36)   # default OCR region
SMART_FALLBACK = True                # ignore noisy results

# Logging & fuzzy thresholds
TIME_IN_AREA = False
DYNAMIC_LARGE_IMAGE = False
VERBOSE_LOGGING = False
FUZZY_THRESHOLD = 95
OCR_SCALE = 4
UPDATE_INTERVAL = 10

# =====================================================
# ---------------- UTF-8 Console Setup ----------------
# =====================================================
def set_utf8_console():
    if os.name == "nt":
        result = subprocess.run("chcp", capture_output=True, text=True, shell=True)
        original_cp = None
        if result.stdout:
            try:
                original_cp = int(result.stdout.split(":")[-1].strip())
            except:
                pass
        os.system("chcp 65001 > nul")
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        if original_cp:
            sys._original_cp = original_cp  # store it for clean exit
            def restore_cp():
                os.system(f"chcp {original_cp} > nul")
            atexit.register(restore_cp)

set_utf8_console()

# =====================================================
# ---------------- OCR Language Map -------------------
# =====================================================
OCR_LANGUAGE_MAP = {
    "EN": "eng", "FI": "fin", "FR": "fra", "DE": "deu", "JP": "jpn",
    "NO": "nor", "IT": "ita", "PL": "pol", "ES": "spa", "SV": "swe",
    "CS": "ces", "PT": "por", "DA": "dan", "NL": "nld", "RU": "rus"
}
def get_ocr_language(lang_code: str) -> str:
    return OCR_LANGUAGE_MAP.get(lang_code.upper(), "eng")

# =====================================================
# -------------- OCR Text Normalization --------------
# =====================================================
COMMON_OCR_MISREADS = {
    "ß": "ss",
    "ø": "o", "Ø": "O",
    "å": "a", "Å": "A",
    "ä": "a", "Ä": "A",
    "ö": "o", "Ö": "O",
    "é": "e", "è": "e", "ê": "e", "ë": "e",
    "á": "a", "à": "a", "â": "a", "ã": "a",
    "í": "i", "ì": "i", "î": "i", "ï": "i",
    "ó": "o", "ò": "o", "ô": "o", "õ": "o",
    "ú": "u", "ù": "u", "û": "u", "ü": "u",
    "ç": "c",
    "ń": "n", "ñ": "n",
    "ś": "s", "š": "s",
    "ž": "z", "ź": "z", "ż": "z",
    "ď": "d", "ť": "t", "ř": "r", "ů": "u",
    "ě": "e",

    # Cyrillic-to-Latin OCR confusions (common in Russian text)
    "А": "A", "В": "B", "Е": "E", "К": "K", "М": "M", "Н": "H",
    "О": "O", "Р": "P", "С": "C", "Т": "T", "У": "Y", "Х": "X",
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "у": "y", "х": "x",
    "І": "I", "і": "i",  # sometimes from Ukrainian fonts
    "Ѵ": "V", "ѵ": "v",
}

def normalize_ocr_text(text: str) -> str:
    """
    Converts OCR text to a normalized form for fuzzy matching:
    - Strips accents & diacritics
    - Maps common misreads to expected letters
    - Converts to uppercase
    """
    if not text:
        return ""
    
    # Decompose Unicode characters (é -> e + ´)
    text = unicodedata.normalize("NFKD", text)
    
    # Remove combining marks (accents)
    text = "".join(c for c in text if not unicodedata.combining(c))
    
    # Map common OCR misreads
    text = "".join(COMMON_OCR_MISREADS.get(c, c) for c in text)
    
    # Remove extra whitespace and unwanted symbols
    text = re.sub(r"[^A-Za-z0-9\s\-]", "", text)
    
    return text.upper()

# =====================================================
# ---------------- Resource Handling ------------------
# =====================================================
def resource_path(relative_path):
    """Resolves paths correctly for both .py and .exe (PyInstaller) builds."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# =====================================================
# ---------------- Config Handling --------------------
# =====================================================
CONFIG_FILE = os.path.join(
    os.path.dirname(sys.executable if getattr(sys, "frozen", False) else __file__),
    "config.json"
)

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)

def log_message(msg: str):
    timestamp_full = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp_short = datetime.now().strftime("%H:%M:%S")
    with open("TcuStatus.log", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp_full}] {msg}\n")
    print(f"[{timestamp_short}] {msg}")

# =====================================================
# --------------- Verification Check ------------------
# =====================================================

def ensure_config_values(cfg):
    """
    Ensures required config values exist and are valid.
    Prompts user for missing critical fields, and allows "default" to use preset defaults
    for Discord image/text/button fields.
    """
    needs_setup = False  # track if we need to save & exit

    # ---------------- Discord Client ID ----------------
    client_id = str(cfg.get("DISCORD_CLIENT_ID", "")).strip()
    if not client_id or not client_id.isdigit():
        needs_setup = True
        log_message("[!] No valid Discord Client ID found in config.json.")
        print("\nYou can create one at: https://discord.com/developers/applications\n")
        while True:
            new_id = input("Please enter your Discord Client ID: ").strip()
            if not new_id or not new_id.isdigit():
                print("Invalid ID. Discord Client IDs contain only numbers.\n")
                continue
            break
        cfg["DISCORD_CLIENT_ID"] = new_id
        log_message(f"[+] Discord Client ID saved: {new_id}")

    # ---------------- Current Language ----------------
    valid_langs = list(OCR_LANGUAGE_MAP.keys())
    curr_lang = str(cfg.get("current_language", "")).upper()
    if curr_lang not in valid_langs:
        needs_setup = True
        print(f"\nSupported languages: {', '.join(valid_langs)}")
        while True:
            lang_input = input("Please enter your current language code (e.g., EN): ").strip().upper()
            if lang_input not in valid_langs:
                print(f"Invalid code. Supported codes: {', '.join(valid_langs)}\n")
                continue
            break
        cfg["current_language"] = lang_input
        log_message(f"[+] Current language set to: {lang_input}")

    # ---------------- Time / Verbose / Dynamic ----------------
    bool_fields = {
        "time_in_area": False,
        "verbose_logging": False,
        "dynamic_large_image": False
    }
    for key, default in bool_fields.items():
        val = cfg.get(key)
        if val not in (True, False):
            needs_setup = True
            response = input(f"Do you want {key.replace('_',' ')}? (yes/no) [default: {default}]: ").strip().lower()
            cfg[key] = response in ("yes", "y") if response not in ("default", "use default", "") else default
            log_message(f"[+] {key} set to: {cfg[key]}")

    # ---------------- Discord Image / Text / Buttons ----------------
    discord_defaults = {
        "large_image": "embedded_cover",
        "large_text": "Once A 5-10, Always A 5-10",
        "small_image": "thecrewunlimitedicon",
        "small_text": "The Crew Unlimited",
        "button1_label": "Join the TCU Discord Server!",
        "button1_url": "https://discord.gg/tcu",
        "button2_label": "Check the TCU YouTube Channel!",
        "button2_url": "https://youtube.com/@whammy4"
    }

    for key, default in discord_defaults.items():
        val = cfg.get(key)
        if not val or not isinstance(val, str):
            needs_setup = True
            prompt_text = f"Enter value for '{key}' or type 'default' to use default [{default}]: "
            user_input = input(prompt_text).strip()
            if user_input.lower() in ("default", "use default", ""):
                cfg[key] = default
            else:
                cfg[key] = user_input
            log_message(f"[+] {key} set to: {cfg[key]}")

    # ---------------- OCR / Interval Defaults ----------------
    cfg["update_interval"] = cfg.get("update_interval", 10)
    cfg["ocr_scale"] = cfg.get("ocr_scale", 4)
    cfg["ocr_region"] = tuple(cfg.get("ocr_region", (1655, 772, 208, 36)))

    # ---------------- Save config & exit if setup was needed ----------------
    if needs_setup:
        save_config(cfg)
        log_message("[+] config.json settings have been saved.")
        log_message("[!] Please rerun the Exe/Script")
        time.sleep(3)
        sys.exit(0)

    return cfg

# =====================================================
# ------------------ Load Config ----------------------
# =====================================================

# Load configuration and ensures Discord client ID exists
config = ensure_config_values(load_config())

# Override globals with config values
UPDATE_INTERVAL   = config.get("update_interval", UPDATE_INTERVAL)
OCR_SCALE         = config.get("ocr_scale", OCR_SCALE)
current_language  = config.get("current_language", "EN").upper()
exe_folder = os.path.dirname(sys.executable if getattr(sys, "frozen", False) else __file__)
LANGUAGE_JSON = os.path.join(exe_folder, config.get("language_path", "Language"), f"{current_language}.json")
ZONE_COORDS       = tuple(config.get("ocr_region", ZONE_COORDS))
TIME_IN_AREA      = config.get("time_in_area", TIME_IN_AREA)
DYNAMIC_LARGE_IMAGE = config.get("dynamic_large_image", DYNAMIC_LARGE_IMAGE)
VERBOSE_LOGGING   = config.get("verbose_logging", VERBOSE_LOGGING)

# Override Discord presence with config values
DISCORD_CLIENT_ID = config.get("DISCORD_CLIENT_ID")
LARGE_IMAGE  = config.get("large_image", "")
LARGE_TEXT   = config.get("large_text", "")
SMALL_IMAGE  = config.get("small_image", "")
SMALL_TEXT   = config.get("small_text", "")
BUTTON1_LABEL = config.get("button1_label", "")
BUTTON1_URL   = config.get("button1_url", "")
BUTTON2_LABEL = config.get("button2_label", "")
BUTTON2_URL   = config.get("button2_url", "")

ocr_lang = get_ocr_language(current_language)

# =====================================================
# ---------------- OCR Capture Folder -----------------
# =====================================================
OCR_CAPTURE_FOLDER = os.path.join(exe_folder, "Capture")
os.makedirs(OCR_CAPTURE_FOLDER, exist_ok=True)

# =====================================================
# ----------- Hotkey Functions + Logging --------------
# =====================================================
with open("TcuStatus.log", "w", encoding="utf-8") as f:
    f.write("")

def toggle_timeinarea():
    global TIME_IN_AREA
    TIME_IN_AREA = not TIME_IN_AREA
    config["time_in_area"] = TIME_IN_AREA
    save_config(config)                                  
    log_message(f"[+] Time In Area {'enabled' if TIME_IN_AREA else 'disabled'}")

def toggle_dynamic_large_image():
    global DYNAMIC_LARGE_IMAGE
    DYNAMIC_LARGE_IMAGE = not DYNAMIC_LARGE_IMAGE
    config["dynamic_large_image"] = DYNAMIC_LARGE_IMAGE
    save_config(config)
    log_message(f"[+] Dynamic Large Image {'enabled' if DYNAMIC_LARGE_IMAGE else 'disabled'}")

def toggle_verbose():
    global VERBOSE_LOGGING
    VERBOSE_LOGGING = not VERBOSE_LOGGING
    config["verbose_logging"] = VERBOSE_LOGGING
    save_config(config)                          
    log_message(f"[+] Verbose logging {'enabled' if VERBOSE_LOGGING else 'disabled'}")

# =====================================================
# ---------------- Tesseract Setup --------------------
# =====================================================
def ensure_tesseract_installed():
    global TESSERACT_PATH, TESSDATA_FALLBACK
    TESSERACT_PATH = resource_path(os.path.join("Tesseract-OCR", "tesseract.exe"))
    TESSDATA_FALLBACK = resource_path(os.path.join("Tesseract-OCR", "tessdata"))

    if not os.path.exists(TESSERACT_PATH):
        log_message(f"[!] Embedded Tesseract not found: {TESSERACT_PATH}")
        sys.exit(1)

    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
    os.environ["TESSDATA_PREFIX"] = TESSDATA_FALLBACK
    log_message(f"[+] Using embedded Tesseract: {TESSERACT_PATH}")

ensure_tesseract_installed()

# =====================================================
# ---------------- Startup Message --------------------
# =====================================================
print("""
Welcome To A Simple TCU Status Presence Maker!

Press 1 To Toggle Time Spent In Current Area
Press 2 To Toggle Reactive Images
Press 3 To Toggle Verbose Logging (Debug)
Press 4 To Reload The Language Files (Debug)
Press 5 To Redefine OCR Region Dynamically
Press 6 To Screenshot Current OCR Region
Press 7 To Exit The Bot
""")

# =====================================================
# ---------------- Language Loading -------------------
# =====================================================
def load_language_file():
    """
    Loads all subs, main image overrides, and transition overrides from the language JSON.
    Ensures that all 'to' subs in transitions are recognized even if they
    aren't part of a standard main area.
    Also updates OCR language.
    """
    global all_sub_areas_list, sub_areas_map, transition_overrides, ocr_lang, current_language, main_images

    # Load language JSON path
    LANGUAGE_JSON = os.path.join(exe_folder, config.get("language_path", "Language"), f"{current_language}.json")

    with open(LANGUAGE_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Update OCR language for Tesseract
    ocr_lang = get_ocr_language(current_language)

    all_sub_areas_set = set()  # use a set to avoid duplicates
    sub_to_main_map = {}
    transition_overrides = data.get("transition_overrides", [])
    main_images = data.get("main_images", {}) 

    # Load main to sub mapping
    for main_area, subs in data.items():
        if main_area in ("transition_overrides", "main_images"):
            continue
        for sub in subs:
            sub_clean = sub.strip()
            norm_sub = sub_clean.upper()
            all_sub_areas_set.add(sub_clean)
            sub_to_main_map.setdefault(norm_sub, []).append(main_area.strip())

    # Add 'to' subs from transitions
    for trans in transition_overrides:
        to_sub = (trans.get("to") or "").strip()
        if to_sub:
            norm_to = to_sub.upper()
            if norm_to not in sub_to_main_map:
                all_sub_areas_set.add(to_sub)
                sub_to_main_map[norm_to] = []

    # Convert set to sorted list for consistency
    all_sub_areas_list = sorted(all_sub_areas_set)
    sub_areas_map = sub_to_main_map

    return all_sub_areas_list, sub_areas_map, transition_overrides

def reload_language_file_hotkey():
    global all_sub_areas_list, sub_areas_map, transition_overrides
    global sub_to_mains_list, main_buffer, current_main, current_sub, previous_main_context
    all_sub_areas_list, sub_areas_map, transition_overrides = load_language_file()
    sub_to_mains_list.clear()
    for sub_upper, mains in sub_areas_map.items():
        sub_to_mains_list.setdefault(sub_upper, []).extend(mains)
    main_buffer = current_main = current_sub = previous_main_context = None

def reload_language_file_hotkey_safe():
    global ocr_lang
    try:
        reload_language_file_hotkey()
        ocr_lang = get_ocr_language(current_language)
        log_message("[+] Language file reloaded and OCR language updated via F9")
    except Exception as e:
        log_message(f"[!] F9 reload failed: {e}")

# =====================================================
# ---------------- Discord Presence -------------------
# =====================================================
rpc = Presence(DISCORD_CLIENT_ID)
rpc.connect()
start_time = int(time.time())

def update_discord_status(main_area, sub_area):
    buttons = []
    if BUTTON1_LABEL and BUTTON1_URL:
        buttons.append({"label": BUTTON1_LABEL, "url": BUTTON1_URL})
    if BUTTON2_LABEL and BUTTON2_URL:
        buttons.append({"label": BUTTON2_LABEL, "url": BUTTON2_URL})

    large_image_key = LARGE_IMAGE  # default

    if DYNAMIC_LARGE_IMAGE:
        # Use language file mappings if available
        if "main_images" in globals() and isinstance(main_images, dict):
            large_image_key = main_images.get(main_area, large_image_key)

        if VERBOSE_LOGGING:
            log_message(f"[+] Dynamic Large Image updated to '{large_image_key}'")

    try:
        rpc.update(
            state=str(sub_area),
            details=str(main_area),
            large_image=large_image_key or LARGE_IMAGE,
            large_text=LARGE_TEXT or None,
            small_image=SMALL_IMAGE or None,
            small_text=SMALL_TEXT or None,
            start=start_time,
            buttons=buttons if buttons else None
        )
    except Exception as e:
        log_message(f"[!] Discord update failed: {e}")

# =====================================================
# ---------------- OCR Matching Helper ----------------
# =====================================================
def clean_ocr_text(text):
    if not text: 
        return ""
    text = text.replace("\u200b", "").replace("\ufeff", "")
    text = re.sub(r"\s+", " ", text.strip())
    cleaned = "".join(c for c in text if c.isalnum() or c in " -’.,、。")
    return "".join(c.upper() if "A" <= c <= "Z" else c for c in cleaned)

def preprocess_zone_image(img: Image.Image) -> Image.Image:
    gray_img = img.convert("L")
    enhanced = ImageEnhance.Contrast(gray_img).enhance(1.5)
    return enhanced.resize(
        (int(enhanced.width * OCR_SCALE), int(enhanced.height * OCR_SCALE)), 
        Image.LANCZOS
    )

def match_area_hybrid(ocr_text, possible_areas, fallback="Unknown Location"):
    """
    Matches OCR text to the most likely sub-area using:
    - exact match
    - partial match
    - fuzzy match with stricter thresholds and first-letter check
    """
    if not ocr_text or not possible_areas: 
        return fallback

    ocr_norm = normalize_ocr_text(ocr_text)
    possible_norm = [normalize_ocr_text(s) for s in possible_areas]

    # Exact match
    for i, sub in enumerate(possible_norm):
        if sub == ocr_norm:
            return possible_areas[i]

    # Partial match (OCR text contained in the sub or vice versa)
    for i, sub in enumerate(possible_norm):
        if ocr_norm in sub or sub in ocr_norm:
            # length tolerance is 25% to prevent false positives
            if abs(len(sub) - len(ocr_norm)) / max(len(sub), 1) <= 0.25:
                return possible_areas[i]

    # Fuzzy match (stricter + first-letter check)
    result = process.extractOne(ocr_norm, possible_norm, scorer=fuzz.partial_ratio)
    if result:
        match, score, *_ = result if len(result) >= 2 else (result[0], 0)
        if (
            score >= 85  # require high similarity
            and abs(len(match) - len(ocr_norm)) / max(len(match), 1) <= 0.25  # length sanity
            and ocr_norm[0] == match[0]  # first-letter MUST match
        ):
            return possible_areas[possible_norm.index(match)]

    return fallback

# =====================================================
# ---------------- OCR + Main Loop --------------------
# =====================================================
def main_loop():
    global current_main, current_sub, main_buffer, last_confirmed_sub, start_time
    while running:
        try:
            if pause_ocr:
                time.sleep(0.2)
                continue

            # Capture the OCR region
            zone_img = pyautogui.screenshot(region=ZONE_COORDS)
            ocr_raw = pytesseract.image_to_string(
                preprocess_zone_image(zone_img), lang=ocr_lang, config="--psm 7"
            )
            ocr_clean = clean_ocr_text(ocr_raw)

            # Match sub-area using the hybrid matcher
            matched_sub = match_area_hybrid(ocr_clean, all_sub_areas_list, fallback="Unknown Location")
            possible_mains = sub_to_mains_list.get(matched_sub.upper(), [])
            matched_main = "Unknown Main Area"

            # Determine main area based on the buffer
            if len(possible_mains) == 1:
                matched_main = main_buffer = possible_mains[0]
            elif len(possible_mains) > 1 and main_buffer in possible_mains:
                matched_main = main_buffer

            # Apply transition overrides
            if last_confirmed_sub:
                def _norm_key(s: str) -> str:
                    return re.sub(r'\s+', '', (s or "")).upper()

                last_norm = _norm_key(last_confirmed_sub)
                matched_norm = _norm_key(matched_sub)

                for trans in transition_overrides:
                    from_sub = (trans.get("from") or "").strip()
                    to_sub   = (trans.get("to")   or "").strip()
                    main_override = (trans.get("main") or "").strip()
                    if not from_sub or not to_sub or not main_override:
                        continue

                    if last_norm == _norm_key(from_sub) and matched_norm == _norm_key(to_sub):
                        matched_main = main_override
                        main_buffer = matched_main
                        log_message(f"[!] Transition override applied: {from_sub} → {to_sub} → Main: {main_override}")
                        break

            # Only update last_confirmed_sub is valid
            if matched_sub != "Unknown Location":
                last_confirmed_sub = matched_sub

            is_fallback = matched_sub == "Unknown Location" or matched_main == "Unknown Main Area"

            if VERBOSE_LOGGING:
                log_message(f"[VERBOSE] OCR Zone: '{ocr_clean}' | Sub: '{matched_sub}' | Main: '{matched_main}' | Fallback: {is_fallback}")

            # Determine final values for comparison check
            final_sub = matched_sub if matched_sub != "Unknown Location" else current_sub
            final_main = matched_main if matched_main != "Unknown Main Area" else current_main

            # Only update Discord if the location actually changed
            location_changed = (final_sub != current_sub) or (final_main != current_main)

            if location_changed:
                # Reset TIME_IN_AREA timer only if we have a valid change
                if TIME_IN_AREA and not is_fallback:
                    start_time = int(time.time())

                # SMART_FALLBACK handling
                if SMART_FALLBACK and is_fallback:
                    if VERBOSE_LOGGING:
                        log_message(f"[!] SMART_FALLBACK ignored fallback OCR: (Sub='{final_sub}', Main='{final_main}')")

                else:
                    log_message(f"OCR Zone: '{ocr_clean}' | Sub: '{final_sub}' | Main: '{final_main}'")
                    try:
                        update_discord_status(final_main, final_sub)
                        log_message("[!] Discord presence updated successfully")
                    except Exception as e:
                        log_message(f"[!] Failed to update Discord: {e}")

                    # Update the current location after a successful update
                    current_main, current_sub = final_main, final_sub

            time.sleep(UPDATE_INTERVAL)

        except Exception as e:
            if running:
                log_message(f"[!] Error in main loop: {e}")
            else:
                break
            time.sleep(UPDATE_INTERVAL)

# =====================================================
# --------------- Save Capture & Exit -----------------
# =====================================================
def save_capture():
    """Captures the current OCR region and saves both raw and processed images."""
    try:
        x, y, w, h = map(int, ZONE_COORDS)
        zone_capture = pyautogui.screenshot(region=(x, y, w, h))
        timestamp = datetime.now().strftime("%Y-%m-%d %Hh %Mm %Ss")

        # Raw screenshot
        raw_path = os.path.join(OCR_CAPTURE_FOLDER, f"OCRZone_{timestamp}_raw.png")
        zone_capture.save(raw_path)

        # Processed screenshot
        processed_path = os.path.join(OCR_CAPTURE_FOLDER, f"OCRZone_{timestamp}_processed.png")
        preprocess_zone_image(zone_capture).save(processed_path)

        log_message(f"[+] Saved OCR capture at {timestamp}")
    except Exception as e:
        log_message(f"[!] save_capture() failed: {e}")

# Exiting after reloading the bot due to invalid/missing DISCORD_CLIENT_ID is buggy.
# If running via the .py it will captue all keypresses due to how it works.
def exit_bot():
    """Gracefully exit the bot."""
    global running
    running = False
    log_message("[!] Exiting Bot Safely...")
    os._exit(0)

# Hotkeys
keyboard.add_hotkey("1", toggle_timeinarea, suppress=True)
keyboard.add_hotkey("2", toggle_dynamic_large_image, suppress=True)
keyboard.add_hotkey("3", toggle_verbose, suppress=True)
keyboard.add_hotkey("4", reload_language_file_hotkey_safe, suppress=True)
keyboard.add_hotkey("5", lambda: threading.Thread(target=define_ocr_region_overlay, daemon=False).start(), suppress=True)
keyboard.add_hotkey("6", save_capture, suppress=True)
keyboard.add_hotkey("7", exit_bot, suppress=True)

# =====================================================
# ---------------- OCR Region Overlay -----------------
# =====================================================
def define_ocr_region_overlay():
    global ZONE_COORDS, overlay_enabled, pause_ocr
    if overlay_enabled:
        log_message("[!] OCR Overlay already open.")
        return

    overlay_enabled = True
    pause_ocr = True
    log_message("[!] OCR Region Redefinition Overlay Started (5)")

    root = tk.Tk()
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.3)
    root.attributes("-fullscreen", True)
    root.configure(bg="black")
    root.title("Select OCR Region")

    start_x = start_y = end_x = end_y = 0
    rect_id = None
    region_selected = False  

    canvas = tk.Canvas(root, bg="black")
    canvas.pack(fill=tk.BOTH, expand=True)

    def on_mouse_down(event):
        nonlocal start_x, start_y, rect_id
        start_x, start_y = event.x, event.y
        if rect_id:
            canvas.delete(rect_id)
            rect_id = None

    def on_mouse_drag(event):
        nonlocal rect_id
        if rect_id:
            canvas.delete(rect_id)
        rect_id = canvas.create_rectangle(start_x, start_y, event.x, event.y, outline="red", width=2)

    def on_mouse_up(event):
        nonlocal start_x, start_y, end_x, end_y, region_selected
        end_x, end_y = event.x, event.y
        x1, y1 = min(start_x, end_x), min(start_y, end_y)
        x2, y2 = max(start_x, end_x), max(start_y, end_y)
        w, h = x2 - x1, y2 - y1
        if w > 0 and h > 0:
            region_selected = True
            new_coords = (x1, y1, w, h)
            ZONE_COORDS = new_coords
            config["ocr_region"] = list(new_coords)
            save_config(config)
            log_message(f"[!] OCR Region Updated To {new_coords}")
        root.quit()  # stop mainloop safely

    def close_overlay():
        global overlay_enabled, pause_ocr
        overlay_enabled = False
        pause_ocr = False
        try:
            root.destroy()
        except Exception:
            pass
        if not region_selected:
            log_message("[!] OCR Region Overlay Closed (no changes saved)")
        else:
            log_message("[!] OCR Region Overlay Closed")

    canvas.bind("<ButtonPress-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)

    try:
        root.mainloop()
    finally:
        close_overlay()

# =====================================================
# ---------------- Start Bot --------------------------
# =====================================================
all_sub_areas_list, sub_areas_map, transition_overrides = load_language_file()
for sub_upper, mains in sub_areas_map.items():
    sub_to_mains_list.setdefault(sub_upper, []).extend(mains)
log_message("[+] Language file loaded at startup")

thread = threading.Thread(target=main_loop, daemon=True)
thread.start()

try:
    while running:
        time.sleep(0.1)
finally:
    running = False
    thread.join(timeout=2)
    log_message("[!] Bot fully exited")
