from App.AppState import AppState
from Normalization.Normalization import Normalize
import time

from PyQt5.QtWidgets import QSizePolicy, QWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt

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

		self.normalizer = Normalize()

		FigureCanvas.setSizePolicy(self,
		   QSizePolicy.Expanding,
		   QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)


		self.limit_x = self.limit_y = self.limit_z = [-1,1]
		self.current_plot = self.plot_figure.add_subplot(
			111,
			projection='3d',
			xlim=self.limit_x,
			ylim=self.limit_y,
			zlim=self.limit_z,
			xlabel='X',
			ylabel='Y',
			zlabel='Z'
		)
		self.current_plot.view_init(azim=30)

	def defaultPointCloudRender(self, item, ax):
		data = self.normalizer(item.data)
		pos = data.pos.transpose(0,1)

		ax.scatter(pos[0], pos[1], pos[2], c='r', marker='.')

		data.pos.transpose(0, 1)

		return ax

	def defaultMeshRender(self, item, ax):
		data = self.normalizer(item.data)
		points = data.pos.numpy()
		faces = data.face.transpose(0,1).numpy()

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

		return ax


	def updateRender(self, item, render):
		if(render is None):
			render = self.defaultMeshRender if item.type == 'Mesh' else self.defaultPointCloudRender

		if(item is None or item.data is None):
			return None

		self.current_plot.cla()
		self.current_plot.set_xlim(self.limit_x)
		self.current_plot.set_ylim(self.limit_y)
		self.current_plot.set_zlim(self.limit_z)

		render(item, self.current_plot)
		self.draw_idle()

	def reset(self):
		self.limit_x = self.limit_y = self.limit_z = [-1, 1]
		self.current_plot.set_xlim(self.limit_x)
		self.current_plot.set_ylim(self.limit_y)
		self.current_plot.set_zlim(self.limit_z)
		self.current_plot.view_init(azim=30)

		self.draw_idle()

