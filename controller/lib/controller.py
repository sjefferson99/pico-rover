from config import SPI_ID, SCK, MOSI, MISO, CSN, CE, FWD_BUTTON, REV_BUTTON, LEFT_BUTTON, RIGHT_BUTTON
from machine import SPI, Pin
from lib.nrf24l01 import NRF24L01
from lib.ulogging import uLogger
from lib.button import Button
from asyncio import create_task, sleep, get_event_loop
import struct
from time import ticks_ms, ticks_diff

class Controller:
    """
    RC controller class, which initialises the radio, buttons, and asyncio
    tasks for sending control commands over RF.
    """
    def __init__(self) -> None:
        """
        Init method for the controller, initialises the radio and buttons.
        """
        self.log = uLogger("Controller initialised")
        
        spi = SPI(SPI_ID, sck=Pin(SCK), mosi=Pin(MOSI), miso=Pin(MISO))
        csn = Pin(CSN, mode=Pin.OUT, value=1)
        ce = Pin(CE, mode=Pin.OUT, value=0)
        self.radio = NRF24L01(spi, csn, ce, payload_size=8)
        pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")
        self.radio.open_tx_pipe(pipes[0])
        self.radio.open_rx_pipe(1, pipes[1])

        self.fwd_button = self.init_button(FWD_BUTTON, "Fwd")
        self.rev_button = self.init_button(REV_BUTTON, "Rev")
        self.left_button = self.init_button(LEFT_BUTTON, "Lft")
        self.right_button = self.init_button(RIGHT_BUTTON, "Rht")

    def init_button(self, gpio: int, name: str) -> Button:
        """
        Initialise a button on a GPIO pin, and create asyncio tasks for
        watching for and responding to button presses.
        """
        button = Button(gpio, name)
        create_task(button.wait_for_press())
        create_task(self.async_button_watcher(button))
        return button

    async def async_button_watcher(self, button: Button) -> None:
        """
        Async watcher for button press event to trigger action.
        """
        while True:
            event = button.get_event()
            await event.wait()
            event.clear()
            await self.async_do_button_action(button)
            await sleep(0.1)

    async def async_send_radio_command(self, command: str) -> int:
        """
        Send a 3 character command to the radio, and wait for an ACK
        Ack is an integer matching standard return codes:
        0 = Success - 1 = Failure
        """
        assert len(command) == 3
        self.radio.stop_listening()
        self.log.info(f"Sending radio command: {command}")
        try:
            self.radio.send(struct.pack("3s", command))
        except OSError:
            pass

        self.radio.start_listening()

        start_time = ticks_ms()
        timeout = False
        while not self.radio.any() and not timeout:
            if ticks_diff(ticks_ms(), start_time) > 250:
                self.log.error("Radio command response timed out")
                raise Exception("Radio command response timed out")
            await sleep(0.001)

        (ack,) = struct.unpack("i", self.radio.recv())
        self.log.info(f"Got radio command response: {ack}")

        return ack
    
    async def async_do_button_action(self, button: Button) -> None:
        """
        Abstract method to handle button press actions.
        """
        self.log.info(f"Button pressed: {button.get_name()}")
        await self.async_send_radio_command(button.get_name())

    def run(self) -> None:
        """
        Main run method for the controller, which starts the radio listening
        and runs the asyncio event loop.
        """
        self.log.info("Starting controller")
        self.radio.start_listening()

        loop = get_event_loop()
        loop.run_forever()
