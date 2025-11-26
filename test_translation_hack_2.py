from deep_translator import GoogleTranslator

def test_language_hack(lang_code, lang_name, text="Good morning"):
    try:
        # Initialize with valid target
        translator = GoogleTranslator(source='auto', target='en')
        # Bypass validation
        translator.target = lang_code
        
        res = translator.translate(text)
        print(f"Success for {lang_name} ({lang_code}) translating '{text}': {res}")
    except Exception as e:
        print(f"Failed for {lang_name} ({lang_code}): {e}")

languages = {
    'Luo': 'luo',
    'Kikuyu': 'ki',
    'Luhya': 'luy',
    'Kisii': 'guz',
    'Swahili': 'sw'
}

for name, code in languages.items():
    test_language_hack(code, name)
