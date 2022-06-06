from datetime import datetime

from fastapi import FastAPI, Query
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

from api.gen_messages import gen_greeting, gen_temperature, gen_heads_up
from api.models import CurrentWeather, HistoricalWeather, ForecastWeather
from api.weather_api import get_weathers

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
    forecast_weathers = get_forecast_weathers(weathers)

    return {
        "summary": {
            "greeting": gen_greeting(current_weather),
            "temperature": gen_temperature(historical_weathers, current_weather),
            "heads-up": gen_heads_up(forecast_weathers),
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


def get_forecast_weathers(data):
    now = datetime.now()
    return [
        ForecastWeather(**datum) for datum in data
        if now.timestamp() < datum['timestamp']
    ]


