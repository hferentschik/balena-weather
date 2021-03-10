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

GPIO_BUTTON = 6
RECORDING_INTERVAL = 300


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


class Raingauge:
    """Defines the an raingauge sensor"""

    BUCKET_CAPACITY = 0.2794  # mm
    MEASURE_INTERVAL = 180
    RESET_TIME = "23:59"

    _count = 0
    _level = 0

    def __init__(self):
        self.counter = Button(GPIO_BUTTON)
        self.counter.when_pressed = self.tick
        self._lock = threading.Lock()

        schedule.every(self.MEASURE_INTERVAL).seconds.do(self.measure)
        schedule.every().day.at(self.RESET_TIME).do(self.reset)

    def tick(self):
        with self._lock:
            self._count += 1

    def level(self):
        return self._level

    def measure(self):
        with self._lock:
            self._level = round(self.BUCKET_CAPACITY * self._count, 1)

    def reset(self):
        with self._lock:
            self._count = 0


raingauge = Raingauge()

broker_address = os.environ.get('MQTT_BROKER') or "localhost"
client = mqtt.Client("1")


def record():
    client.connect(broker_address)
    json_body = [
        {
            "time": str('{:%Y-%m-%dT%H:%M:%S}'.format(datetime.datetime.now(tzutc()))),
            "measurement": "rain",
            "fields": {
                "value": raingauge.level(),
                "sensor": "raingauge"
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
