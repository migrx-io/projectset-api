FROM ubuntu:20.04
LABEL MAINTAINER="Anatolii Makarov <anatolii.makaroff@gmail.com>"

RUN apt-get update && \
    apt-get -y install \
        curl \
        git \
        python3 \
        python3-dev \
        python3-pip \
        vim-tiny && \
    apt-get -qq clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

RUN useradd -ms /bin/bash appuser
COPY . /app
RUN rm -rf /app/app.yaml /app/config/app.db
RUN chown -R appuser:appuser /app

USER appuser

RUN pip3 install -r requirements.txt

ENV PORT=8082 
ENV LOGLEVEL=INFO
ENV PYENV=~/.local/bin

CMD ["./start"]
