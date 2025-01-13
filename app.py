from flask import Flask, jsonify, request , render_template
import json

app = Flask(__name__)

# Load dataset
with open('datasets/translations.json', 'r') as file:
    dataset = json.load(file)





@app.route('/')
def landing():
    message = "Hello, this message is dynamic!"
    return render_template('index.html', message=message)





@app.route('/translate/<path:translation_type>', methods=['GET'])
def translate(translation_type):
    # Check if translation type exists
    translations = dataset.get(translation_type)
    if not translations:
        return jsonify({"error": f"Invalid translation type: {translation_type}"}), 400

    # Get the word parameter and check if it's provided
    word = request.args.get('word')
    if not word:
        return jsonify({"error": "Missing 'word' query parameter"}), 400

    # Attempt to fetch the translation (case-insensitive)
    translation = translations.get(word.lower())
    if not translation:
        return jsonify({"error": f"Translation for '{word}' not found"}), 404

    return jsonify({"word": word, "translation": translation})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
