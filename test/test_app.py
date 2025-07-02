"""Test for Flask application"""
import pytest
from api.app import create_app
from config.config import COINS

@pytest.fixture(scope='module')
def test_client():
    app = create_app('testing')
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(test_client):
    """Test the root dashboard route"""
    response = test_client.get('/')
    assert response.status_code == 200

def test_prediction_page(test_client):
    response = test_client.get('prediction')
    assert response.status_code == 200

def test_data_drift_page(test_client):
    response = test_client.get('/data-drift')
    assert response.status_code == 200

def test_settings_page(test_client):
    response = test_client.get('/settings')
    assert response.status_code == 200

@pytest.mark.parametrize("coin", COINS)
def test_get_supported_coins(test_client):
    response = test_client.get('/api/coins')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert all('id' in coin for coin in data)

@pytest.mark.parametrize("coin", COINS)
def test_get_prediction(test_client, coin):
    response = test_client.get(f'/api/predict/{coin}')
    assert response.status_code in (200, 500)
    data = response.get_json()
    assert isinstance(data, dict)

def test_get_model_metrics(test_client, coin):
    response = test_client.get(f'/api/model-metrics/{coin}')
    assert response.status_code in (200, 500)
    data = response.get_json()
    assert isinstance(data, dict)
