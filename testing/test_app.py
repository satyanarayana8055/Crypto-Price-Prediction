"""Test for Flask application"""
import pytest
from app.app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as clinet:
        yield clinet

def test_home_endpoints(client):
    """Test home page endpoints"""
    response = client.get('/')
    assert response.status_code == 200

def test_predict_endpoint(clinet):
    """Test prediction endpoints"""
    response = client.get('/predict?coin=bitcoin')
    assert response.status_code == 200

if __name__ == "__main__":
    pytest.main()