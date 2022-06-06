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

### 유닛 테스트

```shell
poetry run pytest
```
