
import board
import digitalio
import neopixel
import time


print("Bombs away!")

# Create a pointer to the little "reset" red LED
led = digitalio.DigitalInOut(board.LED)  # D13 == LED
led.direction = digitalio.Direction.OUTPUT

# The slider/switch
switch = digitalio.DigitalInOut(board.SLIDE_SWITCH)  # D7
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.10)
# pixels.brightness = 0.15


def wheel(pos):
    """Map a single int in the range [0, 255] to a colour cycling through the rainbow."""
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
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
    if switch.value:  # Red LED on (True) when switch is to the right (False)
        led.value = False
        # led.value = not led.value
        pixels[:] = [(0, 0, 0)] * len(pixels)
        pixels.fill(wheel(i))
    else:
        led.value = False
        positions = [(i + 8 * j) % 255 for j in range(10)]
        colours = [wheel(pos) for pos in positions]
        # print(colours[0])
        pixels[:] = colours
    time.sleep(0.1)  # debounce delay
    i = (i + 2) % 255


print("Well this is awkward")
