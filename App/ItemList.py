from PyQt5.QtWidgets import QWidget, QTreeView, QPushButton, QGridLayout
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt
from App.AppState import AppState

class ItemList(QWidget):

	_ITEM_NAME, _OPERATIONS = range(2)


	def __init__(self):
		super().__init__()

		self.app_state = AppState()

		self.model = QStandardItemModel()
		self.model.setHeaderData(self._ITEM_NAME, Qt.Horizontal, "Name")
		self.model.setHeaderData(self._OPERATIONS, Qt.Horizontal, "Operations")
		self.initUI()


	def initUI(self):
		grid = QGridLayout()
		self.setLayout(grid)

		self.tree_view = QTreeView()
		self.tree_view.setModel(self.model)

		grid.addWidget(self.tree_view, 0, 0, 19, 1)

		self.load_data_button = QPushButton('Load Data')
		self.load_data_button.clicked.connect(self._loadDatauttonListener)
		grid.addWidget(self.load_data_button, 20, 0, 1, 1)


	#Event Handlers
	def _selectedItemListener(self, event):
		selection = self.tree_view.selectedIndexes()[0]
		print(selection)


	def _loadDatauttonListener(self):
		#TODO!!!!!!! Load the real mesh!!! or Pytorch Data!!!
		data_obj = []
		obj_index = self.app_state.newIndex()
		self.app_state.addItem('{}'.format(obj_index), data_obj)

		item = QStandardItem("NewItem name")
		item.setData(obj_index) #Set my custom index as a payload
		item.setSelectable(True)
		item.setEditable(True)
		self.model.appendRow(item)

