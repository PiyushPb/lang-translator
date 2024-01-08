from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import pytesseract
from googletrans import Translator
from io import BytesIO

app = Flask(__name__)
CORS(app)
translator = Translator()


supported_languages = ["hi", "bn", "ta", "te", "mr", "es", "fr", "de", "ja", "ru", "en"] # for langauge translation api
language_mapping = {
    "hi": "hin",
    "bn": "ben",
    "ta": "tam",
    "te": "tel",
    "mr": "mar",
    "es": "spa",
    "fr": "fra",
    "de": "deu",
    "ja": "jpn",
    "ru": "rus",
    "en": "eng"
} # for pytessaract


def translate(text, target_language):
    translation = translator.translate(text, dest=target_language)
    result = {
        'original_text': text,
        'translated_text': translation.text,
        'source_language': translation.src,
        'target_language': target_language
    }
    return result


def ocr_and_translate(image, source_language, target_language):
    image = Image.open(BytesIO(image.read()))
    ocr_text = pytesseract.image_to_string(image, lang=source_language)

    translated_result = translate(ocr_text, target_language)

    return translated_result



@app.route('/translate', methods=['POST'])
def translate_text():
    try:
        data = request.get_json()

        if 'text' not in data or 'target_language' not in data:
            return jsonify({'error': 'Missing required fields'}), 400

        text_to_translate = data['text']
        target_language = data['target_language']

        result = translate(text_to_translate, target_language)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/image-translate', methods=['POST'])
def image_translate_api():
    try:
        if 'image' not in request.files or 'target_language' not in request.form or 'source_language' not in request.form:
            return jsonify({'error': 'Missing required fields'}), 400
        
        image_file = request.files['image']
        target_language = request.form['target_language']
        source_language = request.form['source_language']

        if target_language not in supported_languages or source_language not in supported_languages:
            return jsonify({'error': 'Unsupported target language'}), 400
        

        image = request.files['image']

        result = ocr_and_translate(image, source_language, target_language)
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True, port=8000)
