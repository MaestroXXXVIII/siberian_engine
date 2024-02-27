FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /development/backend/siberian_engine/siberian_engine/siberian_engine

COPY ./requirements.txt /development/backend/siberian_engine/siberian_engine/siberian_engine/requirements.txt
RUN pip install -r /development/backend/siberian_engine/siberian_engine/siberian_engine/requirements.txt

COPY . /development/backend/siberian_engine/siberian_engine/siberian_engine
