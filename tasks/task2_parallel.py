"""Параллельная версия генерации матрицы с разбиением на чанки."""
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from dataclasses import dataclass, asdict

from tasks.task2 import (
    build_matrix, random_tuples_generator,
    DEFAULT_ROWS, DEFAULT_COLS, DEFAULT_MIN, DEFAULT_MAX,
)
from exceptions import InvalidWorkerCountError, InvalidLengthError, InvalidRangeError

# ===== НАСТРОЙКИ =====
DEFAULT_WORKERS = 8          # число потоков/процессов
BENCH_ROWS = 2000            # размер матрицы для бенчмарка (строк) - увеличено для наглядного ускорения
BENCH_COLS = 2000            # размер матрицы для бенчмарка (столбцов)
BENCH_MIN = -5
BENCH_MAX = 5
# =====================


@dataclass
class TimingResult:
    label: str
    seconds: float
    rows: int
    cols: int

    def as_dict(self):
        return asdict(self)


def _generate_chunk(args):
    """Генерирует rows_per_chunk строк, каждая длиной cols. Возвращает список списков."""
    rows_per_chunk, cols, a, b = args
    return [list(row) for row in random_tuples_generator(cols, a, b, count=rows_per_chunk)]


def _split_into_chunks(total, parts):
    """Делит total на parts примерно равных частей."""
    base = total // parts
    rem = total % parts
    return [base + (1 if i < rem else 0) for i in range(parts)]


def build_matrix_threaded(rows, cols, a, b, workers=None):
    if workers is None:
        workers = DEFAULT_WORKERS
    if rows <= 0 or cols <= 0:
        raise InvalidLengthError("rows и cols должны быть > 0")
    if a > b:
        raise InvalidRangeError(f"a={a} должно быть <= b={b}")
    if workers <= 0:
        raise InvalidWorkerCountError("workers должно быть > 0")

    chunk_sizes = _split_into_chunks(rows, workers)
    tasks = [(size, cols, a, b) for size in chunk_sizes if size > 0]

    with ThreadPoolExecutor(max_workers=workers) as ex:
        chunks = list(ex.map(_generate_chunk, tasks))
    return [row for chunk in chunks for row in chunk]


def build_matrix_multiproc(rows, cols, a, b, workers=None):
    if workers is None:
        workers = DEFAULT_WORKERS
    if rows <= 0 or cols <= 0:
        raise InvalidLengthError("rows и cols должны быть > 0")
    if a > b:
        raise InvalidRangeError(f"a={a} должно быть <= b={b}")
    if workers <= 0:
        raise InvalidWorkerCountError("workers должно быть > 0")

    chunk_sizes = _split_into_chunks(rows, workers)
    tasks = [(size, cols, a, b) for size in chunk_sizes if size > 0]

    with ProcessPoolExecutor(max_workers=workers) as ex:
        chunks = list(ex.map(_generate_chunk, tasks))
    return [row for chunk in chunks for row in chunk]


def benchmark(rows=None, cols=None, a=None, b=None, workers=None):
    if rows is None:
        rows = BENCH_ROWS
    if cols is None:
        cols = BENCH_COLS
    if a is None:
        a = BENCH_MIN
    if b is None:
        b = BENCH_MAX
    if workers is None:
        workers = DEFAULT_WORKERS

    results = []

    t0 = time.perf_counter()
    build_matrix(rows, cols, a, b)
    results.append(TimingResult("sequential", time.perf_counter() - t0, rows, cols))

    t0 = time.perf_counter()
    build_matrix_threaded(rows, cols, a, b, workers)
    results.append(TimingResult("threaded", time.perf_counter() - t0, rows, cols))

    t0 = time.perf_counter()
    build_matrix_multiproc(rows, cols, a, b, workers)
    results.append(TimingResult("multiprocess", time.perf_counter() - t0, rows, cols))

    return results


def format_benchmark(results):
    base = results[0].seconds
    lines = [f"{'mode':<14}{'time, s':>10}{'speedup':>10}"]
    lines.append("-" * 34)
    for r in results:
        speedup = base / r.seconds if r.seconds else 0.0
        lines.append(f"{r.label:<14}{r.seconds:>10.4f}{speedup:>9.2f}x")
    return "\n".join(lines)
