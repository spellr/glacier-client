import logging
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

from widgets.region_tree import RegionTree
from widgets.tasks_table import TasksTable
from task_manager import TaskManager

logging.basicConfig(level=logging.INFO)

Form, Window = uic.loadUiType("mainwindow.ui")
app = QApplication([])

window: QMainWindow = Window()

form = Form()
form.setupUi(window)

TasksTable.initialize(window)
RegionTree.initialize(window)

TaskManager.start()

window.show()
app.exec_()
