FROM python:3.7
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

WORKDIR /root/opt
RUN apt-get install -y vim less
RUN apt-get install -y rsyslog
RUN apt-get install -y cron

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install redis
RUN pip install fastapi uvicorn

EXPOSE 80

#COPY ./app /app

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]