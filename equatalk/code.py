"""EquaTalk, a tool for facilitating better conversations.

Reference: https://mason.gmu.edu/~rhanson/equatalk.html
"""
import math
import random
import time

from adafruit_circuitplayground.express import cpx

# Average and minimum time in seconds between timer triggering
MEAN_TRIGGER_INTERVAL = 60
MIN_TRIGGER_INTERVAL = 5

# LED params
SAMPLE_RATE = 200
REFRESH_RATE = 1 / SAMPLE_RATE
PULSE_RATE = 2 / 3
MAX_BRIGHTNESS = 0.5

# Time in secs for linear increase/decrease in brightness before/after a trigger
TRIGGER_WINDOW = 3

print("Launching EquaTalk")


def wheel(pos):
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


def get_next_trigger_time(now):
    """Randomly select a time for the next trigger to go off.

    Time is sampled from a geometric distribution, i.e. the number X of Bernoulli trials needed to
    get one success.

    Cumulative distribution function:

        1 - (1 - p)**floor(x)
    """
    p = 1 / MEAN_TRIGGER_INTERVAL

    # The base 1-p logarithm is the inverse of the exponential CDF.
    interval = math.log(random.random(), 1 - p) + 1
    interval = max(interval, MIN_TRIGGER_INTERVAL)

    print("Next trigger in", interval, "seconds")

    return now + interval


def solve_linear_equation(x1: float, y1: float, x2: float, y2: float):
    """Solve the linear equation connecting two points.

    Return the gradient and intercept.
    """
    m = (y2 - y1) / (x2 - x1)
    c = y1 - m * x1

    return m, c


def get_next_brightness(
    now: float,
    gradient=None,
    intercept=None,
):
    """Return the next brightness value.

    Transitions through 3 modes:
        - Pulsing according to a sine wave (while people talking)
        - Linearly increasing to a max when nearing triggering
        - Linearly decreasing to resuming sine pulsing after triggering
    """
    if gradient is None:  # Pulsing
        # Sin is defined over range [-1, 1] - scale to range [0.1, 0.3]
        return math.sin(now * math.pi * PULSE_RATE) / 10 + 0.2

    # Linearly rising or descending linearly
    return gradient * now + intercept


def run():
    """Play a softly pulsing light. Every second there's a 1/60 chance that a chime is emitted
    and the light will change to a new colour.
    """
    colour = wheel(random.randint(0, 255))  # Random starting colour
    cpx.pixels.fill(colour)

    next_trigger_time = get_next_trigger_time(time.monotonic())

    # This will be updated before it's encountered
    last_trigger_end = next_trigger_time + 1000 * TRIGGER_WINDOW
    gradient = None
    intercept = None

    muted = cpx.switch

    while True:
        now = time.monotonic()
        if muted and not cpx.switch:  # Un-mute
            muted = False
            cpx.play_tone(300, 0.2)
        elif not muted and cpx.switch:
            muted = True

        if now > next_trigger_time - TRIGGER_WINDOW:
            if gradient is None:
                print("Rising")
                # Enter the rising phase
                x1, y1 = now, brightness
                x2, y2 = next_trigger_time, MAX_BRIGHTNESS
                gradient, intercept = solve_linear_equation(x1, y1, x2, y2)
        elif now > (last_trigger_end + TRIGGER_WINDOW):
            if gradient is not None:
                # Return to normal inter-trigger pulsing
                print("Pulsing")
                gradient, intercept = None, None

        brightness = get_next_brightness(
            now,
            gradient,
            intercept,
        )
        cpx.pixels.brightness = brightness

        if now > next_trigger_time:
            # Update colour
            colour = wheel(random.randint(0, 255))
            cpx.pixels.fill(colour)

            # Play tone if not muted. Switch = True when to the left
            if not muted:
                # NB playing audio blocks the main thread, so time/brightness updates will block too
                cpx.play_tone(400, 0.15)
                cpx.play_tone(800, 0.15)
                now = time.monotonic()

            last_trigger_end = now
            next_trigger_time = get_next_trigger_time(now)

            # Enter the descending phase
            x1, y1 = now, MAX_BRIGHTNESS
            x2 = now + TRIGGER_WINDOW
            y2 = get_next_brightness(x2, None, None)
            print("Descending")
            gradient, intercept = solve_linear_equation(x1, y1, x2, y2)

        time.sleep(REFRESH_RATE)


if __name__ == "__main__":
    run()
