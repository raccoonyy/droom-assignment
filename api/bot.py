import json
import random
from datetime import datetime, timedelta

from fastapi import FastAPI, Query
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

from api.gen_messages import gen_greeting, gen_temperature
from api.models import CurrentWeather, HistoricalWeather

app = FastAPI()
ONE_MINUTE = 60


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.get("/summary")
async def summary(
        lat: float = Query(ge=-90, lt=90),
        lon: float = Query(ge=-180, lt=180)
):
    weathers = await get_weathers(lat=lat, lon=lon)
    current_weather = get_current_weather(weathers)
    historical_weathers = get_historical_weathers(weathers)

    return {
        "summary": {
            "greeting": gen_greeting(current_weather),
            "temperature": gen_temperature(historical_weathers, current_weather)
        }
    }


def get_current_weather(data):
    now = datetime.now()
    return [
        CurrentWeather(**datum) for datum in data
        if -ONE_MINUTE < int(now.timestamp()) - datum['timestamp'] < ONE_MINUTE
    ][0]


def get_historical_weathers(data):
    now = datetime.now()
    return [
        HistoricalWeather(**datum) for datum in data
        if ONE_MINUTE < int(now.timestamp()) - datum['timestamp']
    ]


async def get_weathers(lat: float, lon: float):
    return json.loads(get_mock_response())


def get_mock_response():
    now = datetime.now()

    results = [{"timestamp": (now.timestamp()), "code": 2, "temp": 20, "rain1h": 22}]

    # historical weathers
    for i in range(-6, -25, -6):
        results.append({
            "timestamp": int((now + timedelta(hours=i)).timestamp()),
            "code": random.choice([0, 1, 2, 3]),
            "temp": random.choice(range(-20, 40)),
            "rain1h": random.choice(range(0, 110))
        })


    return json.dumps(results)
