# Humidity

This container handles the humidity and temperature sensor of the weather station.

This container is using Python and the [smbus2](https://pypi.org/project/smbus2/) library.
The sensor itself uses the [I2C](https://en.wikipedia.org/wiki/I%C2%B2C).

## Wiring

Ground and power of the SHT-30 are connected to ground and 3V on the Pi respectively.
The SCK (yellow) of the sensor connects to SCL1 (GPIO 3) of the PI and DATA (blue) to SDA1 (GPIO 2).

## Balena

To enable the I2C overlay for the PI using [Balena](https://www.balena.io/docs/reference/OS/advanced/), _"i2c_arm=on"_ must be specified as [device tree (DT)](https://www.raspberrypi.org/documentation/configuration/device-tree.md) parameter.

## Development

In order to test the code easily, the container uses a trick to allow using PyCharm locally and execute the code in the remote container.
For that the container needs to open an SSH port.
This can be achieved setting the device service variable `START_SSHD=1`.
This will start sshd and allow PyCharm to sue the container as a remote execution environment.

**NOTE**: This is a development trick/hack.
In a production environment the sshd config should be removed.

## Misc

* [SHT-30 Mesh-protected Weather-proof Temperature/Humidity Sensor](https://www.adafruit.com/product/4099)
* [SHT-30 Data sheet](https://cdn-shop.adafruit.com/datasheets/SLHT5.pdf)
* [Sample code](https://github.com/ControlEverythingCommunity/SHT30)
