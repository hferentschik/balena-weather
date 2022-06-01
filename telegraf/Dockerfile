FROM telegraf:1.22.4

RUN apt-get update \
 && apt-get install -y vim netcat \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN rm /etc/telegraf/telegraf.conf
# need to create a dummy config, even if --config-directory is going to be specified
RUN touch /etc/telegraf/telegraf.conf

COPY *.conf /etc/telegraf/telegraf.d/
COPY entrypoint.sh /entrypoint.sh
CMD ["telegraf", "--config-directory", "/etc/telegraf/telegraf.d"]
