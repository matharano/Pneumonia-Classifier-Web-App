import os, base64
from fastapi.testclient import TestClient
from http import HTTPStatus

from .app import app, Prediction
from .utils import init_logging

client = TestClient(app)
log = init_logging()

test_file_path = 'data/chest_xray/test/NORMAL/IM-0001-0001.jpeg'

def test_image_inference():
    """Check expected behavior with file uploaded"""
    with open(test_file_path, 'rb') as file:
        extension = os.path.splitext(test_file_path)[1][1:]
        response = client.post('/predict', files={'file': (os.path.basename(test_file_path), file, extension)})
    assert response.status_code == HTTPStatus.OK
    Prediction.model_validate(response.json())

def test_encoded_image_inference():
    """Check expected behavior with encoded file in base64"""
    with open(test_file_path, 'rb') as file:
        bytes_file = file.read()
    encoded_file = base64.b64encode(bytes_file)
    extension = os.path.splitext(test_file_path)[1][1:]
    response = client.post('/predict', files={'file': (os.path.basename(test_file_path), encoded_file, extension)})
    assert response.status_code == HTTPStatus.OK
    Prediction.model_validate(response.json())

def test_large_file():
    """Check response to a large file"""
    filepath = 'data/large-image.jpg'
    with open(filepath, 'rb') as file:
        extension = os.path.splitext(filepath)[1][1:]
        response = client.post('/predict', files={'file': (os.path.basename(filepath), file, extension)})
    content = response.json()
    assert response.status_code == HTTPStatus.OK
    Prediction.model_validate(response.json())

def test_without_content():
    """Check response when file is empty"""
    response = client.post('/predict', files={'file': ('IM-0001-0001.jpeg', b'', 'image/jpeg')})
    content = response.json()
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert content['detail'] == 'File is empty'

def test_wrong_file_format():
    """Check response to file other than image"""
    filepath = 'data/README.md'
    with open(filepath, 'rb') as file:
        extension = os.path.splitext(filepath)[1][1:]
        response = client.post('/predict', files={'file': (os.path.basename(filepath), file, extension)})
    content = response.json()
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert content['detail'].startswith('File format not supported')

def test_broken_file():
    """Check response to a broken file"""
    with open(test_file_path, 'rb') as file:
        extension = os.path.splitext(test_file_path)[1][1:]
        encoded_file = file.read(50)
    response = client.post('/predict', files={'file': (os.path.basename(test_file_path), encoded_file, extension)})
    content = response.json()
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert content['detail'].startswith('The file received was corrupted. Check the file and try again.')

def test_get():
    """Check response to a not-implemented method"""
    response = client.get('/predict')
    content = response.json()
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    assert content['detail'] == 'Method Not Allowed'