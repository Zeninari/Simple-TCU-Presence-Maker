# TCU Status Presence Maker – User Guide

⚠️ **IMPORTANT:** You need to create your own Discord bot and enter its details in the `config.json` file before running this program.  
**NOTE:** The script doesn't require the OG HUD to function, but is recomended.

---

## Setup Notes

- You **must make your own bot** to use this program and enter its information into `config.json`.
- The **buttons** have predefined values but can be changed to your liking in the config.
- There is an **example screenshot** in the `Capture/` folder showing where the OCR region should roughly be (for debugging purposes).
- The OCR is currently configured for **1080p screens**.  
  If your resolution differs, you may need to press the **OCR reconfiguration key `(F10)`** to adjust the region for better results.

---

## Configuration – Key Values

The most important settings in `config.json` are:

### `update_interval`
- **Default:** `4`
- Controls how often (in seconds) the OCR runs.

**Drawbacks:**
- Too low (1–2s): Higher CPU usage, may cause unnecessary stuttering.
- Too high (8–10s): Discord status lags behind your in-game position.

---

### `ocr_scale`
- **Default:** `10`
- Scales the captured OCR region before text recognition to improve accuracy.

**Drawbacks:**
- Too low (2–4): Poor OCR accuracy, more misreads.
- Too high (15+): More CPU usage and slightly slower updates.

---

## Recommended Settings by Resolution  

> ⚠️ **Disclaimer:** These values are suggested defaults only.  
> They are based on scaling logic but remain **untested across most resolutions**.  
> Only the 1080p values are confirmed to work for most users. Feel free to tweak them for best performance on your setup.  

| Resolution      | Suggested `ocr_scale` | Suggested `update_interval` | Notes |
|-----------------|------------------------|-----------------------------|-------|
| **1080p (1920×1080)** | `10–12`  | `3–5` | Default config is tuned for this resolution. |
| **1440p (2560×1440)** | `12–14` | `4–6` | Slightly higher scale improves recognition. |
| **4K (3840×2160)**   | `14–16` | `5–7` | Larger scale needed; longer interval helps reduce CPU load. |
| **Ultrawide (3440×1440 / 5120×1440)** | `11–13` | `5–7` | Similar to 1440p/4K but may need tweaking. |

---

## Table For Tessdata Benifits & Drawbacks

| Model           | Accuracy | Speed (relative) | File Size | Best For / Notes | Trade-offs |
|-----------------|---------|-----------------|-----------|-----------------|-----------|
| **tessdata_fast** | Medium-Low | Fastest | Small (~10–20 MB per language) | Good for English and languages with simple characters. | May misread diacritics or accented characters (é, ç, ñ, etc.). Not recommended for complex languages |
| **tessdata**      | Medium-High | Moderate | Medium (~20–50 MB per language) | Balanced choice for most European languages | Slightly slower than `tessdata_fast`. Handles diacritics better, but not as accurate as `tessdata_best` |
| **tessdata_best** | Highest | Slowest | Large (~50–100 MB per language) | Essential for accuracy-sensitive languages | Slowest to load and process. Larger downloads. | 

### **Performance consideration**:  
- Processing time scales with image size and model complexity. Upscaling images will amplify differences in speed.    

---

## Performance Notes

On my system (**Intel Core i5-13420H**, 8 cores / 12 threads @ 2.1–4.6 GHz), the program typically uses **~0–1% CPU** while running with the default settings (`ocr_scale = 10`, `update_interval = 4`) at **1080p resolution**.  

Performance may vary on lower-end CPUs or at higher resolutions (1440p / 4K), where OCR has to process more pixels, or when using `tessdata_fast` vs `tessdata` & `tessdata_best`

If you experience higher CPU usage, try:  
- Increasing `update_interval` slightly (e.g., from `4` → `6`) to reduce OCR checks per second.  
- Lowering `ocr_scale` if recognition is already accurate enough.
- Tinkering is recomended for advanced users

---

## Tips
- Start with the defaults (`update_interval = 4`, `ocr_scale = 10`).
- If CPU usage is too high → **increase update_interval** or lower ocr_scale.  
- If OCR accuracy is poor → **increase ocr_scale** slightly, or use a higher `tessdata` model at the expense of discord update speed.
- if that also fails try fiddling with the OCR region if needed.
