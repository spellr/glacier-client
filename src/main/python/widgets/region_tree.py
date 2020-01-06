from typing import cast

from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTreeView, QMainWindow, QAction, QMenu

import keys
import regions
from widgets import widgets_map
from inventory_manager import Inventories
from regions import REGIONS
from task_manager import TaskManager
from tasks.get_inventory import GetInventoryTask
from tasks.list_vaults import ListVaultsTask
from widgets.files_table import FilesTable


class _RegionTree(object):
    def __init__(self):
        self.view = None
        self.model = None

    def on_clicked_region(self):
        widgets_map['create_vault_button'].set_enabled(True)

    def on_clicked_vault(self):
        region = self.get_selected_region()
        vault = self.get_selected_vault()
        inventory = Inventories.get_inventory(region, vault)
        FilesTable.display_inventory(region, vault, inventory)

    def on_clicked(self, index: QModelIndex):
        widgets_map['create_vault_button'].set_enabled(False)

        if index.parent().isValid():
            self.on_clicked_vault()
        else:
            self.on_clicked_region()

    def get_selected_region(self):
        index = self.view.selectedIndexes()[0]

        if index.parent().isValid():
            region_name = index.parent().data()
        else:
            region_name = index.data()

        return regions.get_by_name(region_name)

    def get_selected_vault(self):
        index = self.view.selectedIndexes()[0]
        if not index.parent().isValid():
            return None
        return index.data()

    def initialize(self, window: QMainWindow):
        self.view: QTreeView = cast(QTreeView, window.findChild(QTreeView, 'treeView'))

        self.view.clicked.connect(self.on_clicked)
        self.view.customContextMenuRequested.connect(self.open_menu)

        self.model = QStandardItemModel()
        root: QStandardItem = self.model.invisibleRootItem()
        self.view.setModel(self.model)

        for region in REGIONS:
            item = QStandardItem(region.name)
            root.appendRow(item)
            if keys.Keys.has_keys():
                TaskManager.add_task(ListVaultsTask(region))

    def open_menu(self, position):
        level = 0

        indexes = self.view.selectedIndexes()
        if len(indexes) > 0:
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1

        menu = QMenu()
        if level == 1:
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
        vault_name = self.view.selectedIndexes()[0].data()
        region = self.get_selected_region()

        TaskManager.add_task(GetInventoryTask(region, vault_name))


RegionTree = _RegionTree()
widgets_map['region_tree'] = RegionTree
