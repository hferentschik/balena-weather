FROM hferentschik/raspberrypi3-grafana:7.3.0

RUN apt-get update \
  &&  apt-get install -y unzip \
  &&  apt-get clean \
  &&  rm -rf /var/lib/apt/lists/*

# Plugin install
COPY marcusolsson-json-datasource-1.1.0.zip /marcusolsson-json-datasource-1.1.0.zip
RUN mkdir -p /usr/share/grafana/data/plugins
RUN unzip /marcusolsson-json-datasource-1.1.0.zip -d /usr/share/grafana/data/plugins

# Grafana config
COPY ./custom.ini /usr/share/grafana/conf/

# Grafana data sources
COPY ./influxdb-datasource.yml /usr/share/grafana/conf/provisioning/datasources

# Grafana dash config
COPY ./dashboard.json /usr/share/grafana/conf/provisioning/dashboards
COPY ./dashboards.yml /usr/share/grafana/conf/provisioning/dashboards
