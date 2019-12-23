from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

from region_tree import RegionTree

Form, Window = uic.loadUiType("mainwindow.ui")
app = QApplication([])

window: QMainWindow = Window()

form = Form()
form.setupUi(window)

RegionTree(window)

window.show()
app.exec_()
