# Telegraf

This container runs [Telegraf](https://www.influxdata.com/time-series-platform/telegraf) consuming [MQTT](https://mqtt.org/) messages posted by the various sensors and pushing the data into [InfluxDB](https://www.influxdata.com/).

## Testing

On your local machine you can replicate the MQTT -> Telegraf -> InfluxDB setup by running the following commands from within the _telegraf_ subdirectory:

```sh
docker build  . -t telegraf
docker network create telegraf
docker run -d --rm -p 1883:1883 -p 9001:9001 --name mqtt -v $PWD/../mqtt/mosquitto.conf:/mosquitto/config/mosquitto.conf --network telegraf  eclipse-mosquitto
docker run -d --rm -p 8086:8086 --name influxdb -v influxdb:/var/lib/influxdb --network telegraf influxdb:1.8
docker run --network telegraf telegraf
```

Now you can now connect to the MQTT queue using [MQTT Explorer](http://mqtt-explorer.com/) and send test messages.

To cleanup:

```sh
docker stop mqtt
docker stop influxdb
docker network rm telegraf
```

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

## References

* Telegraf [configuration](https://github.com/influxdata/telegraf/blob/master/docs/CONFIGURATION.md)
* Telegraf [troubleshooting](https://docs.influxdata.com/telegraf/v1.17/administration/troubleshooting/)
* Telegraf [JSON input data format](https://docs.influxdata.com/telegraf/v1.18/data_formats/input/json/)
* [plugins](https://archive.docs.influxdata.com/telegraf/v1.8/plugins)
