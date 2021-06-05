#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import json
import os
import schedule
from signal import pause
import threading
import time

import paho.mqtt.client as mqtt
from dateutil.tz import tzutc
from gpiozero import Button

RECORDING_INTERVAL = 90


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


class Anemometer:
    """Defines the an anemometer sensor"""

    BASE_SPEED = 2.4  # km/h
    MEASURE_INTERVAL = 60

    _count = 0
    _speed = 0

    def __init__(self):
        self.counter = Button(5)
        self.counter.when_pressed = self.tick
        self._lock = threading.Lock()

        schedule.every(self.MEASURE_INTERVAL).seconds.do(self.measure)

    def tick(self):
        with self._lock:
            self._count += 1

    def speed(self):
        return self._speed

    def measure(self):
        with self._lock:
            current_count = self._count
            self._speed = round((self.BASE_SPEED * 1000 * current_count) / (3600 * self.MEASURE_INTERVAL), 0)
            self._count = 0


anemometer = Anemometer()

broker_address = os.environ.get('MQTT_BROKER') or "mqtt"
client = mqtt.Client("1")


def record():
    client.connect(broker_address)
    json_body = [
        {
            "time": str('{:%Y-%m-%dT%H:%M:%S}'.format(datetime.datetime.now(tzutc()))),
            "measurement": "wind-speed",
            "fields": {
                "value": anemometer.speed(),
                "sensor": "anemometer"
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
