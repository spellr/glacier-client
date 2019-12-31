import logging
from typing import cast, Optional

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMainWindow, QPushButton

from regions import Region
from widgets import widgets_map
from task_manager import TaskManager
from tasks.download_archive import DownloadArchive


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
        print(region, vault)
        # TaskManager.add_task(DownloadArchive(region, vault, archive))

    def initialize(self, window: QMainWindow):
        self.button = cast(QPushButton, window.findChild(QPushButton, 'download_btn'))

        self.button.clicked.connect(self.on_click)


DownloadButton = _DownloadButton()
widgets_map['download_button'] = DownloadButton
