# TCU Status Presence Maker

> ⚠️ **Important:**<br>
> - This program does **not** interact with the game directly. It reads your screen to determine your location.<br>
> - **The script doesn't require the original HUD to function, but is recomended**<br>
> **If Running WR UI its recomended to run Xenias "[`Vanilla HUD - Always visible current area`](https://modworkshop.net/mod/54037)"**
> - **ONLY THE CURRENT LANGUAGES ARE SUPPORTED**: EN, PL, RU<br>
> - Borderless window recommended. A User guide is provided for more information under `main`<br>
> - For fullscreen, **ENSURE** native resolution is selected. Set the ocr region in borderless window, and set back to fullscreen.
> OCR **WILL** break if the resolution is set to something that your monitor doesn't support - i.e. Super Resolution

---

## Overview
**TCU Status Presence Maker** displays your current in-game map location from **The Crew Unlimited** as a **Discord Rich Presence** status, updating automatically as you move around the map.

---

# How Updates Work

The program reads your in-game location from the screen and updates your Discord status. Here's how it works:

### 1. **OCR (Optical Character Recognition):**  
   - The bot takes a small screenshot of your map’s HUD text and converts it to characters.

### 2. **Matching Locations:**  
   - First tries an **exact match** against known sub-area names.  
   - If that fails, tries a **partial match** (for small OCR misreads).  
   - If still no match, uses **fuzzy matching**, but only if the first letter matches and the text is very similar.  
   - This ensures minor OCR errors don’t trigger completely wrong updates.

### 3. **Transition Rules:**  
   - Certain area transitions have **special rules** (such as moving to a city from it's surrounding region; entering an area that appears in multiple locations). The bot manages these automatically.

### 4. **Discord Updates:**  
   - The bot only updates Discord when the confirmed location changes.  
   - Verbose logging shows every OCR read for debugging, but normal updates are minimized to avoid unnecessary Discord changes.  
   - Updates happen roughly every few seconds (controlled by `update_interval` in `config.json`). Typically, your Discord status reflects a location change within 2–4.5 seconds.

### 5. **Misreads & Safety:**  
   - Some unusual OCR outputs might still appear temporarily, but the bot is designed to minimize false updates.  
   - If you notice its not reading/updating or is having persistent misreads, you can **redefine the OCR region** using **`5`**.

---

## How To Run This Program

### Step 1: Configure Your Discord Bot
Before running the program, you need to create your **own Discord application** and bot:

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create a new application.  
2. Add a bot to the application and copy its **Client ID**.  
3. Open `config.json` in the program folder and enter your Discord **Client ID** under `DISCORD_CLIENT_ID`.  
4. To use the default images and area rich presence, upload the images from the `Images/` folder to your Discord application under **Rich Presence → Art Assets**. The provided names are already formatted to match the defaults for the `config.json`, so the bot will use them automatically if using the defaults.

### Step 2: If you prefer to use your own images, buttons, & urls, you have two options:

1. Put in the information into the `config.json`.  
2. Use the setup provided by the terminal on first setup (**_or if one is missing or invalid_**) to set what you want to use without having to touch the `config.json`. the only thing you cannot set maually during this process is OCR cordinates, and the update interval.

---

### Option 1: Run the Executable
Simply launch **TCUStatus.exe**. No additional dependencies are required when using the defaults.

### Option 2: Run the Python Source File

### Prerequisite:
TcuStatus requires python to run, if it's not installed go to [Python.Org](https://www.python.org/) and install python

### Instructions:
If you prefer to run the script directly (`TcuStatus.py`), you will need to install the following Python dependencies:

```bash
pip install pyautogui pygetwindow pyrect pytesseract pillow keyboard pypresence rapidfuzz
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
pyinstaller TcuStatus.spec
```


---


### Hotkeys
Some settings can also be toggled in real-time using Number-keys (pressing the key while the terminal is focused is recomended):

- **`Alt+1`** – Toggle "Time Spent in Current Area" (`time_in_area`).  
- **`Alt+2`** – Toggle dynamic large images (`dynamic_large_image`).  
- **`Alt+3`** – Toggle verbose logging (`verbose_logging`).  
- **`Alt+4`** – Reload language files for OCR (debug).  
- **`Alt+5`** – Redefine `WR` OCR Region Dynamically 
- **`Alt+6`** – Redefine `OG` OCR Region Dynamically 
- **`Alt+7`** – Screenshot Current Chosen OCR Region
- **`Alt+8`** – Swap Between Capture Zones (`Wr`;`OG`)  
- **`Alt+9`** – Exit the bot.

---

## Configuration

The program uses a `config.json` file to control settings. You can adjust the following options:

### Discord Bot
- **DISCORD_CLIENT_ID** – Your Discord application’s **Client ID** (required).  
- **large_image** – Default large image key for Discord Rich Presence.  
- **large_text** – Tooltip text for the large image.  
- **small_image** – Small image key for Discord Rich Presence.  
- **small_text** – Tooltip text for the small image.  
- **button1_label / button1_url** – Label and URL for the first Rich Presence button.  
- **button2_label / button2_url** – Label and URL for the second button.

### OCR / Map Detection
- **update_interval** – How often the OCR reads the map, in seconds.  
- **ocr_scale** – Scaling factor for OCR accuracy (higher = more precise).  
- **current_language** – ISO language code for OCR (e.g., `EN`, `PL`).  
- **wr_ocr_region** – `[x, y, width, height]` of the screen region the OCR reads for the WR hud. 
- **ocr_region** – `[x, y, width, height]` of the screen region the OCR reads for the OG hud. 
- **force_hud** - what version of the hud OCR is reading
- **time_in_area** – If `true`, the bot tracks how long you remain in each area.  
- **dynamic_large_image** – If `true`, changes the large image based on the current main area.  
- **verbose_logging** – Enables detailed console logging for debugging.

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
- RU - Russian

---

## Notes
- Focusing on the terminal is recomended before using hotkeys but is not required.
- OCR relies on your screen resolution and map location; use **`5`** or **`6`** to redefine the OCR if needed.
- When screenshotting the OCR region, make sure to **ONLY** include the sub region.
- Tessdata files are downloaded at runtime to reduce file size.
- Make sure `config.json` and Language/ folder are in the same directory as the executable
- If running from source, also make sure the `Tesseract-OCR` folder is in the same directory
- If you run into an issue, open a request

---

## License

This project bundles **Tesseract OCR**, which is licensed under **Apache License 2.0**.  
The original `LICENSE` file for Tesseract is included in the `Tesseract-OCR/doc/` folder.

The remainder of this project is also licensed under **Apache License 2.0**

---

## Community Links

- [Join the TCU Discord Server!](https://discord.gg/tcu)  
- [Check the official TCU YouTube Channel!](https://youtube.com/@whammy4)


