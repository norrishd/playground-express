# EquaTalk

Implementation of Robin Hanson's "EquaTalk" idea for dividing up speaking time amongst a group of
people in a way that's basically fair, but also allows for randomness and valuable contributions to
a discussion to be prolonged.

See: https://mason.gmu.edu/~rhanson/equatalk.html

Every second there's a 1/60th chance of the device "triggering", i.e. the colour changes, and if
the switch is set to the right, a chime will play. Any person(s) speaking when this happens should
pay a token. When a person runs out of tokens they can't speak anymore, unless someone else pays
them one of their own tokens.

## Maths

A 1/60th chance of triggering per second defines a geometric cumulative distribution function. This
distribution has a minimum of 1 and is technically unbounded in the maximal direction, however the
mean is 60 seconds and median is 42 seconds. There's only a 1% chance of at least 4.5 minutes
elapsing between chimes.

To efficiently solve this, a uniform random value is sampled and used with the inverse
(logarithmic) function to get the next interval. To avoid the chime triggering in rapid succession
a 5 second cool-off is imposed between triggerings.

In between triggers, the colour pulses gently according to a sine wave, linearly ramping up to a
maximum brightness when the trigger is ready to occur, then ramping back down to resume the
sinusoidal pulsing.
