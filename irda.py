"""
Tools to initialize PIO state machines and send/receive UART data frames over infrared
The actual PIO code is generated from irda_uart.pio. To change it, modify the .pio file
and run:

```
./pioasm -o python irda_uart.pio irda_uart_generated.py
```

pioasm is from the pico SDK: https://github.com/raspberrypi/pico-sdk/tree/master/tools/pioasm
"""

import irda_uart_generated
from machine import Pin, mem32
import rp2


class IrDA_UART:
    def __init__(self, tx_pin_num, rx_pin_num, baud_rate=9600):
        tx_pin = Pin(tx_pin_num, Pin.OUT)
        set_drive_strength_high(tx_pin_num)
        rx_pin = Pin(rx_pin_num, Pin.IN, pull=Pin.PULL_UP)

        # these programs have to go on separate state machines or they don't work right
        # not 100% sure why but that generally makes sense I guess
        self.tx_machine = rp2.StateMachine(
            1, irda_uart_generated.irda_uart_tx, freq=16 * baud_rate, set_base=tx_pin
        )
        self.tx_machine.active(True)

        if baud_rate == 9600:
            self.rx_machine = rp2.StateMachine(
                0,
                irda_uart_generated.irda_uart_rx_9600,
                freq=6_000_000,
                in_base=rx_pin,
                jmp_pin=rx_pin,
            )
        elif baud_rate == 115200:
            self.rx_machine = rp2.StateMachine(
                0,
                irda_uart_generated.irda_uart_rx_115200,
                freq=115_200 * 100,
                in_base=rx_pin,
                jmp_pin=rx_pin,
            )
        else:
            print("Invalid baud rate: {baud_rate}. Using 9600")
            self.rx_machine = rp2.StateMachine(
                0,
                irda_uart_generated.irda_uart_rx_9600,
                freq=6_000_000,
                in_base=rx_pin,
                jmp_pin=rx_pin,
            )
        self.rx_machine.active(True)

    def send_byte(self, b):
        # TODO: Do I need to set the rx state machine to inactive so it doesn't feedback?
        self.tx_machine.put(b << 24)

    def receive_byte(self):
        # TODO: poll this more efficiently
        while True:
            if self.rx_machine.rx_fifo() > 0:
                return self.rx_machine.get()


# this is wack I should look into adding this to micropython for real
# values are from RP2350 datasheet 9.11.3 Pad Control - User Bank
# thank you /u/17_maple_st on reddit for explaining this strategy
def set_gpio26_drivestrength_high():
    PADS_BANK0_BASE = 0x40038000
    GPIO26_OFFSET = 0x6C
    # 0x3 is 12mA
    DRIVE_HIGH_MASK = 0x00_00_00_30
    mem32[PADS_BANK0_BASE + GPIO26_OFFSET] = (
        mem32[PADS_BANK0_BASE + GPIO26_OFFSET] | DRIVE_HIGH_MASK
    )
    # print(f"GPIO 26 register state: {mem32[PADS_BANK0_BASE + GPIO26_OFFSET]:032b}")
    # print(f"GPIO 27 register state: {mem32[PADS_BANK0_BASE + GPIO26_OFFSET + 4]:032b}")


def set_drive_strength_high(pin_num):
    if pin_num == 26:
        set_gpio26_drivestrength_high()
    else:
        raise NotImplementedError("Not implemented for any pin but 26 yet")
