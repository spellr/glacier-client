import logging
from typing import cast, Optional

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMainWindow, QPushButton


class _DownloadButton(QObject):
    def __init__(self):
        super(_DownloadButton, self).__init__()
        self.button: Optional[QPushButton] = None

    def set_enabled(self, enabled: bool):
        self.button.setEnabled(enabled)

    def on_click(self):
        logging.info("Download clicked!")

    def initialize(self, window: QMainWindow):
        self.button = cast(QPushButton, window.findChild(QPushButton, 'download_btn'))

        self.button.clicked.connect(self.on_click)


DownloadButton = _DownloadButton()
