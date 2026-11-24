class LabError(Exception):
    """Базовое исключение лабораторной."""


class EmptyInputError(LabError):
    """Пустой ввод."""


class InvalidRangeError(LabError):
    """Некорректный диапазон (a > b)."""


class InvalidLengthError(LabError):
    """Некорректная длина/размер."""


class InvalidWorkerCountError(LabError):
    """Некорректное число воркеров."""
