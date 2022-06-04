from api.models import CurrentWeather


def gen_greeting(weather: CurrentWeather):
    match weather.code:
        case 3 if weather.rain1h >= 100:
            return "폭설이 내리고 있어요."
        case 3:
            return "눈이 포슬포슬 내립니다."
        case 2 if weather.rain1h >= 100:
            return "폭우가 내리고 있어요."
        case 2:
            return "비가 오고 있습니다."
        case 1:
            return "날씨가 약간은 칙칙해요."
        case 0 if weather.temp >= 30:
            return "따사로운 햇살을 맞으세요."
        case 0 if weather.temp <= 0:
            return "날이 참 춥네요."
        case _:
            return "날씨가 참 맑습니다."
