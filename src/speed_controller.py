import RPi.GPIO as GPIO

from Record import a, b, c
from rotation_controller import rotate

# Pin for relay channels
Relay_Ch1 = 26
Relay_Ch2 = 20
Relay_Ch3 = 21


def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(Relay_Ch1, GPIO.OUT)
    GPIO.setup(Relay_Ch2, GPIO.OUT)
    GPIO.setup(Relay_Ch3, GPIO.OUT)


def run_speed_controller():
    init()

    try:
        while True:
            if 3 >= (a + b + c) >= 1 or a == b == c:
                if a + b + c == 1 or a == b == c == 1:
                    GPIO.output(Relay_Ch1, GPIO.LOW)
                    GPIO.output(Relay_Ch2, GPIO.HIGH)
                    GPIO.output(Relay_Ch3, GPIO.HIGH)
                elif a + b + c == 2 or a == b == c == 2:
                    GPIO.output(Relay_Ch1, GPIO.HIGH)
                    GPIO.output(Relay_Ch2, GPIO.LOW)
                    GPIO.output(Relay_Ch3, GPIO.HIGH)
                elif a + b + c == 3 or a == b == c == 3:
                    GPIO.output(Relay_Ch1, GPIO.HIGH)
                    GPIO.output(Relay_Ch2, GPIO.HIGH)
                    GPIO.output(Relay_Ch3, GPIO.LOW)

            # if totalFingers == 0:
            #     GPIO.output(Relay_Ch1, GPIO.HIGH)
            #     GPIO.output(Relay_Ch2, GPIO.HIGH)
            #     GPIO.output(Relay_Ch3, GPIO.HIGH)
            # elif totalFingers == 1:
            #     GPIO.output(Relay_Ch1, GPIO.LOW)
            #     GPIO.output(Relay_Ch2, GPIO.HIGH)
            #     GPIO.output(Relay_Ch3, GPIO.HIGH)
            # elif totalFingers == 2:
            #     GPIO.output(Relay_Ch1, GPIO.HIGH)
            #     GPIO.output(Relay_Ch2, GPIO.LOW)
            #     GPIO.output(Relay_Ch3, GPIO.HIGH)
            # elif totalFingers == 3:
            #     GPIO.output(Relay_Ch1, GPIO.HIGH)
            #     GPIO.output(Relay_Ch2, GPIO.HIGH)
            #     GPIO.output(Relay_Ch3, GPIO.LOW)
    except KeyboardInterrupt:
        GPIO.cleanup()
