import asyncio
import json
import os
import random
from datetime import datetime, timedelta
from urllib.parse import urljoin

import httpx

API_KEY = os.environ.get("API_KEY")
API_BASE_URL = "https://thirdparty-weather-api-v2.droom.workers.dev/"
CURRENT = urljoin(API_BASE_URL, "/current")
FORECAST = urljoin(API_BASE_URL, "/forecast/hourly")
HISTORICAL = urljoin(API_BASE_URL, "/historical/hourly")


async def request(client: httpx.AsyncClient, url: str, params: dict):
    response = await client.get(url, params=params)
    return json.loads(response.text)


async def get_weathers(lat: float, lon: float):
    params = {"lat": lat, "lon": lon, "api_key": API_KEY}

    async with httpx.AsyncClient() as client:
        tasks = [asyncio.create_task(request(client=client, url=CURRENT, params=params))]

        for i in range(6, 43, 6):
            tasks.append(
                asyncio.create_task(request(client=client, url=FORECAST, params={**params, "hour_offset": i}))
            )

        for i in range(-6, -25, -6):
            tasks.append(
                asyncio.create_task(request(client=client, url=HISTORICAL, params={**params, "hour_offset": i}))
            )

        results = await asyncio.gather(*tasks)

    return results


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

    # forecast weathers
    for i in range(6, 43, 6):
        results.append({
            "timestamp": int((now + timedelta(hours=i)).timestamp()),
            "code": random.choice([0, 1, 2, 3]),
            "min_temp": random.choice(range(-20, 40)),
            "max_temp": random.choice(range(-20, 40)),
            "rain": random.choice(range(0, 110))
        })

    return json.dumps(results)
