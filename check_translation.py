import os
import sys
import django

sys.path.append('f:/47Docs')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lughalink.settings')
django.setup()

from translator.services import TranslationService

text = "Hello world"
target = "Swahili"

print(f"Testing translation of '{text}' to {target}...")
try:
    translated = TranslationService.translate_single(text, target)
    print(f"Result: '{translated}'")
    
    if translated == text:
        print("WARNING: Text was NOT translated (returned original).")
    else:
        print("SUCCESS: Text was translated.")
        
except Exception as e:
    print(f"CRITICAL ERROR: {e}")
