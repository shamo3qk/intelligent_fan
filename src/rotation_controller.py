import time

import RPi.GPIO as GPIO

# Pin for step motor driver
out1 = 16
out2 = 11
out3 = 18
out4 = 13

i = 0  # range: 0 ~ 7, step 1 ~ 8 of step motor
positive = 0
negative = 0
y = 0

C = 200
A = C
B = -C

flag = False

rotate = C  # current angle of fan's forward direction


def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(out1, GPIO.OUT)
    GPIO.setup(out2, GPIO.OUT)
    GPIO.setup(out3, GPIO.OUT)
    GPIO.setup(out4, GPIO.OUT)


def run_rotation_controller():
    init()

    try:
        while True:
            GPIO.output(out1, GPIO.LOW)
            GPIO.output(out2, GPIO.LOW)
            GPIO.output(out3, GPIO.LOW)
            GPIO.output(out4, GPIO.LOW)

            if flag:
                x = A  # x =  200
            else:
                x = B  # x = -200
            if x > 0 and x <= 400:
                for y in range(x, 0, -1):
                    if negative == 1:
                        if i == 7:
                            i = 0
                        else:
                            i = i + 1
                        y = y + 2
                        negative = 0
                    positive = 1
                    print(y)
                    if i == 0:
                        GPIO.output(out1, GPIO.HIGH)
                        GPIO.output(out2, GPIO.LOW)
                        GPIO.output(out3, GPIO.LOW)
                        GPIO.output(out4, GPIO.LOW)
                        time.sleep(0.03)
                    elif i == 1:
                        GPIO.output(out1, GPIO.HIGH)
                        GPIO.output(out2, GPIO.HIGH)
                        GPIO.output(out3, GPIO.LOW)
                        GPIO.output(out4, GPIO.LOW)
                        time.sleep(0.03)
                    elif i == 2:
                        GPIO.output(out1, GPIO.LOW)
                        GPIO.output(out2, GPIO.HIGH)
                        GPIO.output(out3, GPIO.LOW)
                        GPIO.output(out4, GPIO.LOW)
                        time.sleep(0.03)
                    elif i == 3:
                        GPIO.output(out1, GPIO.LOW)
                        GPIO.output(out2, GPIO.HIGH)
                        GPIO.output(out3, GPIO.HIGH)
                        GPIO.output(out4, GPIO.LOW)
                        time.sleep(0.03)
                    elif i == 4:
                        GPIO.output(out1, GPIO.LOW)
                        GPIO.output(out2, GPIO.LOW)
                        GPIO.output(out3, GPIO.HIGH)
                        GPIO.output(out4, GPIO.LOW)
                        time.sleep(0.03)
                    elif i == 5:
                        GPIO.output(out1, GPIO.LOW)
                        GPIO.output(out2, GPIO.LOW)
                        GPIO.output(out3, GPIO.HIGH)
                        GPIO.output(out4, GPIO.HIGH)
                        time.sleep(0.03)
                    elif i == 6:
                        GPIO.output(out1, GPIO.LOW)
                        GPIO.output(out2, GPIO.LOW)
                        GPIO.output(out3, GPIO.LOW)
                        GPIO.output(out4, GPIO.HIGH)
                        time.sleep(0.03)
                    elif i == 7:
                        GPIO.output(out1, GPIO.HIGH)
                        GPIO.output(out2, GPIO.LOW)
                        GPIO.output(out3, GPIO.LOW)
                        GPIO.output(out4, GPIO.HIGH)
                        time.sleep(0.03)

                    i = (i + 1) % 8
            elif x < 0 and x >= -400:
                x = x * -1
                for y in range(x, 0, -1):
                    if positive == 1:
                        if i == 0:
                            i = 7
                        else:
                            i = i - 1
                        y = y + 3
                        positive = 0
                    negative = 1
                    print(-y)
                    if i == 0:
                        GPIO.output(out1, GPIO.HIGH)
                        GPIO.output(out2, GPIO.LOW)
                        GPIO.output(out3, GPIO.LOW)
                        GPIO.output(out4, GPIO.LOW)
                        time.sleep(0.03)
                    elif i == 1:
                        GPIO.output(out1, GPIO.HIGH)
                        GPIO.output(out2, GPIO.HIGH)
                        GPIO.output(out3, GPIO.LOW)
                        GPIO.output(out4, GPIO.LOW)
                        time.sleep(0.03)
                    elif i == 2:
                        GPIO.output(out1, GPIO.LOW)
                        GPIO.output(out2, GPIO.HIGH)
                        GPIO.output(out3, GPIO.LOW)
                        GPIO.output(out4, GPIO.LOW)
                        time.sleep(0.03)
                    elif i == 3:
                        GPIO.output(out1, GPIO.LOW)
                        GPIO.output(out2, GPIO.HIGH)
                        GPIO.output(out3, GPIO.HIGH)
                        GPIO.output(out4, GPIO.LOW)
                        time.sleep(0.03)
                    elif i == 4:
                        GPIO.output(out1, GPIO.LOW)
                        GPIO.output(out2, GPIO.LOW)
                        GPIO.output(out3, GPIO.HIGH)
                        GPIO.output(out4, GPIO.LOW)
                        time.sleep(0.03)
                    elif i == 5:
                        GPIO.output(out1, GPIO.LOW)
                        GPIO.output(out2, GPIO.LOW)
                        GPIO.output(out3, GPIO.HIGH)
                        GPIO.output(out4, GPIO.HIGH)
                        time.sleep(0.03)
                    elif i == 6:
                        GPIO.output(out1, GPIO.LOW)
                        GPIO.output(out2, GPIO.LOW)
                        GPIO.output(out3, GPIO.LOW)
                        GPIO.output(out4, GPIO.HIGH)
                        time.sleep(0.03)
                    elif i == 7:
                        GPIO.output(out1, GPIO.HIGH)
                        GPIO.output(out2, GPIO.LOW)
                        GPIO.output(out3, GPIO.LOW)
                        GPIO.output(out4, GPIO.HIGH)
                        time.sleep(0.03)
                    if i == 0:
                        i = 7
                        continue
                    i = i - 1
            flag = not flag
    except KeyboardInterrupt:
        GPIO.cleanup()
