FROM arm64v8/telegraf:1.15.4

RUN apt-get update \
 && apt-get install -y vim netcat \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY telegraf.conf /etc/telegraf/telegraf.conf
