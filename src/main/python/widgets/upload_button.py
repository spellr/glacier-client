import logging
from typing import cast, Optional

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMainWindow, QPushButton, QFileDialog

from archive import Archive
from regions import Region
from tasks.upload_file import UploadFileTask
from widgets import widgets_map
from task_manager import TaskManager
from tasks.get_archive import GetArchiveTask


class _UploadButton(QObject):
    def __init__(self):
        super(_UploadButton, self).__init__()
        self.button: Optional[QPushButton] = None

    def set_enabled(self, enabled: bool):
        self.button.setEnabled(enabled)

    def on_click(self):
        logging.info("Upload clicked!")
        files_table = widgets_map['files_table']
        region: Region = files_table.displayed_region
        vault: str = files_table.displayed_vault

        file_location = QFileDialog.getOpenFileName(self.button, "Select file to upload")[0]
        if not file_location:
            return

        TaskManager.add_task(UploadFileTask(region, vault, file_location))

    def initialize(self, window: QMainWindow):
        self.button = cast(QPushButton, window.findChild(QPushButton, 'upload_btn'))

        self.button.clicked.connect(self.on_click)


UploadButton = _UploadButton()
widgets_map['upload_button'] = UploadButton
