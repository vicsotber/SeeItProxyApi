from flask import Flask, request, jsonify
import os
import requests

import base64

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg']

subscription_key = os.environ.get('AZURE_API_KEY')
endpoint = os.environ.get('AZURE_ENDPOINT')

images_folder = os.path.join (os.path.dirname(os.path.abspath(__file__)), "images_folder")

@app.route('/analizar_imagen', methods=['POST'])
def analizar_imagen():
    language = request.args.get('language')
    imagen = request.files['imagen'].read()
    url = endpoint + 'computervision/imageanalysis:analyze'

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

    # Devolver el resultado como una respuesta HTTP en formato JSON
    return jsonify(resultado)

if __name__ == '__main__':
    app.run()