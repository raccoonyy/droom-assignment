import json
import random
from datetime import datetime, timedelta

from fastapi import FastAPI

from api.gen_messages import gen_greeting
from api.models import CurrentWeather

app = FastAPI()
ONE_MINUTE = 60


@app.get("/summary")
async def summary(lat: float, lon: float):
    weathers = await get_weathers(lat=lat, lon=lon)
    current_weather = get_current_weather(weathers)

    return {
        "summary": {
            "greeting": gen_greeting(current_weather),
        }
    }


def get_current_weather(data):
    now = datetime.now()
    return [
        CurrentWeather(**datum) for datum in data
        if -ONE_MINUTE < int(now.timestamp()) - datum['timestamp'] < ONE_MINUTE
    ][0]


async def get_weathers(lat: float, lon: float):
    return json.loads(get_mock_response())


def get_mock_response():
    now = datetime.now()

    results = [{"timestamp": (now.timestamp()), "code": 2, "temp": 38, "rain1h": 22}]

    return json.dumps(results)
