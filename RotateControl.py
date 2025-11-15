import RPi.GPIO as GPIO
import time

out1 = 16
out2 = 11
out3 = 18
out4 = 13

i = 0
positive = 0
negative = 0
y = 0
with open("test.txt", "r") as file:
    start = int(file.read())
C = 200
# C=int(input())
A = C
B = -C
flag = False

print(A, B)
rotate=C
GPIO.setmode(GPIO.BOARD)
GPIO.setup(out1, GPIO.OUT)
GPIO.setup(out2, GPIO.OUT)
GPIO.setup(out3, GPIO.OUT)
GPIO.setup(out4, GPIO.OUT)

try:
    while (1):
        GPIO.output(out1, GPIO.LOW)
        GPIO.output(out2, GPIO.LOW)
        GPIO.output(out3, GPIO.LOW)
        GPIO.output(out4, GPIO.LOW)

        if flag:
            x = A
        else:
            x = B
        # x = int(input())
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
                    # time.sleep(1)
                elif i == 1:
                    GPIO.output(out1, GPIO.HIGH)
                    GPIO.output(out2, GPIO.HIGH)
                    GPIO.output(out3, GPIO.LOW)
                    GPIO.output(out4, GPIO.LOW)
                    time.sleep(0.03)
                    # time.sleep(1)
                elif i == 2:
                    GPIO.output(out1, GPIO.LOW)
                    GPIO.output(out2, GPIO.HIGH)
                    GPIO.output(out3, GPIO.LOW)
                    GPIO.output(out4, GPIO.LOW)
                    time.sleep(0.03)
                    # time.sleep(1)
                elif i == 3:
                    GPIO.output(out1, GPIO.LOW)
                    GPIO.output(out2, GPIO.HIGH)
                    GPIO.output(out3, GPIO.HIGH)
                    GPIO.output(out4, GPIO.LOW)
                    time.sleep(0.03)
                    # time.sleep(1)
                elif i == 4:
                    GPIO.output(out1, GPIO.LOW)
                    GPIO.output(out2, GPIO.LOW)
                    GPIO.output(out3, GPIO.HIGH)
                    GPIO.output(out4, GPIO.LOW)
                    time.sleep(0.03)
                    # time.sleep(1)
                elif i == 5:
                    GPIO.output(out1, GPIO.LOW)
                    GPIO.output(out2, GPIO.LOW)
                    GPIO.output(out3, GPIO.HIGH)
                    GPIO.output(out4, GPIO.HIGH)
                    time.sleep(0.03)
                    # time.sleep(1)
                elif i == 6:
                    GPIO.output(out1, GPIO.LOW)
                    GPIO.output(out2, GPIO.LOW)
                    GPIO.output(out3, GPIO.LOW)
                    GPIO.output(out4, GPIO.HIGH)
                    time.sleep(0.03)
                    # time.sleep(1)
                elif i == 7:
                    GPIO.output(out1, GPIO.HIGH)
                    GPIO.output(out2, GPIO.LOW)
                    GPIO.output(out3, GPIO.LOW)
                    GPIO.output(out4, GPIO.HIGH)
                    time.sleep(0.03)
                    # time.sleep(1)
                if i == 7:
                    i = 0
                    continue
                i = i + 1

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
                    # time.sleep(1)
                elif i == 1:
                    GPIO.output(out1, GPIO.HIGH)
                    GPIO.output(out2, GPIO.HIGH)
                    GPIO.output(out3, GPIO.LOW)
                    GPIO.output(out4, GPIO.LOW)
                    time.sleep(0.03)
                    # time.sleep(1)
                elif i == 2:
                    GPIO.output(out1, GPIO.LOW)
                    GPIO.output(out2, GPIO.HIGH)
                    GPIO.output(out3, GPIO.LOW)
                    GPIO.output(out4, GPIO.LOW)
                    time.sleep(0.03)
                    # time.sleep(1)
                elif i == 3:
                    GPIO.output(out1, GPIO.LOW)
                    GPIO.output(out2, GPIO.HIGH)
                    GPIO.output(out3, GPIO.HIGH)
                    GPIO.output(out4, GPIO.LOW)
                    time.sleep(0.03)
                    # time.sleep(1)
                elif i == 4:
                    GPIO.output(out1, GPIO.LOW)
                    GPIO.output(out2, GPIO.LOW)
                    GPIO.output(out3, GPIO.HIGH)
                    GPIO.output(out4, GPIO.LOW)
                    time.sleep(0.03)
                    # time.sleep(1)
                elif i == 5:
                    GPIO.output(out1, GPIO.LOW)
                    GPIO.output(out2, GPIO.LOW)
                    GPIO.output(out3, GPIO.HIGH)
                    GPIO.output(out4, GPIO.HIGH)
                    time.sleep(0.03)
                    # time.sleep(1)
                elif i == 6:
                    GPIO.output(out1, GPIO.LOW)
                    GPIO.output(out2, GPIO.LOW)
                    GPIO.output(out3, GPIO.LOW)
                    GPIO.output(out4, GPIO.HIGH)
                    time.sleep(0.03)
                    # time.sleep(1)
                elif i == 7:
                    GPIO.output(out1, GPIO.HIGH)
                    GPIO.output(out2, GPIO.LOW)
                    GPIO.output(out3, GPIO.LOW)
                    GPIO.output(out4, GPIO.HIGH)
                    time.sleep(0.03)
                    # time.sleep(1)
                if i == 0:
                    i = 7
                    continue
                i = i - 1
        flag = not flag

except KeyboardInterrupt:
    GPIO.cleanup()
if __name__=="__main__":
    exec1()

