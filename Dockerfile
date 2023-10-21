FROM python:3.11-alpine

WORKDIR /todo

COPY ./requirements.txt /todo/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /todo/requirements.txt

COPY . /todo/

CMD uvicorn main:app --proxy-headers --host 0.0.0.0 --port $PORT