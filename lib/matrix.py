from fractions import Fraction


class Matrix:
    """
    행렬을 나타내는 클래스.
    """

    def __init__(self, rows):
        """
        행렬 클래스의 initiator.

        :param rows: 행렬의 각각의 원소인 integer를로 구성된
                     행렬의 각각의 행인 tuple이나 list들로 구성된
                     tuple이나 list가 들어와야 한다.
                     tuple로 구성된 list, tuple로 구성된 tuple, list로 구성된 list, list로 구성된 tuple
                     어떤 것도 상관 없다.

        ex) my_mtrx = Matrix(((1, 0, 1231231, 3),
                              (2, 3, 4, 3241),
                              (-1, -3, -3, -4)))
        """
        if type(rows) is not list and type(rows) is not tuple:
            raise Exception('matrix param must be list or tuple')

        self.rows = []
        self.nr_column = None
        self.nr_max_width = None

        for r in rows:
            if type(r) is not list and type(r) is not tuple:
                raise Exception('cannot make matrix by not iterable param')
            elif self.nr_column is not None and self.nr_column != len(r):
                raise Exception('each row has different size of columns')

            self.nr_column = len(r) if self.nr_column is None else self.nr_column
            self.rows.append([])

            for c in r:
                if type(c) is not int and type(c) is not Fraction:
                    raise Exception('matrix must consist of integers or fractions')

                if type(c) is int:
                    new_elem = Fraction(c, 1)
                else:  # Fraction
                    new_elem = Fraction(c)

                self.rows[-1].append(new_elem)
                len_new_elem = len(str(new_elem.numerator) + '/' + str(new_elem.denominator))
                self.nr_max_width = len_new_elem \
                    if self.nr_max_width is None or len_new_elem > self.nr_max_width \
                    else self.nr_max_width

        self.nr_row = len(self.rows)

    def print(self):
        """
        행렬 전체를 출력한다.
        """

        form_str = '{:' + str(self.nr_max_width) + 's}'

        for r in self.rows:
            for c in r:
                if c.denominator == 1:
                    printed_str = str(c.numerator)
                else:
                    printed_str = str(c.numerator) + '/' + str(c.denominator)

                print(form_str.format(printed_str), end='  ')

            print('')

    def to_reduced_row_echelon_form(self):
        return
