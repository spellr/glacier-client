from typing import cast

from PyQt5.QtCore import QMutex, QMutexLocker
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem


class _TasksTable(object):
    def __init__(self):
        self.lock = QMutex()
        self.view = None

    def add_task(self, task, size):
        with QMutexLocker(self.lock):
            num_rows = self.view.rowCount()
            self.view.setRowCount(num_rows + 1)
            item = QTableWidgetItem(task)
            self.view.setItem(num_rows, 0, item)
            self.view.setItem(num_rows, 1, QTableWidgetItem(size))
            return item

    def remove_task(self, item):
        with QMutexLocker(self.lock):
            row = self.view.row(item)
            self.view.removeRow(row)

    def initialize(self, window: QMainWindow):
        self.view: QTableWidget = cast(QTableWidget, window.findChild(QTableWidget, 'tasksTable'))


TasksTable = _TasksTable()
