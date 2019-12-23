import logging
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

from region_tree import RegionTree

logging.basicConfig(level=logging.INFO)

Form, Window = uic.loadUiType("mainwindow.ui")
app = QApplication([])

window: QMainWindow = Window()

form = Form()
form.setupUi(window)

RegionTree.initialize(window)

window.show()
app.exec_()
