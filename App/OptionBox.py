from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

class OptionBox(QWidget):
	def __init__(self, wList):
		super().__init__()
		self.layout = QVBoxLayout()
		self.layout.setAlignment(Qt.AlignTop)
		self.setLayout(self.layout)

		self.addAll(wList)

	def addAll(self, wList):
		for w in wList:
			self.layout.addWidget(w)