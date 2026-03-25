class Matrix:
    def __init__(self, data):
        if not data or not data[0]:
            raise ValueError("빈 행렬은 생성할 수 없습니다")
        self.data = [row[:] for row in data]
        self.rows = len(data)
        self.cols = len(data[0])

    @classmethod
    def zeros(cls, rows, cols):
        return cls([[0] * cols for _ in range(rows)])

    @classmethod
    def ones(cls, rows, cols):
        return cls([[1] * cols for _ in range(rows)])

    @classmethod
    def identity(cls, n):
        data = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        return cls(data)

    @classmethod
    def from_flat(cls, flat_list, rows, cols):
        if len(flat_list) != rows * cols:
            raise ValueError("크기가 맞지 않습니다")
        data = [flat_list[i * cols : (i + 1) * cols] for i in range(rows)]
        return cls(data)

    def __getitem__(self, key):
        if isinstance(key, tuple):
            return self.data[key[0]][key[1]]
        return self.data[key]

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            self.data[key[0]][key[1]] = value
        else:
            self.data[key] = value

    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("행렬 크기가 다릅니다")
        result = [
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def __sub__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("행렬 크기가 다릅니다")
        result = [
            [self.data[i][j] - other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            result = [
                [self.data[i][j] * other for j in range(self.cols)]
                for i in range(self.rows)
            ]
            return Matrix(result)

        if self.cols != other.rows:
            raise ValueError(
                f"행렬 곱셈 불가: ({self.rows}x{self.cols}) * ({other.rows}x{other.cols})"
            )
        result = [
            [
                sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                for j in range(other.cols)
            ]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def transpose(self):
        result = [
            [self.data[j][i] for j in range(self.rows)] for i in range(self.cols)
        ]
        return Matrix(result)

    def determinant(self):
        if self.rows != self.cols:
            raise ValueError("정방행렬이 아닙니다")

        if self.rows == 1:
            return self.data[0][0]

        if self.rows == 2:
            return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]

        det = 0
        for j in range(self.cols):
            minor = self._minor(0, j)
            cofactor = ((-1) ** j) * self.data[0][j] * minor.determinant()
            det += cofactor
        return det

    def _minor(self, row, col):
        data = [
            [self.data[i][j] for j in range(self.cols) if j != col]
            for i in range(self.rows)
            if i != row
        ]
        return Matrix(data)

    def trace(self):
        if self.rows != self.cols:
            raise ValueError("정방행렬이 아닙니다")
        return sum(self.data[i][i] for i in range(self.rows))

    def flatten(self):
        return [x for row in self.data for x in row]

    def map(self, func):
        result = [[func(self.data[i][j]) for j in range(self.cols)] for i in range(self.rows)]
        return Matrix(result)

    def row_echelon(self):
        mat = [row[:] for row in self.data]
        rows, cols = self.rows, self.cols
        current_row = 0

        for col in range(cols):
            max_row = current_row
            for row in range(current_row + 1, rows):
                if abs(mat[row][col]) > abs(mat[max_row][col]):
                    max_row = row

            if abs(mat[max_row][col]) < 1e-10:
                continue

            mat[current_row], mat[max_row] = mat[max_row], mat[current_row]

            pivot = mat[current_row][col]
            mat[current_row] = [x / pivot for x in mat[current_row]]

            for row in range(current_row + 1, rows):
                factor = mat[row][col]
                mat[row] = [
                    mat[row][j] - factor * mat[current_row][j] for j in range(cols)
                ]

            current_row += 1

        return Matrix(mat)

    def __eq__(self, other):
        return self.data == other.data

    def __repr__(self):
        rows_str = []
        for row in self.data:
            rows_str.append("  [" + ", ".join(f"{x:>6.2f}" for x in row) + "]")
        return "Matrix([\n" + "\n".join(rows_str) + "\n])"

    def pretty_print(self):
        col_widths = []
        for j in range(self.cols):
            width = max(len(f"{self.data[i][j]:.2f}") for i in range(self.rows))
            col_widths.append(width)

        for i in range(self.rows):
            row_str = " | ".join(
                f"{self.data[i][j]:>{col_widths[j]}.2f}" for j in range(self.cols)
            )
            print(f"| {row_str} |")


if __name__ == "__main__":
    print("=== 기본 연산 ===")
    a = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    b = Matrix([[9, 8, 7], [6, 5, 4], [3, 2, 1]])

    print("A:")
    a.pretty_print()
    print("\nB:")
    b.pretty_print()

    print("\nA + B:")
    (a + b).pretty_print()

    print("\nA * B:")
    (a * b).pretty_print()

    print(f"\nA 전치:")
    a.transpose().pretty_print()

    print(f"\n대각합: {a.trace()}")

    print("\n=== 단위행렬 ===")
    Matrix.identity(4).pretty_print()

    print("\n=== 행렬식 ===")
    m = Matrix([[1, 2], [3, 4]])
    print(f"det([[1,2],[3,4]]) = {m.determinant()}")

    m3 = Matrix([[2, 1, 3], [0, -1, 2], [1, 4, -1]])
    print(f"det(3x3) = {m3.determinant()}")

    print("\n=== 스칼라 곱 ===")
    (m * 3).pretty_print()

    print("\n=== Row Echelon ===")
    m4 = Matrix([[2, 1, -1, 8], [-3, -1, 2, -11], [-2, 1, 2, -3]])
    m4.row_echelon().pretty_print()
