from lib.motors import Motors, motor2040
from pimoroni import Button
from asyncio import sleep as sleep, create_task, get_event_loop, Event

buggy = Motors()
user_switch = Button(motor2040.USER_SW)
button_pressed = Event()

async def async_demo():
    while True and not button_pressed.is_set():
        if user_switch.read():
            break

        await sleep(1)
        buggy.smooth_all_wheels(0.3)
        await sleep(0.3)

        buggy.coast()
        await sleep(1)

        buggy.turn(0.3)
        await sleep(1)
        buggy.turn(-0.3)
        buggy.turn(-0.3)
        await sleep(1)
        buggy.turn(0.3)
        await sleep(1)

        buggy.smooth_all_wheels(-0.3)
        await sleep(0.3)

        buggy.coast()

async def async_poll_switch():
    while True:
        if user_switch.read():
            button_pressed.set()
            break
        await sleep(0.01)

create_task(async_demo())
create_task(async_poll_switch())

loop = get_event_loop()
loop.run_forever()