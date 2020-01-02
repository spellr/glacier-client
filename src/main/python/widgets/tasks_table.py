import uuid
from typing import cast, Optional

from PyQt5.QtCore import QMutex, QMutexLocker, Qt, pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QProgressBar


class _TasksTable(QObject):
    COLUMNS = 5
    new_task = pyqtSignal(str, str, str, name='new_task')
    task_finished = pyqtSignal(str, name='task_finished')

    def __init__(self):
        super(_TasksTable, self).__init__()
        self.lock = QMutex()
        self.view: Optional[QTableWidget] = None
        self.task_handles = {}

    def on_new_task(self, task, size, handle):
        with QMutexLocker(self.lock):
            num_rows = self.view.rowCount()
            self.view.setRowCount(num_rows + 1)
            item = QTableWidgetItem(task)
            self.view.setItem(num_rows, 0, item)
            self.view.setItem(num_rows, 1, QTableWidgetItem(size))
            q = QProgressBar(self.view)
            q.setRange(0, 0)
            self.view.setCellWidget(num_rows, 2, q)
            self.task_handles[handle] = item

    def add_task(self, task, size):
        # Give back a handle to the item - to be used to update/remove item
        handle = str(uuid.uuid4())
        self.new_task.emit(task, size, handle)
        return handle

    def update_task(self, handle: str, task, size):
        with QMutexLocker(self.lock):
            item = self.task_handles[handle]
            row = self.view.row(item)
            size_item = self.view.item(row, 1)

            item.setText(task)
            size_item.setText(size)

            first = self.view.model().index(row, 0)
            last = self.view.model().index(row, self.COLUMNS)
            self.view.dataChanged(first, last, [])

    def on_task_finished(self, handle):
        with QMutexLocker(self.lock):
            item = self.task_handles[handle]
            row = self.view.row(item)
            self.view.removeCellWidget(row, 2)
            self.view.removeRow(row)

    def remove_task(self, handle):
        self.task_finished.emit(handle)

    def initialize(self, window: QMainWindow):
        self.view = cast(QTableWidget, window.findChild(QTableWidget, 'tasksTable'))

        self.new_task.connect(self.on_new_task)
        self.task_finished.connect(self.on_task_finished)


TasksTable = _TasksTable()
