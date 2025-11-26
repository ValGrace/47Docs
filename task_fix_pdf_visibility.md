# Task: Fix PDF Translation Visibility

## Status
- [x] Analyze the issue (text wiped out).
- [x] Create implementation plan.
- [x] Modify `translator/services.py` to implement dynamic font scaling.
- [ ] Verify the fix (User to test).

## Context
The user reported that translated PDFs only showed the title and first subtitle. The rest was blank. This was likely due to `insert_textbox` failing when the translated text (or the enforced font size) didn't fit in the original bounding box.

## Changes
- Updated `translator/services.py`: `translate_pdf_preserve_layout` now loops to reduce font size if `insert_textbox` returns a failure code (< 0).

## Next Steps
- Ask the user to retry the translation.
