from typing import cast, Optional, Sequence, Dict

from regions import Region
from widgets import widgets_map
from widgets.download_button import DownloadButton

from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem

from archive import Archive


class _FilesTable(object):
    def __init__(self):
        self.view: Optional[QTableWidget] = None

        self.displayed_region: Optional[Region] = None
        self.displayed_vault: Optional[str] = None

        # Map between row and the archive
        self.archive_map: Dict[int, Archive] = {}

    def sizeof_fmt(self, num, suffix='B'):
        for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)

    def display_inventory(self, region: Region, vault: str, inventory: Sequence[Archive]):
        self.displayed_region = region
        self.displayed_vault = vault

        self.view.clearContents()
        self.archive_map.clear()

        self.view.setRowCount(len(inventory))

        for i, archive in enumerate(inventory):
            self.archive_map[i] = archive
            item = QTableWidgetItem(archive.description)
            self.view.setItem(i, 0, item)
            item = QTableWidgetItem(self.sizeof_fmt(archive.size))
            self.view.setItem(i, 1, item)
            item = QTableWidgetItem(archive.creation_date.strftime("%m/%d/%Y %H:%M:%S"))
            self.view.setItem(i, 2, item)

    def get_active_archive(self):
        row = self.view.selectedItems()[0].row()
        return self.archive_map[row]

    def initialize(self, window: QMainWindow):
        self.view: QTableWidget = cast(QTableWidget, window.findChild(QTableWidget, 'filesTable'))
        self.view.itemSelectionChanged.connect(self.on_item_selection_changed)

    def on_item_selection_changed(self):
        is_selected_items = bool(self.view.selectedItems())
        DownloadButton.set_enabled(is_selected_items)


FilesTable = _FilesTable()
widgets_map['files_table'] = FilesTable
