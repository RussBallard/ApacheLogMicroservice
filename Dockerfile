FROM python:3.8

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y --no-install-recommends \
     gcc \
     python-dev \
     python-pip \
     postgresql-client \
     tzdata \
     locales \
     git-core \
     libvips42

RUN mkdir /code

WORKDIR /code

COPY . /code/

RUN pip install -IUr requirements.txt

EXPOSE 8000