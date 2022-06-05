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
