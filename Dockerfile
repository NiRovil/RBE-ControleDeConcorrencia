FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app

RUN rm -rf /app/env.py; rm -rf Dockerfile

EXPOSE 3000

CMD ["python", "/app/app/main.py"]