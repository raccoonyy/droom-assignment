FROM public.ecr.aws/docker/library/python:3.10-slim-buster

WORKDIR /app
COPY poetry.lock     /app
COPY pyproject.toml  /app
COPY gunicorn.py     /app

RUN pip install -U poetry
RUN poetry install --no-dev

COPY api /app/api

# CMD ["poetry", "run", "gunicorn", "api.bot:app", "-c", "gunicorn.py"]
CMD ["poetry", "run", "uvicorn", "api.bot:app", "--host", "0"]
