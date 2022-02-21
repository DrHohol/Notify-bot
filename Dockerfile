FROM python:3.9.5-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app
WORKDIR /app

RUN apt-get update && pip install --upgrade pip && \
	apt-get -y install libpq-dev gcc && \
	pip install -r requirements.txt

CMD ["chmod","755","starter.sh"]
CMD ["./starter.sh"]