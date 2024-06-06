FROM python:3.10

ENV DEBIAN_FRONTEND=noninteractive

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Updating apt to see and install Google Chrome
RUN apt-get -y update

# Magic happens
RUN apt-get install -y google-chrome-stable

# Installing Unzip
RUN apt-get install -yqq unzip

# Download the Chrome Driver
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.141/linux64/chromedriver-linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver-linux64/chromedriver -d /usr/local/bin/

RUN apt-get update && apt-get install -y xvfb && apt-get upgrade -y

# required for headfull Chrome
ENV DISPLAY=:0

WORKDIR /usr/src

COPY . /app

WORKDIR /app

RUN chown -R 10014:0 "/app"

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

USER 10014

# now, replace `python3 main.py` with the command invocation that will employ headfull Chrome
CMD xvfb-run --server-args="-screen 0 1900x1200x24" python3 manage.py runserver 0.0.0.0:8000

#CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]