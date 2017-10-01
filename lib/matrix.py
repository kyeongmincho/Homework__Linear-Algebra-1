from fractions import Fraction


class SquareMatrix:
    """정방행렬을 나타내는 클래스."""

    def __init__(self, rows):
        """정방행렬 클래스의 initiator.
        행렬의 원소를 세팅해준다.

        :param rows: 행렬의 각각의 원소인 integer 혹은 Fraction들로 구성된
                     행렬의 각각의 행인 tuple이나 list들로 구성된
                     tuple이나 list가 들어와야 한다.
                     tuple로 구성된 list, tuple로 구성된 tuple, list로 구성된 list, list로 구성된 tuple
                     어떤 것도 상관 없다.
                     (단, 1x1 행렬의 경우 tuple이 생략되어 버리니 list로 해야함.)

        Examples
        --------

        my_mtrx = SquareMatrix(((1, 0, 1231231, 3),
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

        if self.nr_row + 1 != self.nr_column:
            raise Exception('not a square matrix')

    def to_reduced_row_echelon_form(self):
        """행렬을 reduced row echelon form 형태로 바꾸어준다.
        해가 무한하거나 없는 경우에는 가능한 만큼 1과 0 으로 원소들을 바꾼다.
        먼저 가능한 기준행을 찾은 뒤 다른 행에 적절한 곱을 한 형태를 합하는 방법으로 기준 열의 값을 0으로 만들어준다.
        """
        pending_col_idx = 0
        for i in range(0, self.nr_row):
            pivot_row_idx, pivot_col_idx = self._find_available_pivot(row_idx_lower_bound=i,
                                                                      col_idx_lower_bound=pending_col_idx)
            if pivot_row_idx is None:
                break

            self._swap_rows(i, pivot_row_idx)
            self._make_one_row_echelon_form(row_idx=i, col_idx=pivot_col_idx)
            self._add_other_rows_from_echelon_form_row(echelon_form_row_idx=i, pivot_col_idx=pivot_col_idx)
            pending_col_idx = pivot_col_idx + 1

    def print(self):
        """행렬 전체를 출력한다."""
        form_str = '{:>' + str(self._get_max_len_elem_str()) + 's}'

        for i in range(0, self.nr_row):
            for j in range(0, self.nr_column):
                print(form_str.format(str(self.rows[i][j])), end='  ')

            print('')

    def _get_max_len_elem_str(self):
        """행렬 안의 원소들 중 가장 긴 문자열의 길이를 구한다.

        :return: 행렬 안의 원소들 중 가장 긴 문자열의 길이
        """
        max_len = 0
        for i in range(0, self.nr_row):
            for j in range(0, self.nr_column):
                cur_len = len(str(self.rows[i][j]))
                if cur_len > max_len:
                    max_len = cur_len

        return max_len

    def _make_one_row_echelon_form(self, row_idx, col_idx):
        """한 행을 기준행으로 만들기 위해 기준열의 원소값을 1로 바꾸기 위해 곱하는 작업을 한다.

        :param row_idx: 기준행이 될 행의 인덱스
        :param col_idx: 값이 1이 될 원소의 열 인덱스
        """
        rev = Fraction(self.rows[row_idx][col_idx].denominator, self.rows[row_idx][col_idx].numerator)
        for i in range(col_idx, self.nr_column):
            self.rows[row_idx][i] *= rev

    def _add_other_rows_from_echelon_form_row(self, echelon_form_row_idx, pivot_col_idx):
        """기준행을 이용하여 다른 행들에 적절한 합을 해서 기준열의 원소값을 0으로 만들어준다.

        :param echelon_form_row_idx: 기준행의 인덱스
        :param pivot_col_idx: 0이 될 원소의 열 인덱스
        """
        pivot_row = self.rows[echelon_form_row_idx]
        for r_i in range(0, self.nr_row):
            if r_i == echelon_form_row_idx:
                continue

            rev_coefficient = -self.rows[r_i][pivot_col_idx]
            for c_i in range(pivot_col_idx, self.nr_column):
                self.rows[r_i][c_i] += pivot_row[c_i] * rev_coefficient

    def _find_available_pivot(self, row_idx_lower_bound, col_idx_lower_bound):
        """기준행이 가질 수 있는 가장 왼쪽의 미지수를 찾고 그 행과 열의 인덱스를 구한다.
        이미 기준행이 된 적이 있는 행들을 제외한 행들 중에서 0이 아닌 값을 갖는 원소의 열 인덱스가 가장 작은 행을 찾는다.
        WARNING: 가장 오른쪽 열의 원소들은 미지수가 아니므로 참조하지 않는다.

        :param row_idx_lower_bound: 기준행이 된 적이 없는 행들 중 가장 작은 인덱스
        :param col_idx_lower_bound: 기준열이 된 적이 없는 열들 중 가장 작은 인덱스
        :return: 다음으로 기준행이 될 행의 인덱스와 그 행에서 1이 될 열의 인덱스
        """
        min_row_idx = None
        min_col_idx = None
        for i in range(row_idx_lower_bound, self.nr_row):
            for j in range(col_idx_lower_bound, self.nr_column - 1):
                if self.rows[i][j] != 0:
                    if min_col_idx is None or j < min_col_idx:
                        min_row_idx = i
                        min_col_idx = j
                        break
            if min_col_idx == col_idx_lower_bound:
                return min_row_idx, min_col_idx

        return min_row_idx, min_col_idx

    def _swap_rows(self, first_idx, second_idx):
        """행과 행의 순서를 교체한다.
        두 개의 파라미터는 같을 수도 있다 (변화가 없음)

        :param first_idx: 바꿀 행 중 하나
        :param second_idx: 바꿀 행 중 다른 하나
        """
        self.rows[second_idx], self.rows[first_idx] = self.rows[first_idx], self.rows[second_idx]
