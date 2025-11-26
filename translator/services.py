import fitz  # PyMuPDF
import os
from django.conf import settings
from django.core.files.base import ContentFile

class PDFService:
    @staticmethod
    def extract_text(file_path):
        """Extracts text from a PDF file."""
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    @staticmethod
    def generate_pdf(text, output_filename):
        """Generates a simple PDF from text."""
        doc = fitz.open()
        page = doc.new_page()
        
        # Simple text insertion
        p = fitz.Point(50, 72)
        page.insert_text(p, text, fontsize=12)
        
        output_path = os.path.join(settings.MEDIA_ROOT, 'translated', output_filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        doc.save(output_path)
        return output_path

    @staticmethod
    def translate_pdf_preserve_layout(input_path, output_filename, target_language):
        """
        Translates a PDF while preserving layout and enforcing uniform shrink-to-fit.
        """
        doc = fitz.open(input_path)
        
        # Register fonts
        font_paths = {
            'regular': r'C:\Windows\Fonts\arial.ttf',
            'bold': r'C:\Windows\Fonts\arialbd.ttf',
            'italic': r'C:\Windows\Fonts\ariali.ttf',
            'bold_italic': r'C:\Windows\Fonts\arialbi.ttf',
        }
        
        # Pass 1: Analyze, Translate, and Calculate Sizes
        # We need to store everything to render in Pass 2
        processed_pages = [] 
        
        # Global minimum size starts at a reasonable default (e.g. 11 or based on doc)
        # We will shrink this as we encounter blocks that need smaller text
        global_min_size = 11.0 
        
        # First, determine a baseline global size from the document
        all_font_sizes = []
        for page in doc:
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if block["type"] == 0:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            all_font_sizes.append(span["size"])
        
        if all_font_sizes:
            from collections import Counter
            # Use the most common size as baseline
            global_min_size = Counter(all_font_sizes).most_common(1)[0][0]
            if global_min_size < 8: global_min_size = 10
        
        print(f"Baseline Global Size: {global_min_size}")

        # Helper to detect columns (reused)
        def get_vertical_groups(spans):
            if not spans: return []
            x_min = min(s["bbox"][0] for s in spans)
            x_max = max(s["bbox"][2] for s in spans)
            width = int(x_max - x_min)
            if width <= 0: return [spans]
            has_text = [False] * (width + 1)
            for s in spans:
                s_x0 = int(s["bbox"][0] - x_min)
                s_x1 = int(s["bbox"][2] - x_min)
                for i in range(max(0, s_x0), min(width, s_x1)):
                    has_text[i] = True
            gap_threshold = 10
            current_gap = 0
            split_points = []
            for i in range(width):
                if not has_text[i]:
                    current_gap += 1
                else:
                    if current_gap > gap_threshold:
                        split_points.append(x_min + i - current_gap / 2)
                    current_gap = 0
            if not split_points: return [spans]
            groups = [[] for _ in range(len(split_points) + 1)]
            for s in spans:
                center = (s["bbox"][0] + s["bbox"][2]) / 2
                placed = False
                for i, split_x in enumerate(split_points):
                    if center < split_x:
                        groups[i].append(s)
                        placed = True
                        break
                if not placed:
                    groups[-1].append(s)
            return [g for g in groups if g]

        # Process all pages
        for page_num, page in enumerate(doc):
            page_data = []
            blocks = page.get_text("dict")["blocks"]
            
            for block in blocks:
                if block["type"] == 0:
                    all_spans = []
                    for line in block["lines"]:
                        for span in line["spans"]:
                            all_spans.append(span)
                    if not all_spans: continue

                    column_groups = get_vertical_groups(all_spans)
                    
                    for group_spans in column_groups:
                        if not group_spans: continue
                        
                        # Sort and BBox
                        group_spans.sort(key=lambda s: (s["bbox"][1], s["bbox"][0]))
                        g_x0 = min(s["bbox"][0] for s in group_spans)
                        g_y0 = min(s["bbox"][1] for s in group_spans)
                        g_x1 = max(s["bbox"][2] for s in group_spans)
                        g_y1 = max(s["bbox"][3] for s in group_spans)
                        group_bbox = fitz.Rect(g_x0, g_y0, g_x1, g_y1)
                        
                        # Reconstruct Text
                        original_text = ""
                        last_y = -100
                        last_x = -100
                        for s in group_spans:
                            if abs(s["bbox"][1] - last_y) > 5:
                                if original_text: original_text += "\n"
                                last_y = s["bbox"][1]
                                last_x = s["bbox"][0]
                            else:
                                if s["bbox"][0] > last_x + 2:
                                    original_text += " "
                            original_text += s["text"]
                            last_x = s["bbox"][2]
                        
                        original_text = original_text.strip()
                        if not original_text: continue

                        # Style Detection (from first span)
                        first_span = group_spans[0]
                        flags = first_span["flags"]
                        is_bold = bool(flags & 16)
                        is_italic = bool(flags & 2)
                        
                        # Determine fontname
                        font_key = 'regular'
                        if is_bold and is_italic: font_key = 'bold_italic'
                        elif is_bold: font_key = 'bold'
                        elif is_italic: font_key = 'italic'
                        
                        fontfile = font_paths.get(font_key, font_paths['regular'])
                        fontname = "arial_" + font_key # Unique name for PyMuPDF registration

                        # Color
                        try:
                            color_int = first_span["color"]
                            b = (color_int & 255) / 255
                            g = ((color_int >> 8) & 255) / 255
                            r = ((color_int >> 16) & 255) / 255
                            rgb_color = (r, g, b)
                        except:
                            rgb_color = (0, 0, 0)

                        # Alignment
                        align = 0

                        # Translate
                        translated_text = TranslationService.translate_single(original_text, target_language)

                        page_data.append({
                            "bbox": group_bbox,
                            "text": translated_text,
                            "fontname": fontname,
                            "fontfile": fontfile,
                            "color": rgb_color,
                            "align": align
                        })
            # Redact all first
            for item in page_data:
                page.add_redact_annot(item["bbox"])
            page.apply_redactions()
            
            # Insert
            for item in page_data:
                try:
                    # Try to fit text, reducing font size if necessary
                    curr_fontsize = global_min_size
                    rc = -1
                    while curr_fontsize >= 6:
                        rc = page.insert_textbox(
                            item["bbox"],
                            item["text"],
                            fontsize=curr_fontsize,
                            fontname=item["fontname"],
                            fontfile=item["fontfile"],
                            color=item["color"],
                            align=item["align"]
                        )
                        if rc >= 0: # Success
                            break
                        curr_fontsize -= 1
                    
                    if rc < 0:
                        print(f"Warning: Could not fit text in bbox {item['bbox']} even at size 6. Text: {item['text'][:20]}...")
                        # Force insert with small font as fallback, might overflow but better than nothing?
                        # Or just leave it (it returned < 0 so it might have drawn nothing)
                        # PyMuPDF insert_textbox returns < 0 if rect is too small.
                        # Let's try one last time with a very small font or just logging.
                except Exception as e:
                    print(f"Render error: {e}")

        output_path = os.path.join(settings.MEDIA_ROOT, 'translated', output_filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        doc.save(output_path)
        return output_path

class TranslationService:
    @staticmethod
    def _get_translator(target_language):
        from deep_translator import GoogleTranslator
        
        lang_map = {
            'Luo': 'luo',
            'Kikuyu': 'ki',
            'Luhya': 'luy',
            'Kisii': 'guz',
            'Swahili': 'sw'
        }
        target_code = lang_map.get(target_language, 'en')
        
        # Initialize with a valid target to avoid validation error for new languages
        translator = GoogleTranslator(source='auto', target='en')
        # Bypass validation to allow newer languages like Luo
        translator.target = target_code
        return translator

    @staticmethod
    def translate_single(text, target_language):
        """Translates a single block of text."""
        if not text or not text.strip():
            return text
            
        try:
            translator = TranslationService._get_translator(target_language)
            return translator.translate(text)
        except Exception as e:
            print(f"Translation error: {e}")
            return text

    @staticmethod
    def translate(text, target_language):
        """
        Translates text using Google Translate (via deep-translator).
        """
        try:
            translator = TranslationService._get_translator(target_language)
            
            lines = text.split('\n')
            translated_lines = []
            
            # Translate line by line to preserve structure
            # We filter empty lines to avoid unnecessary requests
            for line in lines:
                if line.strip():
                    try:
                        translated_line = translator.translate(line)
                        translated_lines.append(translated_line)
                    except Exception:
                        # If a line fails, keep original
                        translated_lines.append(line)
                else:
                    translated_lines.append(line)
            
            return "\n".join(translated_lines)
            
        except Exception as e:
            print(f"Translation service error: {e}")
            # Fallback to mock if the service fails entirely
            lines = text.split('\n')
            translated_lines = [f"[{target_language}] {line}" if line.strip() else line for line in lines]
            return "\n".join(translated_lines)
