# pull official base image
FROM python:3.8-alpine3.12

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev \
    && apk add jpeg-dev zlib-dev libjpeg \
    && apk add freetype-dev

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "bot.py"]