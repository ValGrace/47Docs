# Implementation Plan - Fix PDF Translation Visibility

The user is experiencing an issue where translated PDFs show only the title and first subtitle, while the rest of the content is "wiped out" (redacted but not replaced). This suggests that the text insertion step is failing for the body content, likely because the target bounding box is too small for the enforced font size.

## User Review Required

> [!IMPORTANT]
> I will be modifying the text insertion logic to dynamically adjust the font size if the text does not fit in the bounding box. This ensures that the translated text (which might be longer than the original) remains visible within the original layout constraints.

- **Action**: Modify `translator/services.py`.
- **Logic**: Check the return value of `insert_textbox`. If it indicates failure (text didn't fit), reduce the font size and retry until it fits or reaches a minimum readable size.

## Proposed Changes

### `translator/services.py`

#### `PDFService.translate_pdf_preserve_layout`

- Current logic uses a fixed `global_min_size` for all text blocks.
- **New Logic**:
    - Keep `global_min_size` as a baseline preference.
    - When calling `page.insert_textbox`:
        - Check the return value.
        - If the text does not fit (return value < 0 or indicating overflow), decrease the `fontsize` in a loop (e.g., decrement by 1 or 0.5) until it fits or hits a minimum threshold (e.g., 6pt).
    - If it still doesn't fit, log a warning but insert what is possible (or leave it as best effort).

## Verification Plan

### Automated Tests
- Create a test script `test_pdf_rendering.py` (mocking the PDF structure or using a sample if possible) to verify that `insert_textbox` logic handles overflow correctly.
- Since I cannot easily generate a complex PDF with PyMuPDF in a script without external assets, I will rely on the user's feedback after patching, but I will add extensive logging to the service to confirm the fix.

### Manual Verification
- The user will run the server and test with their PDF.
- I will check the logs (via `run_command`) to see the "Retrying with font size X" messages.
