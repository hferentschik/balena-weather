#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import json
import os
import threading
import time

import paho.mqtt.client as mqtt
import pingouin as pg
import schedule
from dateutil.tz import *
from gpiozero import MCP3008


RECORDING_INTERVAL = 600


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


class Windvane:
    """Defines the an windvane"""

    MEASURE_INTERVAL = 1
    RECORD_INTERVAL = 10

    _data = []
    _wind_direction = 0

    def __init__(self):
        self._adc = MCP3008(channel=0)
        self._lock = threading.Lock()

        schedule.every(self.MEASURE_INTERVAL).seconds.do(self.measure)
        schedule.every(self.RECORD_INTERVAL).seconds.do(self.record)

    def current_direction(self):
        return self._wind_direction

    def measure(self):
        with self._lock:
            # print("voltage=%0.4f" % (self._adc.value * 3.3))
            windval = round(self._adc.value * 3.3, 2)
            if 0.3 <= windval <= 0.5:
                wind = 0.0
                self._data.append(wind)

            if 1.3 <= windval <= 1.5:
                wind = 22.5
                self._data.append(wind)

            if 1.1 <= windval <= 1.3:
                wind = 45.0
                self._data.append(wind)

            if 2.76 <= windval <= 2.78:
                wind = 67.5
                self._data.append(wind)

            if 2.71 <= windval <= 2.73:
                wind = 90.0
                self._data.append(wind)

            if 2.8 <= windval <= 2.9:
                wind = 112.5
                self._data.append(wind)

            if 2.1 <= windval <= 2.3:
                wind = 135.0
                self._data.append(wind)

            if 2.4 <= windval <= 2.6:
                wind = 157.5
                self._data.append(wind)

            if 1.7 <= windval <= 1.9:
                wind = 180.0
                self._data.append(wind)

            if 1.9 <= windval <= 2.1:
                wind = 202.5
                self._data.append(wind)

            if 0.6 <= windval <= 0.8:
                wind = 225.0
                self._data.append(wind)

            if 0.7 <= windval <= 0.9:
                wind = 247.5
                self._data.append(wind)

            if 0.0 <= windval <= 0.2:
                wind = 270.0
                self._data.append(wind)

            if 0.30 <= windval <= 0.35:
                wind = 292.5
                self._data.append(wind)

            if 0.2 <= windval <= 0.25:
                wind = 315.0
                self._data.append(wind)

            if 0.5 <= windval <= 0.7:
                wind = 337.5
                self._data.append(wind)

    def record(self):
        with self._lock:
            radian_angles = pg.convert_angles(self._data, low=0, high=360, positive=True)
            radian_mean = pg.circ_mean(radian_angles)
            if radian_mean < 0:
                radian_mean = radian_mean + (2 * 3.14)
            # print("mean=%0.4f" % radian_mean)
            self._wind_direction = round((radian_mean * 57.29578), 4)
            self._data = []


windvane = Windvane()
broker_address = os.environ.get('MQTT_BROKER') or "mqtt"
client = mqtt.Client("1")
if "MQTT_USER" in os.environ and "MQTT_PASSWORD" in os.environ:
    client.username_pw_set(username=os.environ.get('MQTT_USER'),password=os.environ.get('MQTT_PASSWORD'))

def record():
    client.connect(broker_address)
    json_body = [
        {
            "time": str('{:%Y-%m-%dT%H:%M:%S}'.format(datetime.datetime.now(tzutc()))),
            "measurement": "wind-direction",
            "fields": {
                "value": int(windvane.current_direction()),
                "sensor": "windvane"
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
