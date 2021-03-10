# Raingauge

This container handles the rain gauge of the weather station.
The wiring is described [here](https://projects.raspberrypi.org/en/projects/build-your-own-weather-station/8).

This container is using Python and the [gpiozero](https://gpiozero.readthedocs.io/en/stable/) library.
Each rotation is handled as a button press out of which the wind speed can be calculated.

The [data sheet](https://cdn.sparkfun.com/assets/d/1/e/0/6/DS-15901-Weather_Meter.pdf) of the weather station provides the necessary information to calculate the rainfall.

> The rain gauge is a self-emptying tipping bucket type. Each 0.2794 mm of rain cause one momentary contact closure that can be recorded with a digital counter or microcontroller
interrupt input.

## Development

In order to test the code easily, the container uses a trick to allow using PyCharm locally and execute the code in the remote container.
For that the container needs to open an SSH port. 
This can be achieved setting the device service variable `START_SSHD=1`.
This will start sshd and allow PyCharm to sue the container as a remote execution environment.

*NOTE*: This is a development trick/hack.
In a production environment the sshd config should be removed.

## Misc

* [SSH access to container](https://github.com/balena-io-playground/balena-openssh)