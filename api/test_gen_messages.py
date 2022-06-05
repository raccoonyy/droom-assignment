from unittest import TestCase

from parameterized import parameterized

from api.gen_messages import gen_greeting, gen_temperature
from api.models import CurrentWeather, HistoricalWeather


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
        ('어제보다 9도 덜 덥습니다. 최고기온은 15도, 최저기온은 5도 입니다.', [6, 5, 9], 15),
        ('어제보다 8도 더 춥습니다. 최고기온은 14도, 최저기온은 4도 입니다.', [6, 5, 4], 14),
        ('어제보다 5도 더 덥습니다. 최고기온은 20도, 최저기온은 15도 입니다.', [20, 19, 18], 15),
        ('어제보다 6도 덜 춥습니다. 최고기온은 20도, 최저기온은 13도 입니다.', [20, 17, 13], 14),
        ('어제와 비슷하게 덥습니다. 최고기온은 20도, 최저기온은 10도 입니다.', [15, 20, 10], 15),
        ('어제와 비슷하게 춥습니다. 최고기온은 20도, 최저기온은 5도 입니다.', [14, 5, 20], 14),
    ])
    def test_gen_temperature(self, text: str, temps: list[int], cur_temp: int):
        current_weather = CurrentWeather(code=0, rain1h=0, temp=cur_temp)
        historical_weathers = [
            HistoricalWeather(timestamp=index, code=0, temp=temp, rain1h=0)
            for index, temp in enumerate(temps)
        ]

        assert gen_temperature(weathers=historical_weathers, current_weather=current_weather) == text
