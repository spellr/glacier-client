from typing import cast, Optional

from PyQt5.QtCore import QMutex, QMutexLocker, Qt
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem


class _TasksTable(object):
    COLUMNS = 5

    def __init__(self):
        self.lock = QMutex()
        self.view: Optional[QTableWidget] = None

    def add_task(self, task, size):
        with QMutexLocker(self.lock):
            num_rows = self.view.rowCount()
            self.view.setRowCount(num_rows + 1)
            item = QTableWidgetItem(task)
            self.view.setItem(num_rows, 0, item)
            self.view.setItem(num_rows, 1, QTableWidgetItem(size))
            return item

    def update_task(self, item: QTableWidgetItem, task, size):
        with QMutexLocker(self.lock):
            row = self.view.row(item)
            size_item = self.view.item(row, 1)

            item.setText(task)
            size_item.setText(size)

            first = self.view.model().index(row, 0)
            last = self.view.model().index(row, self.COLUMNS)
            self.view.dataChanged(first, last, [])

    def remove_task(self, item):
        with QMutexLocker(self.lock):
            row = self.view.row(item)
            self.view.removeRow(row)

    def initialize(self, window: QMainWindow):
        self.view: QTableWidget = cast(QTableWidget, window.findChild(QTableWidget, 'tasksTable'))


TasksTable = _TasksTable()
