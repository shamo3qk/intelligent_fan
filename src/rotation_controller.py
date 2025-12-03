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

y = 0

C = 200
A = C
B = -C

rotate = C  # current angle of fan's forward direction


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


def run_rotation_controller():
    init()

    positive = False
    negative = False
    flag = False
    i = 0  # sequence index

    try:
        while True:
            reset()

            if flag:
                x = A  # x =  200
            else:
                x = B  # x = -200

            if x > 0 and x <= 400:
                for y in range(x, 0, -1):
                    if negative:
                        y = y + 2
                        negative = False

                    positive = True
                    print(y)

                    for pin, value in zip(PINS, step_sequence[i]):
                        GPIO.output(pin, bool(value))

                    i = (i + 1) % len(step_sequence)
            elif x < 0 and x >= -400:
                x = x * -1
                for y in range(x, 0, -1):
                    if positive:
                        y = y + 3
                        positive = False

                    negative = True
                    print(-y)

                    for pin, value in zip(PINS, step_sequence[i]):
                        GPIO.output(pin, bool(value))

                    i = (i - 1) % len(step_sequence)

            flag = not flag
    except KeyboardInterrupt:
        GPIO.cleanup()
