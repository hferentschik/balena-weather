FROM telegraf:1.19

RUN apt-get update \
 && apt-get install -y vim netcat \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY telegraf.conf /etc/telegraf/telegraf.conf
COPY entrypoint.sh /entrypoint.sh
