import os
import sys
from deep_translator import GoogleTranslator

try:
    langs = GoogleTranslator().get_supported_languages(as_dict=True)
    print("Supported Languages:")
    for name, code in langs.items():
        print(f"{name}: {code}")
except Exception as e:
    print(f"Error: {e}")
