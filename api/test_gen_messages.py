from unittest import TestCase

from parameterized import parameterized

from api.gen_messages import gen_greeting, gen_temperature, gen_heads_up
from api.models import CurrentWeather, HistoricalWeather, ForecastWeather


class TestMessages(TestCase):
    @parameterized.expand([
        ("폭설이 내리고 있어요.", 3, 100),
        ("눈이 포슬포슬 내립니다.", 3, 99),
        ("폭우가 내리고 있어요.", 2, 100),
        ("비가 오고 있습니다.", 2, 99),
        ("날씨가 약간은 칙칙해요.", 1),
        ("따사로운 햇살을 맞으세요.", 0, 0, 30),
        ("날이 참 춥네요.", 0, 0, 0),
    ])
    def test_gen_greeting(self, text: str, code: int, rain1h: int = 0, temp: float = 20):
        weather = CurrentWeather(code=code, rain1h=rain1h, temp=temp)

        assert gen_greeting(weather) == text

    @parameterized.expand([
        ("어제보다 9도 덜 덥습니다. 최고기온은 15도, 최저기온은 5도 입니다.", [6, 5, 9], 15),
        ("어제보다 8도 더 춥습니다. 최고기온은 14도, 최저기온은 4도 입니다.", [6, 5, 4], 14),
        ("어제보다 5도 더 덥습니다. 최고기온은 20도, 최저기온은 15도 입니다.", [20, 19, 18], 15),
        ("어제보다 6도 덜 춥습니다. 최고기온은 20도, 최저기온은 13도 입니다.", [20, 17, 13], 14),
        ("어제와 비슷하게 덥습니다. 최고기온은 20도, 최저기온은 10도 입니다.", [15, 20, 10], 15),
        ("어제와 비슷하게 춥습니다. 최고기온은 20도, 최저기온은 5도 입니다.", [14, 5, 20], 14),
    ])
    def test_gen_temperature(self, text: str, temps: list[float], cur_temp: int):
        current_weather = CurrentWeather(code=0, rain1h=0, temp=cur_temp)
        historical_weathers = [
            HistoricalWeather(timestamp=index, code=0, temp=temp, rain1h=0)
            for index, temp in enumerate(temps)
        ]

        assert gen_temperature(weathers=historical_weathers, current_weather=current_weather) == text

    @parameterized.expand([
        ("내일 폭설이 내릴 수도 있으니 외출 시 주의하세요.", [0, 3, 0, 3, 0, 0, 0, 0]),
        ("눈이 내릴 예정이니 외출 시 주의하세요.", [0, 3, 0, 0, 3, 0, 0, 0]),
        ("폭우가 내릴 예정이에요. 우산을 미리 챙겨두세요.", [0, 2, 0, 2, 0, 0, 0, 0]),
        ("며칠동안 비 소식이 있어요.", [2, 3, 0, 0, 0, 0, 0, 2]),
        ("날씨는 대체로 평온할 예정이에요.", [0, 1, 0, 1, 0, 1, 0, 1]),
    ])
    def test_gen_heads_up(self, text: str, codes: list[int]):
        forecast_weathers = [
            ForecastWeather(timestamp=index, code=code, min_temp=10, max_temp=20, rain=0)
            for index, code in enumerate(codes)
        ]

        assert gen_heads_up(weathers=forecast_weathers) == text
