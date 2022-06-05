import json
from unittest.mock import patch

from fastapi.testclient import TestClient

from api.bot import app, get_mock_response, get_current_weather
from api.models import CurrentWeather

client = TestClient(app)


def test_get_current_weather():
    current_weather = get_current_weather(json.loads(get_mock_response()))

    assert isinstance(current_weather, CurrentWeather)


@patch('api.bot.get_weathers')
def test_summary(mock_api):
    mock_api.return_value = json.loads(get_mock_response())
    response = client.get('/summary')
    assert response.status_code == 400

    response = client.get('/summary', params={'lat': 91, 'lon': 180})
    assert response.status_code == 400

    response = client.get('/summary', params={'lat': 90, 'lon': 181})
    assert response.status_code == 400

    response = client.get('/summary', params={'lat': 37.5, 'lon': 127})
    assert response.status_code == 200
    assert response.json()['summary']['greeting'] != ''
