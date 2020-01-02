import sys
import logging

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from widgets.region_tree import RegionTree
from widgets.tasks_table import TasksTable
from widgets.files_table import FilesTable
from widgets.download_button import DownloadButton
from widgets.access_keys_button import AccessKeysButton
import mock_aws


class AppContext(ApplicationContext):
    def run(self):
        mock_aws.setup_aws_mock()
        logging.basicConfig(level=logging.DEBUG)

        Form, Window = uic.loadUiType(self.get_resource("mainwindow.ui"))
        window: QMainWindow = Window()

        form = Form()
        form.setupUi(window)

        TasksTable.initialize(window)
        RegionTree.initialize(window)
        FilesTable.initialize(window)

        DownloadButton.initialize(window)
        AccessKeysButton.initialize(window)

        window.show()
        return appctxt.app.exec_()


if __name__ == '__main__':
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)
