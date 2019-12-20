from PyQt5.Qt import Qt, QWidget, QTreeView, QPushButton, QGridLayout, QFileDialog, QStandardItem, QStandardItemModel
from App.AppState import AppState
from Data.Loader import Loader
import os

class ItemList(QWidget):

	_ITEM_NAME, _OPERATIONS = range(2)


	def __init__(self):
		super().__init__()

		self.app_state = AppState()
		self.app_state.addAddItemListener(self._addItemListener)

		self.model = QStandardItemModel()
		self.model.setHeaderData(self._ITEM_NAME, Qt.Horizontal, "Name")
		self.model.setHeaderData(self._OPERATIONS, Qt.Horizontal, "Operations")
		self.model.itemChanged.connect(self._renameListener)
		self.initUI()


	def initUI(self):
		grid = QGridLayout()
		self.setLayout(grid)

		self.tree_view = QTreeView()
		self.tree_view.setModel(self.model)
		self.tree_view.clicked.connect(self._selectedItemListener)

		grid.addWidget(self.tree_view, 0, 0, 19, 1)

		self.load_data_button = QPushButton('Load Data')
		self.load_data_button.clicked.connect(self._loadDatauttonListener)
		grid.addWidget(self.load_data_button, 20, 0, 1, 1)

	#Private
	def _getItemKey(self, item):
		return self.model.itemData(item)[257]


	#Event Handlers
	def _selectedItemListener(self, event):
		key = self._getItemKey(self.tree_view.currentIndex())
		self.app_state.setCurrentItem(key)


	def _loadDatauttonListener(self):
		file_path, file_types = QFileDialog.getOpenFileName(self,
			'Open file', os.path.expanduser("~"))
		if(len(file_path) <= 0 ):
			return

		item_data = Loader.load(file_path)
		self.app_state.addItem(item_data)

	#Called when a new item is added to the AppState
	def _addItemListener(self, key, item_data):
		item = QStandardItem(item_data.name)
		item.setData(key)  # Set my custom index as a payload
		item.setSelectable(True)
		item.setEditable(True)
		self.model.appendRow(item)

	def _renameListener(self, item):
		key = item.data()
		self.app_state.renameItemAt(key, item.text())


