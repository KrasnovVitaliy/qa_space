FROM python:3

RUN mkdir /db
WORKDIR /app

ADD ./app/ /app/
ADD ./config/config_prod.py /app/config.py

RUN pip install -r /app/requirements.txt
CMD [ "python", "./main.py" ]