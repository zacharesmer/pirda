from irda import IrDA_UART
import board_config
import time

irda_uart = IrDA_UART(board_config.IRDA_TX_PIN, board_config.IRDA_RX_PIN, 9600)


## Run this loop on the transmitting board

# while True:
#     # b = 0xAA
#     test_string = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
#     for c in test_string:
#         print(f"Sending {c} ({c:08})")
#         irda_uart.send_byte(ord(c))
#     irda_uart.send_byte(ord("\n"))
#     irda_uart.send_byte(ord("\n"))


# and run this loop on the receiving board

while True:
    print(chr(irda_uart.receive_byte()), end="")
