from flask import Flask, request, jsonify, render_template
import os
from flask.helpers import send_from_directory
import requests

import base64
#from dotenv import load_dotenv

app = Flask(__name__)
app.static_folder = 'static'
#load_dotenv('.env')

app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg']

subscription_key = os.environ.get('AZURE_API_KEY')
endpoint = os.environ.get('AZURE_ENDPOINT')

images_folder = os.path.join (os.path.dirname(os.path.abspath(__file__)), "images_folder")

@app.route('/analizar_imagen', methods=['POST'])
def analizar_imagen():
    language = request.args.get('language')
    try:
        imagen = request.files['imagen'].read()
    except Exception:
        return jsonify('No image has been sent'),400
    
    url = endpoint + 'computervision/imageanalysis:analyze'

    if subscription_key is None:
        return jsonify('There has been an error obtaining the subscription API Key'), 401

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-Type': 'application/octet-stream'
    }


    params = {
        'api-version': '2022-10-12-preview',
        'features': 'Description,Objects,Tags',
        'language': language
    }


    response = requests.post(url, headers=headers, params=params, data=imagen)

    resultado = response.json()

    if 'error' in resultado:
        return jsonify(resultado),400
    
    # Devolver el resultado como una respuesta HTTP en formato JSON
    return jsonify(resultado)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run()