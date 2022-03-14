# Telegraf

This container runs [Telegraf](https://www.influxdata.com/time-series-platform/telegraf) consuming [MQTT](https://mqtt.org/) messages posted by the various sensors and pushing the data into [InfluxDB](https://www.influxdata.com/).

## Testing

On your local machine you can replicate the MQTT -> Telegraf -> InfluxDB setup by running the following commands from within the _telegraf_ subdirectory:

```sh
docker build  . -t telegraf
docker network create telegraf
docker run -it -p 1883:1883 -p 9001:9001 --name mqtt -v $PWD/../mqtt/mosquitto.conf:/mosquitto/config/mosquitto.conf --network telegraf  eclipse-mosquitto
docker run -p 8086:8086 --name influxdb -v influxdb:/var/lib/influxdb --network telegraf influxdb
docker run --network telegraf telegraf
```

Now you can now connect to the MQTT queue using [MQTT Explorer](http://mqtt-explorer.com/) and send test messages.

## References

* Telegraf [configuration](https://github.com/influxdata/telegraf/blob/master/docs/CONFIGURATION.md)
* Telegraf [troubleshooting](https://docs.influxdata.com/telegraf/v1.17/administration/troubleshooting/)
* Telegraf [JSON input data format](https://docs.influxdata.com/telegraf/v1.18/data_formats/input/json/)
