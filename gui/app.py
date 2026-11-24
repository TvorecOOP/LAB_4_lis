import sys

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget,
    QVBoxLayout, QPushButton, QTextEdit, QLabel, QLineEdit,
)

from tasks.task1 import first_n, DEFAULT_CITIES
from tasks.task2 import build_matrix, format_matrix
from tasks.task3 import words_to_table, format_table
from tasks.task2_parallel import benchmark, format_benchmark
from exceptions import LabError


class BenchmarkWorker(QThread):
    """Выполняет тяжёлый бенчмарк в отдельном потоке, чтобы GUI не зависал."""
    finished_ok = Signal(str)
    failed = Signal(str)

    def run(self):
        try:
            results = benchmark()
            self.finished_ok.emit(format_benchmark(results))
        except Exception as e:
            self.failed.emit(f"Ошибка: {e}")


class Task1Tab(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)
        self.btn = QPushButton("Показать первые 20 городов")
        self.out = QTextEdit(readOnly=True)
        self.btn.clicked.connect(self.run)
        lay.addWidget(self.btn)
        lay.addWidget(self.out)

    def run(self):
        try:
            self.out.setPlainText("\n".join(first_n(DEFAULT_CITIES, 20)))
        except LabError as e:
            self.out.setPlainText(f"Ошибка: {e}")


class Task2Tab(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)
        self.btn = QPushButton("Сгенерировать матрицу 20x20 [-5; 5]")
        self.out = QTextEdit(readOnly=True)
        self.btn.clicked.connect(self.run)
        lay.addWidget(self.btn)
        lay.addWidget(self.out)

    def run(self):
        try:
            self.out.setPlainText(format_matrix(build_matrix()))
        except LabError as e:
            self.out.setPlainText(f"Ошибка: {e}")


class Task3Tab(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("Слова через пробел:"))
        self.input = QLineEdit("один два три четыре пять шесть семь восемь")
        self.btn = QPushButton("Построить таблицу (3 столбца)")
        self.out = QTextEdit(readOnly=True)
        self.btn.clicked.connect(self.run)
        lay.addWidget(self.input)
        lay.addWidget(self.btn)
        lay.addWidget(self.out)

    def run(self):
        try:
            self.out.setPlainText(format_table(words_to_table(self.input.text())))
        except LabError as e:
            self.out.setPlainText(f"Ошибка: {e}")


class PerfTab(QWidget):
    def __init__(self):
        super().__init__()
        self._worker = None

        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("Бенчмарк (тяжёлый, выполняется в фоне)"))
        self.btn = QPushButton("Запустить бенчмарк")
        self.out = QTextEdit(readOnly=True)
        self.btn.clicked.connect(self.run)
        lay.addWidget(self.btn)
        lay.addWidget(self.out)

    def run(self):
        if self._worker is not None and self._worker.isRunning():
            return

        self.btn.setEnabled(False)
        self.out.setPlainText("Идёт расчёт...")

        self._worker = BenchmarkWorker()
        self._worker.finished_ok.connect(self._on_done)
        self._worker.failed.connect(self._on_fail)
        self._worker.start()

    def _on_done(self, text):
        self.out.setPlainText(text)
        self.btn.setEnabled(True)

    def _on_fail(self, text):
        self.out.setPlainText(text)
        self.btn.setEnabled(True)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная №4 - Вариант 15 (Rare + Medium + Well-done)")
        self.resize(760, 640)
        tabs = QTabWidget()
        tabs.addTab(Task1Tab(), "1: города")
        tabs.addTab(Task2Tab(), "2: матрица")
        tabs.addTab(Task3Tab(), "3: zip")
        tabs.addTab(PerfTab(), "Well-done: perf")
        self.setCentralWidget(tabs)


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.showMaximized()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
