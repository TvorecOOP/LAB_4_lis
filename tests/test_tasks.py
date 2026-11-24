import pytest

from tasks.task1 import first_n, city_generator, DEFAULT_CITIES
from tasks.task2 import random_tuples_generator, build_matrix
from tasks.task3 import words_to_table, format_table
from exceptions import EmptyInputError, InvalidRangeError, InvalidLengthError


def test_city_first_20_cycles():
    r = first_n(DEFAULT_CITIES, 20)
    assert len(r) == 20
    assert r[0] == "Москва"
    assert r[6] == "Москва"
    assert r[5] == "Тула"


def test_city_empty_raises():
    with pytest.raises(EmptyInputError):
        list(city_generator([], 5))


def test_city_invalid_total():
    with pytest.raises(ValueError):
        list(city_generator(DEFAULT_CITIES, 0))


def test_random_tuple_length_and_range():
    for t in random_tuples_generator(5, -5, 5, count=10):
        assert len(t) == 5
        assert all(-5 <= x <= 5 for x in t)


def test_build_matrix_shape():
    m = build_matrix(20, 20, -5, 5)
    assert len(m) == 20
    assert all(len(row) == 20 for row in m)
    assert all(-5 <= x <= 5 for row in m for x in row)


def test_matrix_invalid_range():
    with pytest.raises(InvalidRangeError):
        build_matrix(5, 5, 10, 0)


def test_matrix_invalid_size():
    with pytest.raises(InvalidLengthError):
        build_matrix(0, 5)


def test_words_table_full_rows():
    assert words_to_table("a b c d e f") == [("a", "b", "c"), ("d", "e", "f")]


def test_words_table_drop_remainder():
    assert words_to_table("a b c d e") == [("a", "b", "c")]


def test_words_table_empty():
    with pytest.raises(EmptyInputError):
        words_to_table("   ")


def test_format_table():
    assert format_table([("a", "b", "c"), ("d", "e", "f")]) == "a b c\nd e f"
