from typing import cast, Optional, Sequence
from widgets.download_button import DownloadButton

from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem

from archive import Archive


class _FilesTable(object):
    def __init__(self):
        self.view: Optional[QTableWidget] = None

    def sizeof_fmt(self, num, suffix='B'):
        for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)

    def display_inventory(self, inventory: Sequence[Archive]):
        self.view.clearContents()
        self.view.setRowCount(len(inventory))

        for i, archive in enumerate(inventory):
            item = QTableWidgetItem(archive.description)
            self.view.setItem(i, 0, item)
            item = QTableWidgetItem(self.sizeof_fmt(archive.size))
            self.view.setItem(i, 1, item)
            item = QTableWidgetItem(archive.creation_date.strftime("%m/%d/%Y %H:%M:%S"))
            self.view.setItem(i, 2, item)

    def initialize(self, window: QMainWindow):
        self.view: QTableWidget = cast(QTableWidget, window.findChild(QTableWidget, 'filesTable'))
        self.view.itemSelectionChanged.connect(self.on_item_selection_changed)

    def on_item_selection_changed(self):
        is_selected_items = bool(self.view.selectedItems())
        DownloadButton.set_enabled(is_selected_items)


FilesTable = _FilesTable()
