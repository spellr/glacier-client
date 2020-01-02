import logging
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

from widgets.region_tree import RegionTree
from widgets.tasks_table import TasksTable
from widgets.files_table import FilesTable
from widgets.download_button import DownloadButton
from widgets.access_keys_button import AccessKeysButton
import mock_aws

mock_aws.setup_aws_mock()

logging.basicConfig(level=logging.DEBUG)

Form, Window = uic.loadUiType("mainwindow.ui")
app = QApplication([])

window: QMainWindow = Window()

form = Form()
form.setupUi(window)

TasksTable.initialize(window)
RegionTree.initialize(window)
FilesTable.initialize(window)

DownloadButton.initialize(window)
AccessKeysButton.initialize(window)

window.show()
app.exec_()
