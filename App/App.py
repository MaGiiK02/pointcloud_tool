from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtCore import Qt
import torch
from torch_geometric.data import Data
from Data.Data import Item
from App.AppState import AppState
from App.ItemList import ItemList
from App.Plotter import Plotter
from App.OperationsPanel import OperationsPanel
from matplotlib.backends.backend_qt5agg import (
	FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

class App(QWidget):
	def __init__(self, AppName = 'App', Size=(1024,786)):
		super().__init__()

		self.app_state = AppState()
		self.app_state.createErrorMessage(self)

		self.title = AppName
		self.left = 10
		self.top = 10
		self.width = Size[0]
		self.height = Size[1]
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		grid = QGridLayout()
		self.setLayout(grid)

		self.item_list = ItemList()
		grid.addWidget(self.item_list,
					   0, 0, #position row column
					   10, 2) #span row column

		self.plotter = Plotter()
		grid.addWidget(self.plotter,
					   0, 2, #position row column
					   10, 7) #span row column


		self.operations = OperationsPanel()
		grid.addWidget(self.operations,
					   0, 9,  # position row column
					   10, 1)  # span row column

		self.show()





