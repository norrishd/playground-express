# Playground Express
_Circuit Python scripts to run on an Adafruit Circuit Playground Express_

API references:

Core: https://circuitpython.readthedocs.io/projects/circuitplayground/en/latest/
Neopixels: https://circuitpython.readthedocs.io/projects/neopixel/en/latest/index.html#

## Setup

The Circuit Playground Express looks for a Python script named code.py or main.py in the root
directory of its boot drive. Therefore to run any script in this repo, just copy it to the root.

You may also have to [update your boot loader](https://learn.adafruit.com/adafruit-circuit-playground-express/updating-the-bootloader) first.

## Scripts

### Glow
Slowly pulse all LEDs through the rainbow. Slide the switch to make them all the same colour versus
a spread over a portion of the colour spectrum.

### Equa-Talk
An implementation of Robin Hanson's "EquaTalk": https://mason.gmu.edu/~rhanson/equatalk.html

