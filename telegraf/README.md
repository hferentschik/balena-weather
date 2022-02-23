# Telegraf

This container runs [Telegraf](https://www.influxdata.com/time-series-platform/telegraf) consuming [MQTT](https://mqtt.org/) messages posted by the various sensors and pushing the data into [InfluxDB](https://www.influxdata.com/).
The [Dockerfile](./Dockerfile) adds `netcat` which can be useful for debugging.
In its default configuration Telegraf just ignores ill formatted MQTT messages without logging anything.
This makes it extremely hard to debug problems in the input and output of Telegraf.
For this reason a custom [telegraf.conf](./telegraf.conf) is added which adds for example the printer processor.
The configuration also shows how to enable the UDP output, and the socket listener input.
In combination these in- and output plugins can be used to test the Telegraf configuration in isolation on the container itself using `netcat`.

## Testing

With the socket listener input enabled custom measurements can be passed to Telegraf using `netcat`:

```sh
balena ssh <device-uuid> telegraf
nc -lup 8089

echo 'mymeasurement,my_tag_key=mytagvalue my_field="my field value"' | nc localhost 8094
```

## References

* Telegraf [configuration](https://github.com/influxdata/telegraf/blob/master/docs/CONFIGURATION.md)
* Telegraf [troubleshooting](https://docs.influxdata.com/telegraf/v1.17/administration/troubleshooting/)
* Telegraf [JSON input data format](https://docs.influxdata.com/telegraf/v1.18/data_formats/input/json/)
