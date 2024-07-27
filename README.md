# Pico Rover
Buggy to demonstrate motor and servo control with RF and wifi input.

## Components
### Motors
Motor2040 module with dedicated rp2040 drives the motors for each wheel.

### CPU
Pico W receives commands over wifi or RF and sends commands to the motor controller over I2C or to the servo for steering.

### Controller
Pico that converts button presses to RF signal for the CPU to receive.

## What works
### Controller
Connect 4 buttons to the controller pico and run the controller code with config file set appropriately for RF module and button connections.
Pressing the buttons will create a log message and send the appropriate 3 character command to a receiver listening as per the example file adjusted for "3s" on the receive structure.

### CPU
Need to modify the demo code to receive 3 characters and these will display when the controller sends them.

### Motors
Added a load of demo code lifted from the Pimoroni examples.
