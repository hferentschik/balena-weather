FROM hferentschik/raspberrypi3-grafana:7.3.0

RUN apt-get update \
  &&  apt-get install -y unzip \
  &&  apt-get clean \
  &&  rm -rf /var/lib/apt/lists/*

# Plugin install
COPY marcusolsson-json-datasource-1.1.0.zip /marcusolsson-json-datasource-1.1.0.zip
COPY fetzerch-sunandmoon-datasource-0.2.1.zip /fetzerch-sunandmoon-datasource-0.2.1.zip
RUN mkdir -p /usr/share/grafana/data/plugins \
 && unzip /marcusolsson-json-datasource-1.1.0.zip -d /usr/share/grafana/data/plugins \
 && rm /marcusolsson-json-datasource-1.1.0.zip \
 && unzip /fetzerch-sunandmoon-datasource-0.2.1.zip -d /usr/share/grafana/data/plugins \
 && rm /fetzerch-sunandmoon-datasource-0.2.1.zip

# Grafana config
COPY ./custom.ini /usr/share/grafana/conf/

# Grafana data sources
COPY ./influxdb-datasource.yml /usr/share/grafana/conf/provisioning/datasources

# Grafana dash config
COPY ./dashboard.json /usr/share/grafana/conf/provisioning/dashboards
COPY ./dashboards.yml /usr/share/grafana/conf/provisioning/dashboards
