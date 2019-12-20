import os
import off_parser as Off
import torch
from torch_geometric.data import Data
from Data.Data import Item

class Loader():
	_AcceptedExtension = ['.off', '.pt']
	def __init__(self):
		super().__init__()

	@staticmethod
	def load(path, type='auto'):
		if(type=='auto'):
			type = Loader._getTypeByPath(path)
		else:
			Loader._checkFileType(type)

		func_loader = Loader._loadTorch
		if(type == '.off'):
			func_loader = Loader._loadOff

		return func_loader(path)

	@staticmethod
	def _loadOff(path):
		off_obj = Off.OffParser(path)
		data = Data(
			pos=torch.Tensor(off_obj.points).double(),
			face=torch.Tensor(off_obj.faces).transpose(0, 1).long()
		)

		return Item(data= data, type= Item.TypeMesh, name= os.path.basename(path))

	@staticmethod
	def _loadTorch(path):
		tensor = torch.load(path)
		data = Data(
			pos=tensor.pos.float
		)

		return Item(data= data, type= Item.TypePointCloud, name= os.path.basename(path))

	@staticmethod
	def _getTypeByPath(path):
		filename, type = os.path.splitext(path)
		Loader._checkFileType(type)
		return type

	@staticmethod
	def _checkFileType(type):
		if (type not in Loader._AcceptedExtension):
			raise Exception('Invalid file type.')
