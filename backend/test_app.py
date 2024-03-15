from fastapi.testclient import TestClient
from numbers import Number

from .app import app
from .utils import init_logging

client = TestClient(app)
log = init_logging()

def test_image_inference():
    with open('data/chest_xray/test/NORMAL/IM-0001-0001.jpeg', 'rb') as image:
        response = client.post('/predict', files={'file': ('filename', image, 'image/jpeg')})
    content = response.json()
    log.debug(content)
    assert response.status_code == 200
    assert 'prediction' in content
    assert isinstance(content['prediction'], bool)
    assert isinstance(content['confidence'], Number)
    assert content['confidence'] >= 0 and content['confidence'] <= 1