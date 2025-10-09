# Changelog

## v0.9.0
- You no longer have to install Tesseract manually due to a bug.
- Fixed `F9`: now reloads everything properly, including the mains.

## v0.9.1
- Fixed accidental duplicates in the code causing unintended side effects.
- Fixed the **README** being out of date.

## v0.9.2
- Fixed an **EXE** compile error: "`Paths Not Specified`".

## v0.9.5
- Fixed verbose logging not working entirely (whoops).
- Started compiling a GitHub release.
- Updated the **README**.
- Fixed the **EXE** not using its embedded Tesseract-OCR folder when running.

## v0.9.6
- Fixed more **EXE** compile errors.
- Made the **OCR** more reliable by default.
- Fixed the `F9` toggle not having a fail exception.

## v0.9.7
- Made the transitional overrides more accurate
- Added A better discord update check (To avoid updates when they arent needed)
- Fixed another compile error

## v0.9.8
- Fixed the script being hard to read, cleaned up code, etc
- Fixed `F11` not capturing & saving correctly
- Fixed and made it more obvious when verbrose logging was enabled 

## v0.9.9
- Fixed pushing unneciary discord updates
- Fixed console logging showing duplicates (unless verbrose logging is enabled)
- Made the transitional override more robust for more edge cases
- Fixed the fact i missed a ton of locations throughout the entire map (seriously its confusing)
- Added `F6` (Toggle Area Time)
- Added `F7` (Toggle Images Based On Area)
- Added `F8` Key (Toggle Verbrose)
- Fixed a bug i introduced with how the language file is loaded
- Fixed `F6` (Typo)
- Fixed `F11` & made it more human readable
- Fixed the grandcanyon not having its own area (seriously why is the areas in this game so weird)
- Added Polish (mainly for my 2 polish testers)
- Fixed `F12` triggering screenshot on close (For Steam Users)
- Fixed `F7` not repecting the current language
- Fixed Discord getting un-needed updates
- Fixed Verbrose logging not logging all changes, even if Discord wasn't updated
- Fixed the **OCR** check to be more consistant and smarter
- Removed **SMART_FALLBACK** toggle (deprecicated, this is now always used in verbrose logging)
- Changed config keys from `F-Keys` to `Num Keys` for accessability
- Added prompting the user in the terminal to input config values on invalid or Missing values
- Fixed errors relating to new exit handling

## v0.9.9 hotfix 1
- **Added WR Hud Support!**
- Fixed the program unexpectedly crashing if discord isn't running. throws an error and exits gracefully.
- Fixed log files from _maybe_ crashing the program if the log file was locked, or the disc is getting full.
- Fixed arrow keys and a few other keys firing the top row number key functions
- Fixed the capture function now that theres 2 huds
- Added 8 (switch capturing hud on the fly) and moved 8 to 9 (exit)
- Added Russian

## 0.9.9 Hotfix 2

- Removed the embedded `tessdata` folder; required language files are now downloaded at runtime.  
- Automatically uses the most accurate model for each language. [(See Notes)](#notes)  
- Reduced errors and issues on exiting an overlay.  
- Resolved problems when updating or reloading the language file.  
- Proper fallback and exception reporting if a tessdata download fails.
- **Made OCR Even More Reliable!**
- Updated startup message to be more friendly to read

## Notes

1. **Manual tessdata selection**:  
   If you prefer a different tessdata model than the one automatically chosen, you can manually download the traineddata file and place it in your `tessdata` folder from one of the official repositories:  
   - [tessdata-fast](https://github.com/tesseract-ocr/tessdata_fast) - **faster**, but is slightly less accurate.  
   - [tessdata](https://github.com/tesseract-ocr/tessdata) - balanced for speed and accuracy.  
   - [tessdata_best](https://github.com/tesseract-ocr/tessdata_best) - **slower**, but has the highest accuracy.

---
<br>

**Note:** there are versions from before v0.9, but i did not start logging changes until version v0.9
