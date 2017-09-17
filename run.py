from lib.matrix import *

try:
    a = Matrix(((1, 0, 12323231, 3),
                (2, 3, 4, 3241),
                (-1, -3, -3, -4)))
    a.print()
except Exception as e:
    print('Error: ' + e.args[0])
