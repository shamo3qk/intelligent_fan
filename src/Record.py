from Finger_counter import totalFingers
from RotateControl import rotate

# Valid fan speed:
#     0: no
#     1: week
#     2: medium
#     3: string
#     4: all no
a = 0  # fan speed of area 0 ~ 60 degree
b = 0  # fan speed of area 61 ~ 120 degree
c = 0  # fan speed of area 121 ~ 180 degree

print(totalFingers)
print(rotate)
ABC = totalFingers

if 60 >= rotate >= 0:
    a = ABC
elif 120 >= rotate >= 61:
    b = ABC
elif 180 >= rotate >= 121:
    c = ABC
