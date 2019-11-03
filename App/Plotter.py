from App.AppState import AppState
from Normalization.Normalization import Normalize

from torch_geometric.data import Data
import torch

from PyQt5.QtWidgets import QSizePolicy

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.backends.backend_qt5agg import (
	FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

import numpy as np

class Plotter(FigureCanvas):
	def __init__(self, parent=None, width=8, height=1, dpi=100):
		self.app_status = AppState()
		self.render = self.app_status.current_render
		self.app_status.addCurrentChangedListener(self.updateRender)
		self.plot_figure = Figure(figsize=(width, height), dpi=dpi)
		FigureCanvas.__init__(self, self.plot_figure)
		self.setParent(parent)

		FigureCanvas.setSizePolicy(self,
		   QSizePolicy.Expanding,
		   QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

		self.debugDraw()

		self.draw()

	def debugDraw(self):
		data = Data(pos=torch.rand(100, 3))
		n = Normalize()
		data = n(data)
		pos = data.pos.transpose(0,1)

		axp = self.plot_figure.add_subplot(111,
							  projection='3d',
							  xlabel='X',
							  ylabel='Y',
							  zlabel='Z',
							  xlim=[-1.5, 1.5],
							  ylim=[-1.5, 1.5],
							  zlim=[-1.5, 1.5]
							  )
		axp.scatter(pos[0], pos[1], pos[2], c='r', marker='o')

	def getToolbar(self, parent):
		return NavigationToolbar(self.plot_figure, parent)


	def defaultPointCloudRender(self, item, fig):
		data = Normalize(item.data)
		pos = data.pos

		axp = fig.add_subplot(111,
			projection='3d',
			xlabel='X',
			ylabel='Y',
			zlabel='Z',
			xlim=[-1.5, 1.5],
			ylim=[-1.5, 1.5],
			zlim=[-1.5, 1.5]
			)
		axp.scatter(pos[0], pos[1], pos[2], c='r', marker='o')

	def defaultMeshRender(self, item, fig):
		data = Normalize(item.data)
		points = data.pos
		faces = data.faces

		mx = points.max(axis=0)
		c = 0.5 * (mx + points.min(axis=0))
		r = 1.1 * np.max(mx - c)
		xlim, ylim, zlim = np.column_stack([c - r, c + r])
		ax = fig.add_subplot(111,
			   projection='3d',
			   xlim=xlim,
			   ylim=ylim,
			   zlim=zlim,
			   xlabel='X',
			   ylabel='Y',
			   zlabel='Z'
		)

		sym = dict(
			points=None,
			faces='g',
			edges='#006400'
		)

		if sym['points'] is not None:
			x = points
			ax.plot(x[:, 0], x[:, 1], x[:, 2], sym['points'])

		if sym['faces'] is not None:
			if sym['edges'] is None:
				sym['edges'] = sym['faces']

			v = [points[f] for f in faces]
			poly = Poly3DCollection(v, edgecolor=sym['edges'], facecolor=sym['faces'])
			ax.add_collection(poly)


	def updateRender(self, item, render):
		if(render is None):
			render = self.defaultMeshRender() if item.type == 'Mesh' else self.defaultPointCloudRender()

		self.plot_figure.clear()
		if(item.data is None):
			return
		render(item, self.plot_figure)
		self.draw()


