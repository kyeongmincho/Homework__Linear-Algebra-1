from lib.matrix import *

try:
    # a = Matrix(((1, 2, -1, -4),
    #             (2, 3, -1, -12),
    #             (-2, 0, -3, 2)))
    a = Matrix(((12, 4, -2, 17),
                (1, 2, 3, 14),
                (-3, -4, 5, -2)))
    a.to_reduced_row_echelon_form()
    a.print()

except Exception as e:
    print('Error: ' + e.args[0])
