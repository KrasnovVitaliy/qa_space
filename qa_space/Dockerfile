FROM python:3
RUN mkdir /db
WORKDIR /app
ADD ./app/ /app/
RUN pip install -r /app/requirements.txt
CMD [ "python", "./main.py" ]