import typing
import logging
from pathlib import PurePosixPath

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

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> typing.Any:
        if orientation != Qt.Horizontal or role != Qt.DisplayRole:
            super(_FilesModel, self).headerData(section, orientation, role)
        else:
            if section == 0:
                return "Name"
            elif section == 1:
                return "Size"
            elif section == 2:
                return "Creation Date"

    def rowCount(self, parent: QtCore.QModelIndex = QModelIndex()) -> int:
        if not parent.isValid():
            return len(self.filesystem.keys())
        return 0

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0 if parent.column() > 0 else 3

    def set_file_system(self, filesystem):
        self.beginResetModel()
        self.filesystem = filesystem
        self.endResetModel()

    def index(self, row: int, column: int, parent: QtCore.QModelIndex = QModelIndex()) -> QtCore.QModelIndex:
        if row < 0 or column < 0 or row >= self.rowCount(parent) or column >= self.columnCount(parent):
            return QModelIndex()

        parent_node = {} if parent.isValid() else self.filesystem

        child_name = sorted(parent_node)[row]
        archive = parent_node[child_name]
        if isinstance(archive, dict):
            archive = archive['']

        return self.createIndex(row, column, archive)

    def data(self, index: QtCore.QModelIndex, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            archive: Archive = index.internalPointer()
            col = index.column()
            if col == 0:
                return PurePosixPath(archive.path).name
            elif col == 1:
                if archive.is_dir:
                    return ""
                else:
                    return archive.size
            elif col == 2:
                return archive.creation_date.strftime("%m/%d/%Y %H:%M:%S")


FilesModel = _FilesModel()
