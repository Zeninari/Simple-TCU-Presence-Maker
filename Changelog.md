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

---

**Note:** there are versions from before v0.9, but i did not start logging changes until version v0.9
