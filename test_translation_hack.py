from deep_translator import GoogleTranslator

def test_language_hack(lang_code, lang_name):
    try:
        # Initialize with valid target
        translator = GoogleTranslator(source='auto', target='en')
        # Bypass validation
        translator.target = lang_code
        
        res = translator.translate("Hello world")
        print(f"Success for {lang_name} ({lang_code}): {res}")
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
