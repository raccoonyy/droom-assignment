from api.models import CurrentWeather, HistoricalWeather


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


def gen_temperature(weathers: list[HistoricalWeather], current_weather: CurrentWeather):
    weathers = sorted(weathers, key=lambda d: d.timestamp)
    oldest_weather = weathers[0]
    min_temp = min([int(weather.temp) for weather in weathers] + [int(current_weather.temp)])
    max_temp = max([int(weather.temp) for weather in weathers] + [int(current_weather.temp)])

    difference = int(current_weather.temp) - int(oldest_weather.temp)
    if difference > 0 and current_weather.temp >= 15:
        text = f"어제보다 {abs(difference)}도 덜 덥습니다."
    elif difference > 0 and current_weather.temp < 15:
        text = f"어제보다 {abs(difference)}도 더 춥습니다."
    elif difference < 0 and current_weather.temp >= 15:
        text = f"어제보다 {abs(difference)}도 더 덥습니다."
    elif difference < 0 and current_weather.temp < 15:
        text = f"어제보다 {abs(difference)}도 덜 춥습니다."
    elif difference == 0 and current_weather.temp >= 15:
        text = "어제와 비슷하게 덥습니다."
    else:
        text = "어제와 비슷하게 춥습니다."

    text += f" 최고기온은 {max_temp}도, 최저기온은 {min_temp}도 입니다."
    return text
