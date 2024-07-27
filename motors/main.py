from pimoroni import Button
from pimoroni import Analog, AnalogMux

from motor import Motor, motor2040
from encoder import MMME_CPR, Encoder
from plasma import WS2812

from time import sleep
from machine import Pin

# ADC reading classes
sen_adc = Analog(motor2040.SHARED_ADC)
vol_adc = Analog(motor2040.SHARED_ADC, motor2040.VOLTAGE_GAIN)
cur_adc = Analog(motor2040.SHARED_ADC, motor2040.CURRENT_GAIN,
                 motor2040.SHUNT_RESISTOR, motor2040.CURRENT_OFFSET)

# Mux setup- includes muxed pull up/down pin
mux = AnalogMux(motor2040.ADC_ADDR_0, motor2040.ADC_ADDR_1, motor2040.ADC_ADDR_2,
                muxed_pin=Pin(motor2040.SHARED_ADC))

# Enable motor fault sense pull up
mux.configure_pull(motor2040.FAULT_SENSE_ADDR, Pin.PULL_UP)

# Configure motor encoder A
enc = Encoder(0, 0, motor2040.ENCODER_A, counts_per_rev=MMME_CPR, count_microsteps=True)

# Neopixel setup
led = WS2812(motor2040.NUM_LEDS, 1, 0, motor2040.LED_DATA)
led.start()
led.set_rgb(255, 0, 0, 0)
led.set_rgb(255, 0, 0, 0)

# Motors setup
motor_a = Motor(motor2040.MOTOR_A)
motor_a.enable()

# User switch
user_switch = Button(motor2040.USER_SW)

# Example sensors pull up
for addr in range(motor2040.NUM_SENSORS):
    mux.configure_pull(addr + motor2040.SENSOR_1_ADDR, Pin.PULL_UP)

# Read motor currents
for addr in range(motor2040.NUM_MOTORS):
    mux.select(addr + motor2040.CURRENT_SENSE_A_ADDR)
    print("Current", addr + 1, "=", cur_adc.read_current(), "A")

# Read motor total voltage
mux.select(motor2040.VOLTAGE_SENSE_ADDR)
print("Voltage =", vol_adc.read_voltage(), "V")

# Read sensors ADC input
for addr in range(motor2040.NUM_SENSORS):
    mux.select(addr + motor2040.SENSOR_1_ADDR)
    print("Sensor", addr + 1, "=", sen_adc.read_voltage())

# Fault sense read
mux.select(motor2040.FAULT_SENSE_ADDR)
print("Fault =", not mux.read())

# Display motor A position
print(f"Motor A position = {enc.degrees()} degrees")

old_state = user_switch.read()
state = user_switch.read()

print("Waiting for user switch to be pressed")

while state == old_state:
    state = user_switch.read()
    sleep(0.1)

led.set_rgb(0, 255, 0, 0)
print("User switch pressed")

motor_a.speed(0.5)

sleep(1)

led.set_rgb(0, 0, 255, 0)

motor_a.speed(-0.5)

sleep(1)

led.set_rgb(0, 0, 0, 255)

motor_a.speed(0)
print(f"Motor A position = {enc.degrees()} degrees")

sleep(1)

led.clear()