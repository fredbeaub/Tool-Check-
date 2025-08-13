from flask import Flask, render_template, request, jsonify
from validators.creative_validator import CreativeValidator
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max-length

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_creative():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    ad_type = request.form.get('ad_type')
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    validator = CreativeValidator(file, ad_type)
    result = validator.validate()
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
