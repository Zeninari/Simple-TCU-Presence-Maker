# TCU Status Presence Maker – User Guide

⚠️ **IMPORTANT:** You need to create your own Discord bot and enter its details in the `config.json` file before running this program.  
**NOTE:** The script requires the OG HUD to function — it will not work otherwise.

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
- **Default:** `8`
- Scales the captured OCR region before text recognition to improve accuracy.

**Drawbacks:**
- Too low (2–4): Poor OCR accuracy, more misreads.
- Too high (12+): More CPU usage and slightly slower updates.

---

## Recommended Settings by Resolution  

> ⚠️ **Disclaimer:** These values are suggested defaults only.  
> They are based on scaling logic but remain **untested across most resolutions**.  
> Only the 1080p values are confirmed to work for most users. Feel free to tweak them for best performance on your setup.  

| Resolution      | Suggested `ocr_scale` | Suggested `update_interval` | Notes |
|-----------------|------------------------|-----------------------------|-------|
| **1080p (1920×1080)** | `6–8`  | `3–5` | Default config is tuned for this resolution. |
| **1440p (2560×1440)** | `8–10` | `4–6` | Slightly higher scale improves recognition. |
| **4K (3840×2160)**   | `10–12` | `5–7` | Larger scale needed; longer interval helps reduce CPU load. |
| **Ultrawide (3440×1440 / 5120×1440)** | `9–11` | `5–7` | Similar to 1440p/4K but may need tweaking. |

---

## Performance Notes

On my system (**Intel Core i5-13420H**, 8 cores / 12 threads @ 2.1–4.6 GHz), the program typically uses **~0–0.6% CPU** while running with the default settings (`ocr_scale = 8`, `update_interval = 4`) at **1080p resolution**.  

Performance may vary on lower-end CPUs or at higher resolutions (1440p / 4K), where OCR has to process more pixels.

If you experience higher CPU usage, try:  
- Increasing `update_interval` slightly (e.g., from `4` → `6`) to reduce OCR checks per second.  
- Lowering `ocr_scale` if recognition is already accurate enough.

---

## Tips
- Start with the defaults (`update_interval = 4`, `ocr_scale = 8`).
- If CPU usage is too high → **increase update_interval** or lower ocr_scale.  
- If OCR accuracy is poor → **increase ocr_scale** slightly.  
