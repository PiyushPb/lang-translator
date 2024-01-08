from flask import Flask, request, jsonify
from googletrans import Translator

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug=True, port=8000)
