# ЛР №4 — Вариант 15 (Rare + Medium + Well-done)

## Название
Генераторы, встроенные функции Python и параллельная генерация данных

## Описание
Приложение с GUI (PySide6, TabWidget) реализует 3 задачи варианта 15:

1. **Города по циклу** — генератор циклически выдаёт города 1 000 000 раз, вывод первых 20.
2. **Матрица случайных кортежей** — генератор кортежей длины n; матрица 20×20 из чисел [-5; 5].
3. **Таблица через zip** — строка слов → таблица из 3 столбцов, остаток отбрасывается.

Дополнительно:
- **Medium**: GUI на PySide6 (QTabWidget, 4 вкладки), тесты pytest.
- **Well-done**: параллельная версия генерации матрицы (ThreadPoolExecutor и ProcessPoolExecutor), замер через time.perf_counter(), вывод ускорения.

## Запуск
pip install -r requirements.txt
python LAB_4_lis.py
python -m pytest -v


## Краткая справка
- Генераторы: yield, ограничение через счётчик
- zip + срезы words[::3], words[1::3], words[2::3] — группировка по 3
- Параллелизм: concurrent.futures; ProcessPoolExecutor даёт реальное ускорение (в отличие от потоков, ограниченных GIL)
- Исключения: EmptyInputError, InvalidRangeError, InvalidLengthError, InvalidWorkerCountError
