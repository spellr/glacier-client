from typing import cast

from PyQt5.QtCore import QModelIndex

from task_manager import TaskManager
from tasks.list_vaults import ListVaultsTask

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTreeView, QMainWindow, QAction, QMenu

from consts import REGIONS


class _RegionTree(object):
    def __init__(self):
        self.view = None
        self.model = None

    def initialize(self, window: QMainWindow):
        self.view: QTreeView = cast(QTreeView, window.findChild(QTreeView, 'treeView'))

        self.view.customContextMenuRequested.connect(self.open_menu)

        self.model = QStandardItemModel()
        root: QStandardItem = self.model.invisibleRootItem()
        self.view.setModel(self.model)

        for region in REGIONS:
            item = QStandardItem(region.name)
            root.appendRow(item)
            TaskManager.add_task(ListVaultsTask(region, self))

    def open_menu(self, position):
        level = 0

        indexes = self.view.selectedIndexes()
        if len(indexes) > 0:
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1

        menu = QMenu()
        if level == 0:
            get_all_inventories_action = QAction("Request last inventory for all vaults", self.view)
            get_all_inventories_action.triggered.connect(self.get_inventory_action)
            menu.addAction(get_all_inventories_action)
        else:
            get_inventory_action = QAction("Request last inventory", self.view)
            get_inventory_action.triggered.connect(self.get_inventory_action)
            menu.addAction(get_inventory_action)

        menu.exec(self.view.viewport().mapToGlobal(position))

    def add_vault(self, region, vault_name):
        root: QModelIndex = self.view.rootIndex()
        child_count = self.model.rowCount(root)
        parent = QModelIndex()

        for i in range(child_count):
            row = self.model.index(i, 0, parent)
            cur_region = row.data()
            if region.name == cur_region:
                break
        else:
            raise ValueError(f"Failed to find region {region}")

        item = QStandardItem(vault_name)
        self.model.itemFromIndex(row).appendRow(item)

        self.view.expandAll()

        # Refresh model to see new rows
        self.model.rowsInserted.emit(parent, 0, child_count)

    def get_inventory_action(self):
        print(self.view.selectedIndexes()[0].data())


RegionTree = _RegionTree()
