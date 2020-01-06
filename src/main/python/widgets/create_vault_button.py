import logging
from typing import cast, Optional

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMainWindow, QPushButton, QInputDialog

from regions import Region
from tasks.create_vault import CreateVaultTask
from widgets import widgets_map
from task_manager import TaskManager


class _CreateVaultButton(QObject):
    def __init__(self):
        super(_CreateVaultButton, self).__init__()
        self.button: Optional[QPushButton] = None

    def set_enabled(self, enabled: bool):
        self.button.setEnabled(enabled)

    def on_click(self):
        logging.info("Create vault clicked!")
        region: Region = widgets_map['region_tree'].get_selected_region()

        vault_name, ok = QInputDialog.getText(self.button, "New vault name", "Name for the new vault:")
        if not ok or not vault_name:
            return

        TaskManager.add_task(CreateVaultTask(region, vault_name))

    def initialize(self, window: QMainWindow):
        self.button = cast(QPushButton, window.findChild(QPushButton, 'create_vault_btn'))

        self.button.clicked.connect(self.on_click)


CreateVaultButton = _CreateVaultButton()
widgets_map['create_vault_button'] = CreateVaultButton
