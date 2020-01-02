import logging
from typing import cast, Optional

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMainWindow, QPushButton, QFileDialog

from archive import Archive
from regions import Region
from widgets import widgets_map
from task_manager import TaskManager
from tasks.get_archive import GetArchiveTask


class _DownloadButton(QObject):
    def __init__(self):
        super(_DownloadButton, self).__init__()
        self.button: Optional[QPushButton] = None

    def set_enabled(self, enabled: bool):
        self.button.setEnabled(enabled)

    def on_click(self):
        logging.info("Download clicked!")
        files_table = widgets_map['files_table']
        region: Region = files_table.displayed_region
        vault: str = files_table.displayed_vault
        archive: Archive = files_table.get_active_archive()

        output_file = QFileDialog.getSaveFileName(self.button, "Output file location", archive.description)[0]
        if not output_file:
            return

        TaskManager.add_task(GetArchiveTask(region, vault, archive, output_file))

    def initialize(self, window: QMainWindow):
        self.button = cast(QPushButton, window.findChild(QPushButton, 'download_btn'))

        self.button.clicked.connect(self.on_click)


DownloadButton = _DownloadButton()
widgets_map['download_button'] = DownloadButton
