from exceptions import EmptyInputError

# ===== НАСТРОЙКИ =====
COLUMNS = 3                       # число столбцов таблицы
DEFAULT_TEXT = "один два три четыре пять шесть семь восемь"  # пример строки
# =====================


def words_to_table(text=None):
    if text is None:
        text = DEFAULT_TEXT
    words = text.split()
    if not words:
        raise EmptyInputError("Строка не содержит слов.")
    return list(zip(*[words[i::COLUMNS] for i in range(COLUMNS)]))


def format_table(table):
    return "\n".join(" ".join(row) for row in table)
