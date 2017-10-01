from fractions import Fraction


class Matrix:
    """
    행렬을 나타내는 클래스.
    """

    def __init__(self, rows):
        """
        행렬 클래스의 initiator.

        :param rows: 행렬의 각각의 원소인 integer 혹은 Fraction들로 구성된
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

        self.nr_row = len(self.rows)

    def to_reduced_row_echelon_form(self):
        pending_col_idx = 0
        for i in range(0, self.nr_row):
            if not self._can_be_pivot(row_idx=i, col_idx=pending_col_idx):
                avail_pivot_idx = self._find_available_pivot(row_idx_upper_bound=i, col_idx=pending_col_idx)
                if avail_pivot_idx is None:
                    continue
                self._swap_rows(i, avail_pivot_idx)

            self._make_one_row_echelon_form(row_idx=i, col_idx=pending_col_idx)
            self._add_other_rows_from_echelon_form_row(echelon_form_row_idx=i, pivot_col_idx=pending_col_idx)
            pending_col_idx += 1

            self.print()
            print("----------------------------------")

    def print(self):
        """
        행렬 전체를 출력한다.
        """
        form_str = '{:>' + str(self._get_max_len_elem_str()) + 's}'

        for i in range(0, self.nr_row):
            for j in range(0, self.nr_column):
                print(form_str.format(str(self.rows[i][j])), end='  ')

            print('')

    def _get_max_len_elem_str(self):
        max_len = 0
        for i in range(0, self.nr_row):
            for j in range(0, self.nr_column):
                cur_len = len(str(self.rows[i][j]))
                if cur_len > max_len:
                    max_len = cur_len

        return max_len

    def _make_one_row_echelon_form(self, row_idx, col_idx):
        rev = Fraction(self.rows[row_idx][col_idx].denominator, self.rows[row_idx][col_idx].numerator)
        for i in range(col_idx, self.nr_column):
            self.rows[row_idx][i] *= rev

    def _add_other_rows_from_echelon_form_row(self, echelon_form_row_idx, pivot_col_idx):
        pivot_row = self.rows[echelon_form_row_idx]
        for r_i in range(0, self.nr_row):
            if r_i == echelon_form_row_idx:
                continue

            rev_coefficient = -self.rows[r_i][pivot_col_idx]
            for c_i in range(pivot_col_idx, self.nr_column):
                self.rows[r_i][c_i] += pivot_row[c_i] * rev_coefficient

    def _can_be_pivot(self, row_idx, col_idx):
        return self.rows[row_idx][col_idx] != 0

    def _find_available_pivot(self, row_idx_upper_bound, col_idx):
        for i in range(row_idx_upper_bound + 1, self.nr_row):
            if self.rows[i][col_idx] != 0:
                return i
        return None

    def _swap_rows(self, first_idx, second_idx):
        self.rows[second_idx], self.rows[first_idx] = self.rows[first_idx], self.rows[second_idx]
