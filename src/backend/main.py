from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import easyocr
from googletrans import Translator

app = Flask(__name__)
CORS(app)
translator = Translator()
reader = easyocr.Reader(['en', 'hin', 'ben', 'tel', 'tam', 'kan', 'fra', 'deu', 'spa', 'chi_sim', 'rus'])



def perform_translation(text, target_language):
    translation = translator.translate(text, dest=target_language)
    result = {
        'original_text': text,
        'translated_text': translation.text,
        'source_language': translation.src,
        'target_language': target_language
    }
    return result

def perform_ocr(image):
    ocr_result = reader.readtext(image)
    ocr_text = ' '.join([result[1] for result in ocr_result])
    return ocr_text

def perform_ocr_and_translation(image, target_language):
    # Perform OCR on the image
    ocr_text = perform_ocr(image)

    # Perform translation
    translation_result = perform_translation(ocr_text, target_language)

    return translation_result

@app.route('/translate', methods=['POST'])
def translate_text():
    try:
        data = request.get_json()

        if 'text' not in data or 'target_language' not in data:
            return jsonify({'error': 'Missing required fields'}), 400

        text_to_translate = data['text']
        target_language = data['target_language']

        result = perform_translation(text_to_translate, target_language)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/translate-image', methods=['POST'])
def translate_image():
    try:
        # Check if the request contains the necessary fields
        if 'image' not in request.files or 'target_language' not in request.form:
            return jsonify({'error': 'Missing required fields'}), 400

        # Get the image file and target language from the request
        image_file = request.files['image']
        target_language = request.form['target_language']

        # Validate if the target language is supported
        if target_language not in supported_languages:
            return jsonify({'error': 'Unsupported target language'}), 400

        # Open the image using Pillow
        image = Image.open(image_file)

        # Perform OCR and translation
        result = perform_ocr_and_translation(image, target_language)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
