# Windvane

This container handles the windvane (wind direction) of the weather station.
The wiring is described [here](https://projects.raspberrypi.org/en/projects/build-your-own-weather-station/7).
It is the most complex sensor in terms of wiring this it makes use of the MCP3008 analog to digital converter.

This container is using Python and the [gpiozero](https://gpiozero.readthedocs.io/en/stable/) library.

The wind direction is determined using a voltage divider.
From the [data sheet](https://cdn.sparkfun.com/assets/d/1/e/0/6/DS-15901-Weather_Meter.pdf) of the weather station:

> The wind vane is the most complicated of the three sensors. It has eight switches, each connected to a different resistor.
> The vane’s magnet may close two switches at once, allowing up to 16 different positions to be indicated.
> An external resistor can be used to form a voltage divider, producing a voltage output that can be measured with an analog to digital converter.

## Balena

The MCP3008 uses the SPI protocol.
To enable the SPI overlay for the PI using [Balena](https://www.balena.io/docs/reference/OS/advanced/), _"spi=on"_ must be specified as [device tree (DT)](https://www.raspberrypi.org/documentation/configuration/device-tree.md) parameter.

## Misc

* [MCP3008 Data sheet](https://cdn-shop.adafruit.com/datasheets/MCP3008.pdf)
