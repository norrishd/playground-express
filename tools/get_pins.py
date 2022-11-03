"""
Print out all pins and their aliases.

For Circuit Playground Express should get:

    board.A0 board.D12 board.SPEAKER
    board.A1 board.D6 board.SCK
    board.A2 board.D9 board.MISO
    board.A3 board.D10 board.MOSI
    board.A4 board.D3 board.SCL
    board.A5 board.D2 board.SDA
    board.A6 board.D0 board.RX
    board.A7 board.D1 board.TX
    board.A8 board.LIGHT
    board.A9 board.TEMPERATURE
    board.ACCELEROMETER_INTERRUPT
    board.ACCELEROMETER_SCL
    board.ACCELEROMETER_SDA
    board.BUTTON_A board.D4
    board.BUTTON_B board.D5
    board.D13 board.LED
    board.D7 board.SLIDE_SWITCH
    board.D8 board.NEOPIXEL
    board.IR_PROXIMITY
    board.IR_RX board.REMOTEIN
    board.IR_TX board.REMOTEOUT
    board.MICROPHONE_CLOCK
    board.MICROPHONE_DATA
    board.SPEAKER_ENABLE
"""
import board
import microcontroller


board_pins = []

for pin in dir(microcontroller.pin):
    if isinstance(getattr(microcontroller.pin, pin), microcontroller.Pin):
        pins = []
        for alias in dir(board):
            if getattr(board, alias) is getattr(microcontroller.pin, pin):
                pins.append("board.{}".format(alias))
        if len(pins) > 0:
            board_pins.append(" ".join(pins))
for pins in sorted(board_pins):
    print(pins)
