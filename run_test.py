import os
import sys
import django

sys.path.append('f:/47Docs')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lughalink.settings')
django.setup()

from translator.services import PDFService

input_pdf = 'f:/47Docs/table_test.pdf'
output_pdf = 'table_test_translated.pdf'
target_lang = 'Swahili' 

print(f"Translating {input_pdf}...")
try:
    output_path = PDFService.translate_pdf_preserve_layout(input_pdf, output_pdf, target_lang)
    print(f"Translation successful: {output_path}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
