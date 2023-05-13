FROM python:3.8-slim-buster

RUN apt-get update && apt-get upgrade -y && apt-get install nano && apt install python3-pip -y
COPY slim-app/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


WORKDIR /usr/app
COPY slim-app.py ./

CMD ["python3.8", "slim-app.py", "Eldad"]
