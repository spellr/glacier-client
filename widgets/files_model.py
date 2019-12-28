import logging

from IPython.external.qt_for_kernel import QtCore
from PyQt5.QtCore import Qt, QModelIndex, QAbstractItemModel
from PyQt5.QtWidgets import QFileSystemModel

from archive import Archive


class _FilesModel(QAbstractItemModel):
    def __init__(self):
        super(_FilesModel, self).__init__()
        self.filesystem = {}

        import pickle
        self.filesystem = pickle.load(open(r'C:\Temp\asdf.pickle', 'rb'))

        self.root = object()

    def rowCount(self, parent: QtCore.QModelIndex = QModelIndex()) -> int:
        try:
            if not parent.isValid():
                return len(self.filesystem.keys())
            return 0
        except:
            logging.exception("qwer")

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0 if parent.column() > 0 else 4

    def set_file_system(self, filesystem):
        self.beginResetModel()
        self.filesystem = filesystem
        self.endResetModel()

    def index(self, row: int, column: int, parent: QtCore.QModelIndex = QModelIndex()) -> QtCore.QModelIndex:
        try:
            if row < 0 or column < 0 or row >= self.rowCount(parent) or column >= self.columnCount(parent):
                return QModelIndex()

            parent_node = {} if parent.isValid() else self.filesystem

            child_name = sorted(parent_node)[row]
            archive = parent_node[child_name]
            if isinstance(archive, dict):
                archive = archive['']

            return self.createIndex(row, column, archive)
        except:
            logging.exception("asdf")

    def data(self, index: QtCore.QModelIndex, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            col = index.column()
            if col == 0:
                return "asdf"
            return "asdf"


FilesModel = _FilesModel()
