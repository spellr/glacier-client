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
        self.cur_dir = self.filesystem

        self.root = object()

    def file_name(self, index: QModelIndex):
        archive: Archive = index.internalPointer()
        return PurePosixPath(archive.path).name

    def row_clicked(self, index: QModelIndex):
        archive: Archive = index.internalPointer()
        if not archive.is_dir:
            return

        file_name = PurePosixPath(archive.path).name

        self.beginResetModel()
        self.cur_dir = self.cur_dir[file_name]
        self.endResetModel()

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
            if '' in self.cur_dir:
                return len(self.cur_dir.keys()) - 1
            else:
                return len(self.cur_dir.keys())

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0 if parent.column() > 0 else 3

    def set_file_system(self, filesystem):
        self.beginResetModel()
        self.filesystem = filesystem
        self.cur_dir = self.filesystem
        self.endResetModel()

    def index(self, row: int, column: int, parent: QtCore.QModelIndex = QModelIndex()) -> QtCore.QModelIndex:
        if row < 0 or column < 0 or row >= self.rowCount(parent) or column >= self.columnCount(parent):
            return QModelIndex()

        child_name = sorted(self.cur_dir)[row]
        if child_name == '':
            child_name = sorted(self.cur_dir)[row + 1]
        archive = self.cur_dir[child_name]
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
