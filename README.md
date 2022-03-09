# Balena Weather

A Raspberry Pi weather station, implemented as [Balena](https://www.balena.io/) multi-container application.

[![balena deploy button](https://www.balena.io/deploy.svg)](https://dashboard.balena-cloud.com/deploy?repoUrl=https://github.com/hferentschik/balena-weather)

![Grafana Dash](./images/dash.png)

Raspberry Pi 3                                | Weather station
:--------------------------------------------:|:-------------------------:
![Raspberry Pi 3](./images/raspberry_pi.png)  |  ![Weather Station](./images/weather_station.png)

<!-- MarkdownTOC levels="2,3,4" autolink="true" indent="  " -->

- [Balena Weather](#balena-weather)
  - [Welcome to Balena Weather](#welcome-to-balena-weather)
  - [Hardware](#hardware)
    - [Wiring](#wiring)
  - [Services](#services)
    - [Sensors](#sensors)
    - [Message queue and database](#message-queue-and-database)
    - [UI and API](#ui-and-api)
    - [DT parameters and overlays](#dt-parameters-and-overlays)
  - [Misc](#misc)
    - [InfluxDB](#influxdb)
    - [Powering via 5V rail](#powering-via-5v-rail)
    - [Other resources](#other-resources)

<!-- /MarkdownTOC -->

## Welcome to Balena Weather

This project is inspired by [Build your own weather station](https://projects.raspberrypi.org/en/projects/build-your-own-weather-station/0) from _projects.raspberrypi.org_.
The following sections describe the hardware, wiring and configuration of Balena Weather.

## Hardware

Let's start with the hardware used for this project.

- 1 [Raspberry Pi 3](https://www.raspberrypi.com/products/raspberry-pi-3-model-b/) - the heart of the weather station.
    Balena Weather is also compatible with the Raspberry Pi 4.
- 1 [Prototyping HAT for Raspberry Pi](https://www.robotshop.com/en/prototyping-hat-raspberry-pi-b-2ba3b.html) - my aim was to build a permanent weather station (see picture above).
    For this reason I opted for the Prototyping HAT and soldering the components together.
    You can of course also use a breadboard for a less permanent solution.
- 1 [Sparkfun Weather Meter Kit](https://www.sparkfun.com/products/15901) - the main weather station components including anemometer, windvane and raingauge.
- 1 [MCP3008](https://www.microchip.com/en-us/product/MCP3008) - a 8-channel, 10-bit ADC with SPI interface.
    It is used to convert the analog voltage provided by the windvane's into a digital value.
- 1 [SHT-30](https://www.adafruit.com/product/4099) - a wheater proof humidity sensor.
    The SHT-30 also includes a temperature sensor.
    The temperature measures by the SHT-30 is also stored in InfluxDB, however, the default Grafana dashboard does not include its value.
- 1 [DS18B20](https://www.amazon.com/Eiechip-Waterproof-Temperature-Thermometer-Resistance/dp/B07MB1J43W/) - standard 1-wire bus water proof temperature sensor.
- 2 4.7k&#8486; resistors - used for the vindvane's voltage divider circuit as well as a pull up resistor for the temperature sensor.
- 1 [Raspberry Pi IP54 Outdoor Project Enclosure](https://sixfab.com/product/raspberry-pi-ip54-outdoor-iot-project-enclosure/) - a weather proof enclosure for the Raspberry Pi.

The folling paragraph shows how the components are connected schematically.

### Wiring

The following diagram shows the schematics of Balena Weather.
The anemometer, windvane and raingauge are symbolised by their main electric component.

**NOTE**: The Sparkfun Weather station comes per default with RJ11 connectors which has 6 pins.
The middle four pins are connected, but only two cables are used.
Refer to the [Sparkfun Weather Meter Kit manual](https://cdn.sparkfun.com/assets/d/1/e/0/6/DS-15901-Weather_Meter.pdf) to see which cables are relevant for each of the components.

![Balena Weather Wiring](./images/balena_weather_bb.png)

## Services

On the software side Balena Weather is built as Balena [multi container application](https://www.balena.io/docs/learn/develop/multicontainer/).
The services comprising Balena Weather are defined in [docker-compose.yml](./docker-compose.yml).

The following paragraphs describe the various services in more detail.
Each of the service build subdirectory contains a README as well providing additional information.

### Sensors

- [Anemometer](./anemometer/README.md) - Anemometer (wind speed) sensor of the weather station.
- [Humidity](./humidity/README.md) - Humidity and temperature sensor SHT-30.
- [Raingauge](./raingauge/README.md) - Raingauge sensor of the weather station.
- [Temperature](/temperature/README.md) - Additional DS18B20 temperature sensor.
- [Windvane](/windvane/README.md) - Windvane sensor of the weather station.

The default sample rate for each of the containers is 15 minutes.
You can define a _SAMPLE_RATE_ device variable for any of these containers to change the sample rate.
The sample rate needs to be specified in seconds.
Each sensor service also accepts values for _MQTT_USER_ and _MQTT_PASSWORD_ to authenticate against the MQTT message broker.
If MQTT authentication is used the same username and password needs to be specified to all sensor containers, as well as the MQTT container itself.

![Balena Device Variables](./images/device_variables.png)

The variables _LATITUDE_, _LONGITUDE_ and _TIMEZONE_ affect the _api_ service.
For more information refer to the _api_ [README](./api/README.md).

### Message queue and database

- [Mqtt](./mqtt/README.md) - [Eclipse Mosquitto](https://hub.docker.com/r/arm64v8/eclipse-mosquitto) container which acts as message broker to which all sensors are sending their data.
  The Telegraf container reads from the Mosquitto queue and pushes the metrics into InfluxDB.
- [Telegraf](./telegraf/README.md) - Part of the [TIG](https://hackmd.io/@lnu-iot/tig-stack) stack to consume and display sensor data.
- InfluxDB - Time series database storing the sensor data.
  This is the storage component of the [TIG](https://hackmd.io/@lnu-iot/tig-stack) stack.
  It uses a default [InfluxDB DockerHub image](https://hub.docker.com/_/influxdb).

### UI and API

- [NGINX](./nginx) - NGINX listening on port 80 and acting as reverse proxy.
- [API](./api/README.md) - A Ruby based [Sinatra](http://sinatrarb.com) used for exposing REST APIs for the weather app.
- [Grafana Dashboard](./dashboard/README.md) - the Grafana dashboard displaying all weather data.

### DT parameters and overlays

For the sensors to work, the Balena [device or fleet configuration](https://github.com/balena-io/balena-fleet-management-masterclass#3-configuration) needs to enable the _w1-gpio_ overlay as well as set the DT parameters _"i2c_arm=on","spi=on"_.

![Balena Device Configuration](./images/device_configuration.png)

## Misc

### InfluxDB

In order to inspect or modify the data stored in the Influx database you can connect directly to the _influxdb_ container and start the [`influx` CLI](https://docs.influxdata.com/influxdb/v1.8/tools/shell/):

```sh
$ balena ssh <app-name> influxdb
? Select a device amazing-smoke (a36de3)
root@265d8274d16b:/# influx
Connected to http://localhost:8086 version 1.8.0
InfluxDB shell version: 1.8.0
```

In order to get human-readable dates use the `precision rfc3339` command:

```sh
> precision rfc3339
> use weather
Using database weather
> show measurements
name: measurements
name
----
humidity
rain
temperature
water-temperature
wind-direction
wind-speed
```

To select the entries of a measurement:

```sh
> SELECT * FROM "water-temperature"
2021-06-18T06:05:05Z DS18B20       22.0625            sensors
...
```

To delete entries from a measurement use te [`DROP SERIES`](https://docs.influxdata.com/influxdb/v1.8/query_language/manage-database/#drop-series-from-the-index-with-drop-series) query:

```sh
> DROP SERIES FROM "water-temperature"
```

### Powering via 5V rail

In my case I decided to power the Raspberry Pi via the 5V power rail.
The following links provide information on how to do so.

- [Raspberry Pi Fuse](https://www.petervis.com/Raspberry_PI/Raspberry_Pi_Dead/Raspberry_Pi_Fuse.html)
- [Power requirements of the Pi](https://raspberrypi.stackexchange.com/questions/51615/raspberry-pi-power-limitations)

### Other resources

- [Balena Masterclass](https://github.com/balena-io/balena-cli-masterclass/blob/master/README.md)
- [Pinout](https://pinout.xyz/)
