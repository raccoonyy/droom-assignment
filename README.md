# WeatherBot API for delightroom

## 실행 환경

- 파이썬 3.10.4

## 실행

### 준비

```shell
pip install -U poetry
poetry install 
export API_KEY={API_KEY}
```

### 개발 서버

```shell
poetry run uvicorn api.bot:app --reload
```

[http://127.0.0.1:8000/summary?lat=37.5&lon=127]() 접속

### 유닛 테스트

```shell
poetry run pytest
```

### 코드 포매팅 검사

```shell
poetry run flake8 api
```
