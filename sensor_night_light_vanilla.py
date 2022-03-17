from machine import Pin
import machine
from time import sleep

class SensorNightLight:

    def __init__(self, trigger_interval=1, trigger_duration=30):
        self.led = Pin(4, Pin.OUT)
        self.light = Pin(27, Pin.IN, Pin.PULL_DOWN)
        self.motion = Pin(28, Pin.IN, Pin.PULL_DOWN)
        self.trigger_interval = trigger_interval
        self.trigger_duration = trigger_duration
        self._loop()

    def _loop(self):
        while True:
            print("light sensor TRIGGERED") if self.light.value() == 1 else print("light sensor SLEEPING")
            print("motion sensor TRIGGERED") if self.motion.value() == 1 else print("motion sensor SLEEPING")
            if self.light.value() == 1:
                print("dark enough - waiting for motion")
                while self.motion.value() == 1:
                    print(f"motion sensor triggered - LED on and checking again in {self.trigger_duration}")
                    self.led.high()
                    sleep(self.trigger_duration)  
            self.led.low()
            sleep(self.trigger_interval)
    

if __name__ == "__main__":
    SensorNightLight()




