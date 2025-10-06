# TCU Status Presence Maker

⚠️ **IMPORTANT:** The program does not interact with the game directly, it only reads your screen to determine your location. 
**THE SCRIPT REQUIRES THE OG HUD TO FUNCTION, IT WILL NOT WORK OTHERWISE**

## Overview
This tool displays your current in-game map location from **The Crew Unlimited** as a Discord Rich Presence status.

---

## How Updates Work

The program reads your in-game location from the screen and updates your Discord status. Here's how it works:

1. **OCR (Optical Character Recognition):**  
   - The bot takes a small screenshot of your map’s HUD text and converts it to characters.

2. **Matching Locations:**  
   - First tries an **exact match** against known sub-area names.  
   - If that fails, tries a **partial match** (for small OCR misreads).  
   - If still no match, uses **fuzzy matching**, but only if the first letter matches and the text is very similar.  
   - This ensures minor OCR errors don’t trigger completely wrong updates.

3. **Transition Rules:**  
   - Certain area transitions have **special rules** (such as moving between a city and its surrounding region, entering an area that appears in multiple locations). The bot manages these automatically.

4. **Discord Updates:**  
   - The bot only updates Discord when the confirmed location changes.  
   - Verbose logging shows every OCR read for debugging, but normal updates are minimized to avoid unnecessary Discord changes.  
   - Updates happen roughly every few seconds (controlled by `update_interval` in `config.json`). Typically, your Discord status reflects a location change within 2–4.5 seconds.

5. **Misreads & Safety:**  
   - Some unusual OCR outputs might still appear temporarily, but the bot is designed to minimize false updates.  
   - If you notice its not reading/updating or is having persistent misreads, you can **redefine the OCR region** using F10.

---

## How To Run This Program

### Option 1: Run the Executable
Simply launch **TCUStatus.exe**. No additional dependencies are required.

### Option 2: Run the Python Source File
If you prefer to run the script directly (`TcuStatus.py`), you will need to install the following Python dependencies:

```bash
pip install pyautogui pygetwindow pytesseract pillow keyboard pypresence
```

Then run:

```bash
python TcuStatus.py
```

### Option 3: Compiling From Source
To compile the `.exe` from source you need the following commands:
```bash
pip install pyinstaller
```

to test it installed correctly, run the following command:
```bash
pyinstaller --version
```

then run this command to compile from the source:
```bash
pyinstaller --onefile --icon="TheCrewUnlimited.ico" --add-data "Tesseract-OCR;Tesseract-OCR" TcuStatus.py
```


---

## Terminal Hotkeys
> NOTE: Make sure your terminal is focused before pressing any F-key.

- **F9**   - Reload the language files (debug)  
- **F10**  - Redefine OCR Region Dynamically  
- **F11**  - Save a screenshot of the current OCR region  
- **F12**  - Exit the program  

---

## Configuration
The program uses a `config.json` file. You can adjust:

- **DISCORD_CLIENT_ID** – Your Discord app ID (required)  
- **update_interval** – How frequently OCR updates, in seconds  
- **ocr_scale** – Scaling factor for OCR accuracy  
- **current_language** – ISO language code for OCR  
- **language_path** – Path to JSON language files  
- **smart_fallback** – Use fallback detection when map OCR is ambiguous  
- **verbose_logging** – Enables extra console logging  
- **Discord presence images & buttons**: `large_image`, `large_text`, `small_image`, `small_text`, `button1_label`, `button1_url`, etc.  

---

## Supported Languages
- EN - English  
- FI - Finnish  
- FR - French  
- DE - German  
- JP - Japanese  
- NO - Norwegian  
- IT - Italian  
- PL - Polish  
- ES - Spanish  
- SV - Swedish  
- CS - Czech  
- PT - Portuguese  
- DA - Danish  
- NL - Dutch  

---

## Notes
- Again focus the terminal before using hotkeys.  
- OCR relies on your screen resolution and map location; use **F10** to redefine the OCR if needed.  
- Only necessary tessdata files for selected languages are included to reduce size. 
- You can also compile your own version of the bot using a custom Tesseract-OCR folder if desired.
- Make sure config.json and Language/ folder are in the same directory as the executable
- If running from source, also make sure the `Tesseract-OCR` folder is in the same directory

---

## License

This project bundles **Tesseract OCR**, which is licensed under **Apache License 2.0**.  
The original `LICENSE` file for Tesseract is included in the `Tesseract-OCR/doc/` folder.

The remainder of this project is also licensed under **Apache License 2.0**

---

## Community Links

- [Join the TCU Discord Server](https://discord.gg/tcu)  
- [Check the TCU YouTube Channel](https://youtube.com/@whammy4)


