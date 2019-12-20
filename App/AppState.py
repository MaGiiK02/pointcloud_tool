import PyQt5.Qt as Qt
#TODO Maybe apply a cole on set current!!!! o solo sulla modifica dei dati
class AppState():
	_shared_state = {
		'items': {},
		'current_item':None,
		'current_render':None,
		'progressive_item_index': 0,
		'current_change_listeners': [],
		'add_item_listeners': [],
		'error_message': None
	}

	def __init__(self):
		self.__dict__ = self._shared_state

	def setCurrentItem(self, key, render=None):
		self.current_item = self.items[key].clone()
		self.current_render = render
		self._emitCurrentChangedListeners()

	def setNewItem(self, item, render=None):
		self.current_item = item
		self.current_render = render
		self._emitCurrentChangedListeners()


	def newIndex(self):
		ret = self.progressive_item_index
		self.progressive_item_index +=1
		return ret

	def renameItemAt(self, key, name):
		item = self.items[key]
		if(item is None):
			return

		item.name = name

	def addItem(self, item, current=False):
		key = self.newIndex()
		self.items[key] = item
		self._emitaddAddItemListeners(key, item)

		if(current):
			self.current_item(key)


	def showError(self, str):
		if(self.error_message is None):
			return
		self.error_message.setStandardButtons(Qt.QMessageBox.Close)
		self.error_message.setIcon(Qt.QMessageBox.Critical)
		self.error_message.setText(str)
		self.error_message.show()

	def createErrorMessage(self, parent):
		self.error_message = Qt.QMessageBox(parent)

	def addCurrentChangedListener(self, callable):
		self.current_change_listeners.append(callable)


	def clearCurrentChangedListener(self):
		self.current_change_listeners = []


	def _emitCurrentChangedListeners(self):
		for listener in self.current_change_listeners:
			listener(self.current_item, self.current_render)

	def addAddItemListener(self, callable):
		self.add_item_listeners.append(callable)


	def clearAddItemListener(self):
		self.add_item_listeners = []


	def _emitaddAddItemListeners(self, key, item):
		for listener in self.add_item_listeners:
			listener(key, item)