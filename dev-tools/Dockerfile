FROM jenkins/jenkins:lts

USER root

RUN apt-get update && \
    apt-get install -y python3
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Install Docker dependencies
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Install Docker Engine
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get update && apt-get install -y docker-ce-cli


USER jenkins

CMD ["python3.8", "app.py", "Eldad"]