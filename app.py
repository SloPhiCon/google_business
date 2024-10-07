import os
from flask import Flask, request, jsonify
import deepl

# Replace with your DeepL API auth key
auth_key = "82a64fae-73d4-4739-9935-bbf3cfc15010"
translator = deepl.Translator(auth_key)

# Comprehensive language mapping
language_mapping = {
    "Arabic": "AR",
    "Bulgarian": "BG",
    "Czech": "CS",
    "Danish": "DA",
    "German": "DE",
    "Greek": "EL",
    "English": "EN",  # General English
    "English (British)": "EN-GB",
    "English (American)": "EN-US",
    "Spanish": "ES",
    "Estonian": "ET",
    "Finnish": "FI",
    "French": "FR",
    "Hungarian": "HU",
    "Indonesian": "ID",
    "Italian": "IT",
    "Japanese": "JA",
    "Korean": "KO",
    "Lithuanian": "LT",
    "Latvian": "LV",
    "Norwegian Bokmål": "NB",
    "Dutch": "NL",
    "Polish": "PL",
    "Portuguese": "PT",  # General Portuguese
    "Portuguese (Brazilian)": "PT-BR",
    "Portuguese (European)": "PT-PT",
    "Romanian": "RO",
    "Russian": "RU",
    "Slovak": "SK",
    "Slovenian": "SL",
    "Swedish": "SV",
    "Turkish": "TR",
    "Ukrainian": "UK",
    "Chinese": "ZH",  # General Chinese
    "Chinese (Simplified)": "ZH-HANS",
    "Chinese (Traditional)": "ZH-HANT"
}

# Define the function to translate text using DeepL API
def translate_text(text, target_lang_name, source_lang_name=None, formality='default', preserve_formatting=True):
    # Validate required parameters
    if not text or not target_lang_name:
        raise ValueError("Missing required parameters: 'text' and 'target_lang'.")

    # Convert language names to codes
    source_lang = language_mapping.get(source_lang_name) if source_lang_name else None
    target_lang = language_mapping.get(target_lang_name)

    if target_lang is None:
        raise ValueError(f"Invalid target language: '{target_lang_name}'. Please provide a valid language name.")

    try:
        # Perform the translation
        result = translator.translate_text(
            text,
            source_lang=source_lang,
            target_lang=target_lang,
            formality=formality,
            preserve_formatting=preserve_formatting
        )

        # Return the translated text
        return result.text

    except Exception as e:
        raise RuntimeError(f"Translation failed: {str(e)}")

# Initialize Flask app
app = Flask(__name__)

# Define the root endpoint
@app.route('/')
def say_hi():
    return 'Hi! This is the addition and translation service.'

# Define an endpoint for adding two numbers
@app.route('/add', methods=['POST'])
def add_numbers():
    # Get JSON data from the request
    data = request.get_json()

    # Extract numbers from the JSON data
    num1 = data.get('num1')
    num2 = data.get('num2')

    # Check if both numbers are provided and are valid
    if num1 is None or num2 is None:
        return jsonify({'error': 'Please provide both num1 and num2'}), 400
    if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
        return jsonify({'error': 'Both num1 and num2 must be numbers'}), 400

    # Perform addition
    result = num1 + num2

    # Return the result as JSON
    return jsonify({'result': result})

# Define an endpoint for text translation
@app.route('/translate', methods=['POST'])
def translate():
    # Get JSON data from the request
    data = request.get_json()

    # Extract required fields from JSON
    text = data.get('text')
    target_lang = data.get('target_language')
    source_lang = data.get('source_language', None)  # Optional
    formality = data.get('formality', 'default')
    preserve_formatting = data.get('preserve_formatting', True)

    # Validate input
    if not text or not target_lang:
        return jsonify({'error': 'Please provide both text and target_language'}), 400

    try:
        # Perform the translation
        translated_text = translate_text(text, target_lang, source_lang, formality, preserve_formatting)
        return jsonify({'translated_text': translated_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the app
if __name__ == '__main__':
    # Use the environment variable PORT, or default to port 5000 if not set
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
