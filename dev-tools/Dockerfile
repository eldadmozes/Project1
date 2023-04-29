FROM jenkins/jenkins:lts

USER root

RUN apt-get update && \
    apt-get install -y python3
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


USER jenkins