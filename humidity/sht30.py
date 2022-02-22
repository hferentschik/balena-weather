#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import json
import os
import schedule
import smbus2
from signal import pause
import threading
import time

import paho.mqtt.client as mqtt
from dateutil.tz import tzutc


RECORDING_INTERVAL = os.getenv('SAMPLE_RATE', 900)
print("SAMPLE_RATE set to " + str(RECORDING_INTERVAL))


def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


class Sht30:
    """Defines the an SHT-30 sensor"""

    def __init__(self):
        self._bus = smbus2.SMBus(1)
        self._lock = threading.Lock()

    def temperature(self):
        raw = self.data()
        return ((((raw[0] * 256.0) + raw[1]) * 175) / 65535.0) - 45

    def humidity(self):
        raw = self.data()
        return 100 * (raw[3] * 256 + raw[4]) / 65535.0

    def data(self):
        with self._lock:
            # SHT30 address, 0x44(68)
            # Send measurement command, 0x2C(44)
            #       0x06(06)    High repeatability measurement
            self._bus.write_i2c_block_data(0x44, 0x2C, [0x06])

            time.sleep(0.5)

            # SHT30 address, 0x44(68)
            # Read data back from 0x00(00), 6 bytes
            # cTemp MSB, cTemp LSB, cTemp CRC, Humidity MSB, Humidity LSB, Humidity CRC
            raw = self._bus.read_i2c_block_data(0x44, 0x00, 6)
            return raw


sht30 = Sht30()

broker_address = os.environ.get('MQTT_BROKER') or "mqtt"
client = mqtt.Client("1")
if "MQTT_USER" in os.environ and "MQTT_PASSWORD" in os.environ:
    client.username_pw_set(username=os.environ.get('MQTT_USER'),password=os.environ.get('MQTT_PASSWORD'))

def record():
    client.connect(broker_address)
    json_body = [
        {
            "time": str('{:%Y-%m-%dT%H:%M:%S}'.format(datetime.datetime.now(tzutc()))),
            "measurement": "humidity",
            "fields": {
                "humidity": sht30.humidity(),
                "temperature": sht30.temperature(),
                "sensor": "SHT-30"
            }
        }
    ]

    print("JSON body = " + str(json_body))
    msg_info = client.publish("sensors", json.dumps(json_body))
    if not msg_info.is_published():
        msg_info.wait_for_publish()
    client.disconnect()


schedule.every(RECORDING_INTERVAL).seconds.do(record)
run_continuously()

pause()
