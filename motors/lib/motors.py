from motor import Motor, motor2040
from time import sleep

class Motors():
    """A class to control the motors on a 4 wheel drive buggy using the moto2040 library."""
    def __init__(self):
        self.motor_pins = [motor2040.MOTOR_A, motor2040.MOTOR_B, motor2040.MOTOR_C, motor2040.MOTOR_D]
        self.motors = [Motor(pins) for pins in self.motor_pins]
        self.right_motors = [self.motors[0], self.motors[1]]
        self.left_motors = [self.motors[2], self.motors[3]]
        self.curent_speed = 0.0

        for m in self.motors:
            m.enable()        
    
    def smooth_all_wheels(self, end_speed: float):
        """Ramp the speed of the motors from current speed to end_speed over the given duration."""
        assert -1.0 <= end_speed <= 1.0
        start_speed = self.curent_speed
        duration = 0.1
        step = 0.01
        steps = int(duration / step)
        for i in range(steps):
            speed = start_speed + (end_speed - start_speed) * (i / steps)
            self.all_wheels(speed)
            sleep(step)
        self.all_wheels(end_speed)
    
    def all_wheels(self, speed: float):
        """Drive forward at the given speed."""
        assert -1.0 <= speed <= 1.0
        self.curent_speed = speed
        for m in self.right_motors:
            m.speed(speed)
        for m in self.left_motors:
            m.speed(-speed)
    
    def turn(self, speed: float):
        """Turn at the given speed, +ve is clockwise."""
        for m in self.right_motors:
            m.speed(self.curent_speed - speed)
        for m in self.left_motors:
            m.speed(self.curent_speed - speed)
        sleep(0.2)
        self.all_wheels(self.curent_speed)

    def stop(self):
        """Stop all motors."""
        self.curent_speed = 0.0
        for m in self.motors:
            m.stop()

    def coast(self):
        """Coast all motors."""
        self.curent_speed = 0.0
        for m in self.motors:
            m.coast()
