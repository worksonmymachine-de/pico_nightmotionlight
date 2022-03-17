from machine import Pin
import machine
from time import sleep

class Sensor:
    def __init__(self, pin, pull_down=True):
        self._sensor = Pin(pin, Pin.IN, Pin.PULL_DOWN if pull_down else Pin.PULL_UP)

    def isTriggered(self):
        return self._sensor.value() == 1
    
    def isNotTriggered(self):
        return not self.isTriggered()
    
    
class Led:
    def __init__(self, pin, init_state_off=True, blink_delay=0.5):
        self._led = Pin(pin, Pin.OUT)
        self._blink_delay = blink_delay
        self._led.off() if init_state_off else self._led.on()

    def on(self):
        if self.isOff():
            self._led.high()

    def off(self):
        if self.isOn():
            self._led.low()

    def isOn(self):
        return self._led.value() == 1
    
    def isOff(self):
        return not self.isOn()
    
    def toggle(self):
        self._led.off() if self.isOn() else self.on()
        
    def blink(self):
        self.on()
        self._blink_delay()
        self.off()
        
    def smart_blink(self):
        self.toggle()
        self._blink_delay()
        self.toggle()
        
    def _blinkDelay(self):
        sleep(self._blink_delay)


class MotionTriggeredNightLight:

    def __init__(self, trigger_interval=1, trigger_duration=30):
        self.led = Led(4)
        self.light = Sensor(27)
        self.motion = Sensor(28)
        self.trigger_interval = trigger_interval
        self.trigger_duration = trigger_duration
        self._loop()

    def _loop(self):
        while True:
            print("light sensor TRIGGERED") if self.light.isTriggered() else print("light sensor SLEEPING")
            print("motion sensor TRIGGERED") if self.motion.isTriggered() else print("motion sensor SLEEPING")
            if self.light.isTriggered():
                print("dark enough - waiting for motion")
                while self.motion.isTriggered():
                    print(f"motion sensor triggered - LED on and checking again in {self.trigger_duration}")
                    self.led.on()
                    sleep(self.trigger_duration)  
            self.led.off()
            sleep(self.trigger_interval)
    

if __name__ == "__main__":
    MotionTriggeredNightLight()



