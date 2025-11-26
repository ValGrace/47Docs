import os
import sys
import django

sys.path.append('f:/47Docs')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lughalink.settings')
django.setup()

from translator.services import TranslationService

text = "How are you?"
target = "kikuyu" # Try full name lower case

print(f"Testing translation of '{text}' to {target}...")
try:
    # Bypass service map to test direct code
    from deep_translator import GoogleTranslator
    translator = GoogleTranslator(source='auto', target=target)
    translated = translator.translate(text)
    print(f"Result: '{translated}'")
    
    if translated == text:
        print("WARNING: Text was NOT translated (returned original).")
    else:
        print("SUCCESS: Text was translated.")
        
except Exception as e:
    print(f"CRITICAL ERROR: {e}")
