# Temperature

This container adds an additional DS18B20 1-wire temperature sensor to the weather station.
This way you can for example have one temperature sensor in the sun and the other in the shade.

This container is using Ruby and uses the [ds18b20](https://github.com/owaiswiz/ds18b20) gem.
Thanks to the popularity of the DS18B20 sensor, it is one of the few sensors for which one can find libraries in pretty much any language.
Otherwise, it is Python which is dominating this space.

## Wiring

Ground and power of the DS18B20 are connected to ground and 3V on the Pi respectively.
The output lead of the DS18B20 is connected to [GPIO 4](https://pinout.xyz/pinout/pin7_gpio4).
Place a 4.7k resistor between the positive lead and the output lead of the sensor.

## Balena

To use the 1-wire protocol the [w1-gpio DT overlay](https://www.balena.io/docs/learn/develop/hardware/i2c-and-spi/#1-wire-and-digital-temperature-sensors) must be enabled.

## Misc

* [DS18B20 Spec](https://datasheets.maximintegrated.com/en/ds/DS18B20.pdf)
