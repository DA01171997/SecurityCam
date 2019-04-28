import RPi.GPIO as GPIO
import time

class RangeFinder:
    """
    this class handles the GPIO functions needed to measure distance
    using the HC-SR04 sonic distance sensor on a breadboard

    configurable attributes:
        sample_size -> number of samples used to derive distance
        settle_time -> how long to wait for the sensor to settle
    
    other attributes:
        trigger_pin -> pin number for the trigger function of the sensor
        echo_pin -> pin number for the echo function of the sensor
    """
    def __init__(self, sample_size=3, settle_time=1):
        self.sample_size = sample_size
        self.settle_time = settle_time
        self.trigger_pin = 7
        self.echo_pin = 11
        GPIO.setmode(GPIO.BOARD)    # setup GPIO for breadboard
        GPIO.setup(self.trigger_pin, GPIO.OUT)  # setup trigger as output
        GPIO.setup(self.echo_pin, GPIO.IN)  # setup echo as input

    def _sample(self):
        """
        private method
        retrieves a single distance sample
        """
        pulse_start = None  # pulse times
        pulse_end = None
        distance = -1   # final distance (default -1)

        try:
            GPIO.output(self.trigger_pin, GPIO.LOW) # send low (0) to trigger pin
            time.sleep(self.settle_time)    # wait to settle
            GPIO.output(self.trigger_pin, GPIO.HIGH)    # send high (1) to trigger pin
            time.sleep(0.00001) # wait for echo back
            GPIO.output(self.trigger_pin, GPIO.LOW) # send low (0) to trigger pin

            while GPIO.input(self.echo_pin) == 0:   # as long as echo pin receives a low (0)
                pulse_start = time.time()   # get the pulse time
            
            while GPIO.input(self.echo_pin) == 1:   # as long as echo pin receives a high (1)
                pulse_end = time.time()     # get the pulse time

            duration = pulse_end - pulse_start  # get the difference in pulse times
            distance = round(duration * 17150, 2)   # convert to distance (cm)
        except:
            pass    # keep going if exception occurs

        return distance

    def get_distance(self):
        """
        returns the distance measured in CM
        the distance is retrieved via an average of samples
        this is to protect against unexpected bad measurements
        """
        samples = []
        while len(samples) < self.sample_size:
            samples.append(self._sample())
        samples = list(filter(lambda x: x < 0, samples))
        dist = sum(samples) / len(samples)
        return dist

    def __del__(self):
        GPIO.cleanup()
