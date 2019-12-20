import _vcg_tools as vcg_s
import torch

class MontecarloSampling(object):
	def __init__(self, num, remove_faces=True):
		self.num = num
		self.remove_faces = remove_faces

	def __call__(self, data):
		out = torch.zeros((self.num, 3), device=data.pos.device)
		data.pos = vcg_s.Montecarlo(data.pos, data.face, out, self.num)[:self.num]
		data.face = None if self.remove_faces else data.faces
		return data

	def __repr__(self):
		return '{}({})'.format(self.__class__.__name__, self.num)

