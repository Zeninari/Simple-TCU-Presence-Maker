# TCU Status Presence Maker – User Guide

⚠️ **IMPORTANT:** You need to create your own Discord bot and enter its details in the `config.json` file before running this program.

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
- Too low (1–2s): High CPU usage, may cause stuttering.
- Too high (8–10s): Discord status lags behind your in-game position.

---

### `ocr_scale`
- **Default:** `8`
- Scales the captured OCR region before text recognition to improve accuracy.

**Drawbacks:**
- Too low (2–4): Poor OCR accuracy, more misreads.
- Too high (12+): Very CPU-heavy, updates slower.

---

## Recommended Settings by Resolution

| Resolution      | Suggested `ocr_scale` | Suggested `update_interval` | Notes |
|-----------------|------------------------|-----------------------------|-------|
| **1080p (1920×1080)** | `6–8`  | `3–5` | Default config is tuned for this. |
| **1440p (2560×1440)** | `8–10` | `4–6` | Slightly higher scale improves recognition. |
| **4K (3840×2160)**   | `10–12` | `5–7` | Large scale needed; longer interval helps reduce CPU load. |
| **Ultrawide (3440×1440 / 5120×1440)** | `9–11` | `5–7` | Similar to 1440p/4K but may need tweaking. |

---

## Tips
- Start with the defaults (`update_interval = 4`, `ocr_scale = 8`).
- If CPU usage is too high → **increase update_interval** or lower ocr_scale.  
- If OCR accuracy is poor → **increase ocr_scale** slightly.  
