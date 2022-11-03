"""Create a gentle strobing rainbow glow.

The A and B buttons control the spread of the light spectrum.
"""
import time

import board
import digitalio
import neopixel

NUMBER_LEDS = 10
BRIGHTNESS = 0.1
UPDATES_PER_SECOND = 20
SPEED = 1  # How fast to progress through the rainbow

# Small values (0-10) put all lights in similar colour range
# 25 gives the full rainbow. Higher values give random-seeming
# colours next to each other.
colour_spread = 5

# The slider/switch
switch = digitalio.DigitalInOut(board.SLIDE_SWITCH)  # D7
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# The buttons
button_a = digitalio.DigitalInOut(board.BUTTON_A)  # D4
button_a.direction = digitalio.Direction.INPUT
button_a.pull = digitalio.Pull.DOWN

button_b = digitalio.DigitalInOut(board.BUTTON_B)  # D5
button_b.direction = digitalio.Direction.INPUT
button_b.pull = digitalio.Pull.DOWN

pixels = neopixel.NeoPixel(board.NEOPIXEL, NUMBER_LEDS, brightness=BRIGHTNESS)


def int_to_rgb(pos):
    """Map a single integer in the range [0, 255] to a colour in the rainbow, linearly interpolating
    from pure red (0) to pure green (85) to pure blue (170) and back to red.
    """
    if pos < 0 or pos > 255:
        return 0, 0, 0
    if pos < 85:
        return int(255 - pos * 3), int(pos * 3), 0
    if pos < 170:
        pos -= 85
        return 0, int(255 - pos * 3), int(pos * 3)
    pos -= 170
    return int(pos * 3), 0, int(255 - (pos * 3))


i = 0
next_update = time.monotonic()
button_a_prev, button_b_prev = button_a.value, button_b.value
while True:
    next_update += 1 / UPDATES_PER_SECOND

    if switch.value:
        pixels.fill(int_to_rgb(i))
    else:
        if button_a.value and not button_a_prev:
            colour_spread = max(0, colour_spread - 1)
            button_a_prev = True
        elif button_b.value and not button_b_prev:
            colour_spread += 1
            button_b_prev = True

        button_a_prev, button_b_prev = button_a.value, button_b.value

        positions = [(i + colour_spread * j) % 255 for j in range(NUMBER_LEDS)]
        colours = [int_to_rgb(pos) for pos in positions]
        pixels[:] = colours

    sleep_for = max(next_update - time.monotonic(), 0)
    time.sleep(sleep_for)

    i = (i + SPEED) % 255
