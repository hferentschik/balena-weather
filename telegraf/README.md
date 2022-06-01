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

## Sample TTN MQTT Message

```json
{
   "end_device_ids":{
      "device_id":"eui-70b3d57ed004bf0d",
      "application_ids":{
         "application_id":"lora-node-strand"
      },
      "dev_eui":"70B3D57ED004BF0D",
      "join_eui":"0000000000000000",
      "dev_addr":"260B419F"
   },
   "correlation_ids":[
      "as:up:01G666QJPDY577KEFM756C6XB4",
      "gs:conn:01G65TH04AKRGBY9Y6HF60498N",
      "gs:up:host:01G65TH04PCMVNFCVK14VH1BXK",
      "gs:uplink:01G666QJFESKAD5V16YXZXY1PY",
      "ns:uplink:01G666QJFF6Y5XF9RRZ5FVTXM4",
      "rpc:/ttn.lorawan.v3.GsNs/HandleUplink:01G666QJFF51PKNFHWT3QJ2SV7",
      "rpc:/ttn.lorawan.v3.NsAs/HandleUplink:01G666QJNYE3RFRETDKBPBNJHM"
   ],
   "received_at":"2022-06-22T17:18:03.469281942Z",
   "uplink_message":{
      "session_key_id":"AYFyzkaRyD0GW9SncUVSVA==",
      "f_port":1,
      "f_cnt":531,
      "frm_payload":"W3sidGltZSI6ICIyMDIyLTA2LTIyVDE3OjE4OjAyIiwgIm1lYXN1cmVtZW50IjogIndhdGVyLXRlbXBlcmF0dXJlIiwgImZpZWxkcyI6IHsidGVtcGVyYXR1cmUiOiAyMS42ODc1LCAic2Vuc29yIjogIkRTMThCMjAifX1d",
      "decoded_payload":{
         "0":{
            "fields":{
               "sensor":"DS18B20",
               "temperature":21.6875
            },
            "measurement":"water-temperature",
            "time":"2022-06-22T17:18:02"
         }
      },
      "rx_metadata":[
         {
            "gateway_ids":{
               "gateway_id":"norsesundshemmet-gw",
               "eui":"B827EBFFFEE6B16A"
            },
            "time":"2022-06-22T17:18:03.164799928Z",
            "timestamp":4205568972,
            "rssi":-60,
            "channel_rssi":-60,
            "snr":14.5,
            "location":{
               "latitude":57.870249320753445,
               "longitude":12.447998723474097,
               "altitude":80,
               "source":"SOURCE_REGISTRY"
            },
            "uplink_token":"CiEKHwoTbm9yc2VzdW5kc2hlbW1ldC1ndxIIuCfr//7msWoQzMev1Q8aCwjLnc2VBhDi+sB1IOCpx/uy9AIqCwjLnc2VBhC4y8pO"
         }
      ],
      "settings":{
         "data_rate":{
            "lora":{
               "bandwidth":125000,
               "spreading_factor":9
            }
         },
         "coding_rate":"4/5",
         "frequency":"867900000",
         "timestamp":4205568972,
         "time":"2022-06-22T17:18:03.164799928Z"
      },
      "received_at":"2022-06-22T17:18:03.247131536Z",
      "consumed_airtime":"0.738304s",
      "network_ids":{
         "net_id":"000013",
         "tenant_id":"ttn",
         "cluster_id":"eu1",
         "cluster_address":"eu1.cloud.thethings.network"
      }
   }
}
```

## References

* Telegraf [configuration](https://github.com/influxdata/telegraf/blob/master/docs/CONFIGURATION.md)
* Telegraf [troubleshooting](https://docs.influxdata.com/telegraf/v1.17/administration/troubleshooting/)
* Telegraf [JSON input data format](https://docs.influxdata.com/telegraf/v1.18/data_formats/input/json/)
* [plugins](https://archive.docs.influxdata.com/telegraf/v1.8/plugins)
