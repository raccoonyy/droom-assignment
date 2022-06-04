from parameterized import parameterized

from api.gen_messages import gen_greeting
from api.models import CurrentWeather


@parameterized.expand([
    ("폭설이 내리고 있어요.", 3, 100),
    ("눈이 포슬포슬 내립니다.", 3, 99),
    ("폭우가 내리고 있어요.", 2, 100),
    ("비가 오고 있습니다.", 2, 99),
    ("날씨가 약간은 칙칙해요.", 1),
    ("따사로운 햇살을 맞으세요.", 0, 0, 30),
    ("날이 참 춥네요.", 0, 0, 0),
])
def test_gen_greeting(text: str, code: int, rain1h: int = 0, temp: float = 20):
    weather = CurrentWeather(code=code, rain1h=rain1h, temp=temp)

    assert gen_greeting(weather) == text
