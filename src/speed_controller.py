import RPi.GPIO as GPIO

from Record import a, b, c
from rotation_controller import rotate

# Pin for relay channels
Relay_Ch1 = 26
Relay_Ch2 = 20
Relay_Ch3 = 21

speed_levels = [
    [GPIO.LOW, GPIO.HIGH, GPIO.HIGH],  # Weak
    [GPIO.HIGH, GPIO.LOW, GPIO.HIGH],  # Medium
    [GPIO.HIGH, GPIO.HIGH, GPIO.LOW],  # Strong
]


def set_speed_level(level: int) -> None:
    speed_level = speed_levels[level]
    GPIO.output(Relay_Ch1, bool(speed_level[0]))
    GPIO.output(Relay_Ch2, bool(speed_level[1]))
    GPIO.output(Relay_Ch3, bool(speed_level[2]))


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
                    set_speed_level(1)
                elif a + b + c == 2 or a == b == c == 2:
                    set_speed_level(2)
                elif a + b + c == 3 or a == b == c == 3:
                    set_speed_level(3)
    except KeyboardInterrupt:
        GPIO.cleanup()
