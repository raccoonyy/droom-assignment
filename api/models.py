from pydantic import BaseModel


class CurrentWeather(BaseModel):
    code: int
    temp: float
    rain1h: int


class HistoricalWeather(BaseModel):
    timestamp: int
    code: int
    temp: float
    rain1h: int


class ForecastWeather(BaseModel):
    timestamp: int
    code: int
    min_temp: float
    max_temp: float
    rain: int
