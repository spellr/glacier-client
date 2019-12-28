from typing import cast, Optional

from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableView

from widgets.files_model import FilesModel


class _FilesTable(object):
    def __init__(self):
        self.model = FilesModel
        self.view: Optional[QTableWidget] = None

    def initialize(self, window: QMainWindow):
        self.view: QTableView = cast(QTableView, window.findChild(QTableView, 'filesTable'))

        self.view.setModel(self.model)


FilesTable = _FilesTable()
