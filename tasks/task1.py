from exceptions import EmptyInputError

# ===== НАСТРОЙКИ =====
DEFAULT_CITIES = ["Москва", "Ульяновск", "Самара", "Уфа", "Омск", "Тула"]
DEFAULT_TOTAL = 1_000_000   # сколько названий выдаёт генератор
DEFAULT_FIRST_N = 20        # сколько выводим на экран
# =====================


def city_generator(cities=None, total=None):
    """Генератор: циклически выдаёт города, ограничение total."""
    if cities is None:
        cities = DEFAULT_CITIES
    if total is None:
        total = DEFAULT_TOTAL

    if not cities:
        raise EmptyInputError("Список городов пуст.")
    if total <= 0:
        raise ValueError("total должно быть > 0")

    i = 0
    for _ in range(total):
        yield cities[i]
        i = (i + 1) % len(cities)


def first_n(cities=None, n=None):
    if cities is None:
        cities = DEFAULT_CITIES
    if n is None:
        n = DEFAULT_FIRST_N
    return list(city_generator(cities, total=n))
