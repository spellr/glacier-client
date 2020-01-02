import logging
from typing import Optional, cast

import botocore.exceptions, botocore.client
from PyQt5 import uic
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QPushButton, QMainWindow, QDialog, QLineEdit, QMessageBox, QCheckBox

from keys import Keys
from regions import REGIONS
from boto import get_boto
from task_manager import TaskManager
from tasks.list_vaults import ListVaultsTask
from widgets import widgets_map

access_keys_dialog = uic.loadUiType("keys_dialog.ui")[0]


class AccessKeysDialog(QDialog, access_keys_dialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setupUi(self)

        self.access_key_input: QLineEdit = cast(QLineEdit, self.findChild(QLineEdit, "access_input"))
        self.secret_key_input: QLineEdit = cast(QLineEdit, self.findChild(QLineEdit, "secret_input"))
        self.save_creds_checkbox: QCheckBox = cast(QCheckBox, self.findChild(QCheckBox, "save_creds_checkbox"))

    def accept(self) -> None:
        access_key = self.access_key_input.text()
        secret_key = self.secret_key_input.text()

        if not access_key or not secret_key:
            return self._invalid_access_keys_msg_box("Please fill both access key and secret key")

        boto = get_boto(REGIONS[0], access_key=access_key, secret_key=secret_key)
        try:
            boto.list_vaults()
        except botocore.exceptions.ClientError:
            return self._invalid_access_keys_msg_box("Keys are invalid. Please validate the access keys, and retry")

        Keys.ACCESS_KEY = access_key
        Keys.SECRET_KEY = secret_key

        if self.save_creds_checkbox.isChecked():
            Keys.dump_to_file()

        for region in REGIONS:
            if Keys.has_keys():
                TaskManager.add_task(ListVaultsTask(region))

        super(AccessKeysDialog, self).accept()

    def _invalid_access_keys_msg_box(self, msg) -> None:
        QMessageBox.warning(self, "Invalid access keys", msg, QMessageBox.Ok)


class _AccessKeysButton(QObject):
    def __init__(self):
        super(_AccessKeysButton, self).__init__()
        self.button: Optional[QPushButton] = None
        self.orig_palette: Optional[QPalette] = None

    def on_click(self):
        logging.info("Access keys button clicked!")
        dialog = AccessKeysDialog()
        res = dialog.exec()
        if res == QDialog.Accepted:
            self.unhighlight()

    def initialize(self, window: QMainWindow):
        self.button = cast(QPushButton, window.findChild(QPushButton, 'access_keys_button'))
        self.button.clicked.connect(self.on_click)

        self.orig_palette: Optional[QPalette] = self.button.palette()

        if not Keys.has_keys():
            self.highlight()

    def unhighlight(self):
        self.button.setPalette(self.orig_palette)

    def highlight(self):
        palette: QPalette = QPalette(self.orig_palette)
        palette.setColor(QPalette.Button, Qt.red)
        palette.setColor(QPalette.ButtonText, Qt.red)
        self.button.setPalette(palette)


AccessKeysButton = _AccessKeysButton()
widgets_map['access_keys_button'] = AccessKeysButton
