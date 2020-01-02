import logging
from typing import Optional, cast

from PyQt5 import uic
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import QCloseEvent, QHideEvent
from PyQt5.QtWidgets import QPushButton, QMainWindow, QDialog

from widgets import widgets_map

access_keys_dialog = uic.loadUiType("keys_dialog.ui")[0]


class AccessKeysDialog(QDialog, access_keys_dialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setupUi(self)


class _AccessKeysButton(QObject):
    def __init__(self):
        super(_AccessKeysButton, self).__init__()
        self.button: Optional[QPushButton] = None

    def on_click(self):
        logging.info("Access keys button clicked!")
        dialog = AccessKeysDialog()
        dialog.exec()

    def initialize(self, window: QMainWindow):
        self.button = cast(QPushButton, window.findChild(QPushButton, 'access_keys_button'))

        self.button.clicked.connect(self.on_click)


AccessKeysButton = _AccessKeysButton()
widgets_map['access_keys_button'] = AccessKeysButton
