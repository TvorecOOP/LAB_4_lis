import pytest

from tasks.task2_parallel import (
    build_matrix_threaded, build_matrix_multiproc,
    benchmark, format_benchmark,
)
from exceptions import InvalidWorkerCountError, InvalidRangeError


def test_threaded_matches_shape():
    m = build_matrix_threaded(10, 10, -5, 5, workers=2)
    assert len(m) == 10
    assert all(len(r) == 10 for r in m)
    assert all(-5 <= x <= 5 for r in m for x in r)


def test_multiproc_matches_shape():
    m = build_matrix_multiproc(10, 10, -5, 5, workers=2)
    assert len(m) == 10
    assert all(-5 <= x <= 5 for r in m for x in r)


def test_invalid_workers_threaded():
    with pytest.raises(InvalidWorkerCountError):
        build_matrix_threaded(5, 5, -1, 1, workers=0)


def test_invalid_workers_multiproc():
    with pytest.raises(InvalidWorkerCountError):
        build_matrix_multiproc(5, 5, -1, 1, workers=0)


def test_invalid_range_parallel():
    with pytest.raises(InvalidRangeError):
        build_matrix_multiproc(5, 5, 10, 0)


def test_benchmark_returns_three_modes():
    res = benchmark(rows=20, cols=20, workers=2)
    labels = [r.label for r in res]
    assert labels == ["sequential", "threaded", "multiprocess"]
    assert all(r.seconds >= 0 for r in res)


def test_format_benchmark_contains_speedup():
    res = benchmark(rows=10, cols=10, workers=2)
    s = format_benchmark(res)
    assert "speedup" in s
    assert "multiprocess" in s
