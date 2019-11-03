

class AppState():
	_shared_state = {
		'items': {},
		'current_item':None,
		'current_render':None,
		'progressive_item_index': 0,
		'current_change_listeneres': []
	}

	def __init__(self):
		self.__dict__ = self._shared_state

	def setCurrentItem(self, item, render=None):
		self.current_item = item
		self.current_render = render


	def newIndex(self):
		ret = self.progressive_item_index
		self.progressive_item_index +=1
		return ret


	def addItem(self, key, item):
		self.items[key] = item


	def addCurrentChangedListener(self, callable):
		self.current_change_listeneres.append(callable)


	def clearCurrentChangedListener(self):
		self.current_change_listeneres = []


	def _emitCurrentChangedListeneres(self):
		for listener in self.current_change_listeneres:
			listener(self.current_item, self.current_render)