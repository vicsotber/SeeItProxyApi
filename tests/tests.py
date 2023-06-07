import pytest
from flask import Flask
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_analizar_imagen(client):
    # Create a sample image file for testing
    image_data =  open('./tests/test_image.jpg', 'rb')

    # Make a POST request to the 'analizar_imagen' endpoint
    response = client.post('/analizar_imagen?language=es', data={'imagen': image_data})

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert any other assertions based on the expected response
    assert 'descriptionResult' in response.json
    assert response.json['descriptionResult']['values'][0]['text'] == 'un perro con un frisbee en la hierba'
    assert 'objectsResult' in response.json
    assert response.json['objectsResult']['values'][0]['name'] == 'beagle'
    assert 'tagsResult' in response.json


def test_edge_case_invalid_image_file(client):
        # Creating a test image file with an invalid extension
        test_image = open('./tests/test_image.txt', 'rb')

        # Sending a POST request to the endpoint
        response = client.post('/analizar_imagen?language=es', data={'imagen': test_image})

        # Asserting that the response is a JSON object with the expected error message
        assert response.status_code == 400
        assert response.content_type == 'application/json'
        assert 'error' in response.json
        assert response.json['error']['code'] == 'InvalidRequest'
        assert response.json['error']['innererror']['code'] == 'InvalidImageFormat'
        assert response.json['error']['innererror']['message'] == 'Image format is not valid.'


def test_edge_case_nonexistent_language_parameter(client):
        # Creating a test image file
        test_image = open('./tests/test_image.jpg', 'rb')

        # Sending a POST request to the endpoint with a non-existent language parameter
        response = app.test_client().post('/analizar_imagen?language=abc', data={'imagen': test_image})

        # Asserting that the response is a JSON object with the expected error message
        assert response.status_code == 400
        assert response.content_type == 'application/json'
        assert 'error' in response.json
        assert response.json['error']['code'] == 'InvalidRequest'
        assert response.json['error']['innererror']['code'] == 'NotSupportedLanguage'
        assert response.json['error']['innererror']['message'] == 'The input language is not supported.'

def test_edge_case_empty_image_file(client):
        # Creating a test image file with an invalid extension
        test_image = open('./tests/empty_image.jpg', 'rb')

        # Sending a POST request to the endpoint
        response = client.post('/analizar_imagen?language=es', data={'imagen': test_image})

        # Asserting that the response is a JSON object with the expected error message
        assert response.status_code == 400
        assert response.content_type == 'application/json'
        assert 'error' in response.json
        assert response.json['error']['code'] == 'InvalidRequest'
        assert response.json['error']['message'] == 'The image size is not allowed to be zero or larger than 20971520 bytes.'

def test_edge_case_missing_image_file(client):
        # Making a request to the function with no image
        response = client.post('/analizar_imagen?language=es')

        # Asserting that the response contains the expected error message
        assert response.status_code == 400
        assert response.json == 'No image has been sent'


def test_valid_image_and_default_language(client):
        test_image = open('./tests/test_image.jpg', 'rb')

        # Sending a POST request to the endpoint
        response = client.post('/analizar_imagen', data={'imagen': test_image})

        # Asserting that the response is a JSON object with the result in english (default language value)
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert 'descriptionResult' in response.json
        assert response.json['descriptionResult']['values'][0]['text'] == 'a dog running with a ball in its mouth'
        assert 'objectsResult' in response.json
        assert 'tagsResult' in response.json