FROM python:stretch

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn", "-b", ":5000", "main:APP"]
