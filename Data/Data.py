
class Item():
	TypePointCloud = 'PointCloud'
	TypeMesh = 'Mesh'

	def __init__(self, name, type, data):
		self.type = type
		self.data = data
		self.name = name

	def clone(self):
		return Item(
			name= self.name,
			data= self.data.clone(),
			type= self.type
		)