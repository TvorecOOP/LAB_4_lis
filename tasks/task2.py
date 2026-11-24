from random import randint

from exceptions import InvalidRangeError, InvalidLengthError

# ===== НАСТРОЙКИ =====
DEFAULT_ROWS = 20      # строк матрицы
DEFAULT_COLS = 20      # столбцов матрицы
DEFAULT_MIN = -5       # минимум диапазона случайных чисел
DEFAULT_MAX = 5        # максимум диапазона случайных чисел
# =====================

def random_tuples_generator(n, a, b, count=None):
    """Генератор кортежей длиной n из случайных целых в [a; b]. count=None - бесконечно."""
    if n <= 0:
        raise InvalidLengthError("n должно быть > 0")
    if a > b:
        raise InvalidRangeError(f"a={a} должно быть <= b={b}")

    produced = 0
    while count is None or produced < count:
        yield tuple(randint(a, b) for _ in range(n))
        produced += 1


def build_matrix(rows=None, cols=None, a=None, b=None):
    if rows is None:
        rows = DEFAULT_ROWS
    if cols is None:
        cols = DEFAULT_COLS
    if a is None:
        a = DEFAULT_MIN
    if b is None:
        b = DEFAULT_MAX

    if rows <= 0 or cols <= 0:
        raise InvalidLengthError("rows и cols должны быть > 0")
    if a > b:
        raise InvalidRangeError(f"a={a} должно быть <= b={b}")

    gen = random_tuples_generator(cols, a, b, count=rows)
    return [list(row) for row in gen]


def format_matrix(matrix):
    return "\n".join(" ".join(f"{x:3d}" for x in row) for row in matrix)
