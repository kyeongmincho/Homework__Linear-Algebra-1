from lib.matrix import *

try:
    # sm = SquareMatrix([[8, 5]])  # 1x1
    # sm = SquareMatrix([[2, 3, 10],  # 2x2
    #                   [6, 10, -4]])
    sm = SquareMatrix([[1, 2, -1, -4],  # 3x3
                      [2, 3, -1, -12],
                      [-2, 0, -3, 2]])
    # sm = SquareMatrix([[1, 2, -1, 1, -4],  # 4x4
    #                   [1, 7, 5, 4, -12],
    #                   [1, 2, 5, 6, -12],
    #                   [1, 2, 2, 7, -12]])
    # sm = SquareMatrix([[1, 2, -1, 1, 3, -4],  # 5x5
    #                   [6, 2, 23, 4, 12, 89182734981723],
    #                   [7, 6, 2, 8, 12, -2],
    #                   [8, 5, -9, 7, 66, -12],
    #                   [15, 2, -34, 1, 4, -86]])

    sm.to_reduced_row_echelon_form()
    sm.print()

except Exception as e:
    print('Error: ' + e.args[0])
