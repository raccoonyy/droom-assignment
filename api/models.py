from pydantic import BaseModel


class CurrentWeather(BaseModel):
    code: int
    temp: float
    rain1h: int
