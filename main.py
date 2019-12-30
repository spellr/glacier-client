import logging
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

from widgets.region_tree import RegionTree
from widgets.tasks_table import TasksTable
from widgets.files_table import FilesTable
from task_manager import TaskManager

logging.basicConfig(level=logging.DEBUG)

Form, Window = uic.loadUiType("mainwindow.ui")
app = QApplication([])

window: QMainWindow = Window()

form = Form()
form.setupUi(window)

TasksTable.initialize(window)
RegionTree.initialize(window)
FilesTable.initialize(window)

window.show()
app.exec_()
