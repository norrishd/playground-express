"""Create a gentle strobing rainbow glow."""
import board
import digitalio
import neopixel
import time


NUMBER_LEDS = 10
BRIGHTNESS = 0.1
SLEEP_SECONDS = 0.05  # debounce delay


print("Bombs away!")

# The slider/switch
switch = digitalio.DigitalInOut(board.SLIDE_SWITCH)  # D7
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

pixels = neopixel.NeoPixel(board.NEOPIXEL, NUMBER_LEDS, brightness=BRIGHTNESS)


def wheel(pos):
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
        pixels.fill(wheel(i))
    else:
        positions = [(i + 8 * j) % 255 for j in range(10)]
        colours = [wheel(pos) for pos in positions]
        pixels[:] = colours

    # print(colours[0])  # Uncomment this to see a print out of the colours in "Plotter" of Mu Editor

    time.sleep(SLEEP_SECONDS)
    i = (i + 1) % 255


print("Well this is awkward")
