# DokerFIle to create Ubuntu server

FROM python:3.9
FROM amazonlinux

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install -r requirements.txt
RUN yum-config-manager --disable docker-ce-stable
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
RUN yum -y install google-chrome-stable_current_x86_64.rpm
RUN wget -N https://chromedriver.storage.googleapis.com/70.0.3538.16/chromedriver_linux64.zip
RUN unzip ~/chromedriver_linux64.zip
RUN rm ~/chromedriver_linux64.zip
COPY . /

ENTRYPOINT [ "python3", "./Master.py"]

