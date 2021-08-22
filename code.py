"""Create a gentle strobing rainbow glow."""
import board
import digitalio
import neopixel
import time


NUMBER_LEDS = 10
BRIGHTNESS = 0.1
UPDATES_PER_SECOND = 20
SPEED = 1

# Small values (0-10) put all lights in similar colour range
# 25 gives the full rainbow. Higher values give random-seeming
# colours next to each other.
COLOUR_SPREAD = 3

print("Bombs away!")

# The slider/switch
switch = digitalio.DigitalInOut(board.SLIDE_SWITCH)  # D7
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

pixels = neopixel.NeoPixel(board.NEOPIXEL, NUMBER_LEDS, brightness=BRIGHTNESS)


def int_to_rgb(pos):
    """Map a single integer in the range [0, 255] to a colour in the rainbow,
    linearly interpolating from pure red (0) to pure green (85) to pure blue (170)
    and back to red.
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
while True:
    if switch.value:
        pixels.fill(int_to_rgb(i))
    else:
        positions = [(i + COLOUR_SPREAD * j) % 255 for j in range(NUMBER_LEDS)]
        colours = [int_to_rgb(pos) for pos in positions]
        pixels[:] = colours

    # print(colours[0])  # Uncomment this to see a print out of the colours in "Plotter" of Mu Editor

    time.sleep(1 / UPDATES_PER_SECOND)
    i = (i + SPEED) % 255


print("Well this is awkward")
