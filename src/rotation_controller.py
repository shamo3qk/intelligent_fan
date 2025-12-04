import RPi.GPIO as GPIO

# Pin for step motor driver
out1 = 16
out2 = 11
out3 = 18
out4 = 13
PINS = [out1, out2, out3, out4]

# step sequence of step motor
step_sequence = [
    [GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.LOW],
    [GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.LOW],
    [GPIO.LOW, GPIO.HIGH, GPIO.LOW, GPIO.LOW],
    [GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW],
    [GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.LOW],
    [GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH],
    [GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.HIGH],
    [GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH],
]

MAX_STEP = 200  # rotate 0.9 degree per step, total 180 degree


def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(out1, GPIO.OUT)
    GPIO.setup(out2, GPIO.OUT)
    GPIO.setup(out3, GPIO.OUT)
    GPIO.setup(out4, GPIO.OUT)


def reset():
    GPIO.output(out1, GPIO.LOW)
    GPIO.output(out2, GPIO.LOW)
    GPIO.output(out3, GPIO.LOW)
    GPIO.output(out4, GPIO.LOW)


def step_motor(current_sequence: int, is_clockwise: bool):
    if is_clockwise:
        index = (current_sequence + 1) % len(step_sequence)
    else:
        index = (current_sequence - 1) % len(step_sequence)

    for pin, value in zip(PINS, step_sequence[index]):
        GPIO.output(pin, bool(value))


def run_rotation_controller():
    init()

    current_sequence = 0
    is_clockwise = True

    try:
        while True:
            reset()

            for step in range(0, MAX_STEP, 1):
                step_motor(current_sequence, is_clockwise)

                if is_clockwise:
                    current_sequence = (current_sequence + 1) % len(step_sequence)
                else:
                    current_sequence = (current_sequence - 1) % len(step_sequence)

            is_clockwise = not is_clockwise
    except KeyboardInterrupt:
        GPIO.cleanup()
