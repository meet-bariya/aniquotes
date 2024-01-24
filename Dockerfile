FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN python3 -m venv /opt/venv

RUN /opt/venv/bin/pip install pip --upgrade && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

COPY ./entrypoint.sh .

RUN chmod +x entrypoint.sh

COPY ./app/ ./app/

ENTRYPOINT [ "/app/entrypoint.sh" ]