FROM python:3.8-slim-buster

RUN apt-get update && apt-get upgrade -y && apt-get install nano
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


WORKDIR /usr/app
COPY app.py ./

CMD ["python3.8", "app.py", "Eldad"]
