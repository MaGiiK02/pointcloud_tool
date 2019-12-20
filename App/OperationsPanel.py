from PyQt5.Qt import QPushButton, QLineEdit, QScrollArea, QToolBox, QIntValidator , QDoubleValidator
from App.OptionBox import OptionBox
from App.AppState import AppState
from torch_geometric.data import Data
from Data.Data import Item

from torch_geometric.nn import fps as FPS
from torch_geometric.transforms import SamplePoints
from Sampling.PoissonDiskSampling import PoissonDiskSampling
from Sampling.MonecarloSampling import MontecarloSampling

from App.RenderPipeline.CenterAndRadiousRender import CenterAndRadious

import torch

class OperationsPanel(QScrollArea):
	def __init__(self):
		super().__init__()

		self.app_state = AppState()
		self.setWidgetResizable(True)
		self.initUI()


	def initUI(self):
		self.container = QToolBox()
		self.setWidget(self.container)
		
		self.b_save_edit = QPushButton("Save current edit")
		self.b_save_edit.clicked.connect(self._applySaveEdit)
		self.container.addItem(OptionBox([
			self.b_save_edit
		]),  "Save")

		self.tf_importance_point_count = QLineEdit()
		self.tf_importance_point_count.setPlaceholderText("Number of Points to Sample")
		self.tf_importance_point_count.setValidator(QIntValidator(1, 1000000, self))
		self.b_importance_apply = QPushButton("Apply Sampling")
		self.b_importance_apply.clicked.connect(self._applyFaceImportanceSampling)
		self.container.addItem(OptionBox([
			self.tf_importance_point_count,
			self.b_importance_apply
		]), "Importance Sampling (Mesh)")

		self.tf_poisson_point_count = QLineEdit()
		self.tf_poisson_point_count.setPlaceholderText("Number of Points to Sample")
		self.tf_poisson_point_count.setValidator(QIntValidator(1, 1000000, self))
		self.tf_poisson_radius = QLineEdit()
		self.tf_poisson_radius.setPlaceholderText("Radius of the poisson disks")
		self.tf_poisson_radius.setValidator(QDoubleValidator(0.0, 2.0, 5, self))
		self.b_poisson_apply = QPushButton("Apply Sampling")
		self.b_poisson_apply.clicked.connect(self._applyPoissonDiskSampling)
		self.container.addItem(OptionBox([
			self.tf_poisson_point_count,
			self.tf_poisson_radius,
			self.b_poisson_apply
		]), "Poisson Sampling (Mesh)")

		self.tf_montecarlo_point_count = QLineEdit()
		self.tf_montecarlo_point_count.setPlaceholderText("Number of Points to Sample")
		self.tf_montecarlo_point_count.setValidator(QIntValidator(1, 1000000, self))
		self.b_montecarlo_apply = QPushButton("Apply Sampling")
		self.b_montecarlo_apply.clicked.connect(self._applyMontecarloSampling)
		self.container.addItem(OptionBox([
			self.tf_montecarlo_point_count,
			self.b_montecarlo_apply
		]), "Montecarlo Sampling (Mesh)")

		self.tf_centroid_count = QLineEdit()
		self.tf_centroid_count.setPlaceholderText("Centroid Count")
		self.tf_centroid_count.setValidator(QIntValidator(1, 1000000, self))
		self.b_show_centroids = QPushButton("Apply FPS")
		self.b_show_centroids.clicked.connect(self._applyFPS)
		self.container.addItem(OptionBox([
			self.tf_centroid_count,
			self.b_show_centroids
		]),  "FPS Sampling (Point)")

		self.tf_show_pp2_centroids = QLineEdit()
		self.tf_show_pp2_centroids.setPlaceholderText("Number of Centroids")
		self.tf_show_pp2_centroids.setValidator(QIntValidator(1, 1000000, self))
		self.tf_show_pp2_centroids_with_ball = QLineEdit()
		self.tf_show_pp2_centroids_with_ball.setPlaceholderText("Number of Centroids with plotted radius")
		self.tf_show_pp2_centroids_with_ball.setValidator(QIntValidator(1, 1000000, self))
		self.tf_show_pp2_radius = QLineEdit()
		self.tf_show_pp2_radius.setPlaceholderText("Radius of the neighbour area")
		self.tf_show_pp2_radius.setValidator(QDoubleValidator(0.0, 2.0, 5, self))
		self.b_show_pp2_step = QPushButton("Apply Sampling")
		self.b_show_pp2_step.clicked.connect(self._show_pp2_step)
		self.container.addItem(OptionBox([
			self.tf_show_pp2_centroids,
			self.tf_show_pp2_centroids_with_ball,
			self.tf_show_pp2_radius,
			self.b_show_pp2_step
		]), "Show PointNet2 sampling")


	#Event Handlers
	def _applyFPS(self, event):
		item = self.app_state.current_item
		if(item is None or item.data is None):
			return

		if(item.type != item.TypePointCloud):
			self.app_state.showError(
				'This operation can only be applyed to a Point Clouds.')
			return

		if(len(self.tf_centroid_count.text()) <= 0):
			return

		count = int(self.tf_centroid_count.text())
		rateo = count / item.data.pos.size(0)
		if(rateo >= 1):
			self.app_state.showError(
				'The number of point to select with FPS({}) have to be less than the total number of points({}).'.format(count,item.data.pos.size(0) ))
			return

		item.data.pos = item.data.pos.double()
		idx = FPS(item.data.pos, torch.zeros(item.data.pos.size(0)).long(), rateo)

		new_item = Item(
			name='{}-FPS'.format(item.name),
			data=Data(pos=item.data.pos[idx]),
			type=Item.TypePointCloud
		)
		self.app_state.setNewItem(new_item)


	def _applyPoissonDiskSampling(self, event):
		item = self.app_state.current_item
		if (item is None or item.data is None):
			return

		if (item.type != item.TypeMesh):
			self.app_state.showError(
				'This operation can only be applyed to be a Mesh object.')
			return

		if(len(self.tf_poisson_point_count.text()) <= 0
		   or len(self.tf_poisson_radius.text()) <=0):
			return

		count = int(self.tf_poisson_point_count.text())
		radio = float(self.tf_poisson_radius.text())

		item.data.pos = item.data.pos.float()
		new_data = PoissonDiskSampling(count, radio)(item.data)
		new_item = Item(
			name='{}-Poisson'.format(item.name),
			data=new_data,
			type=Item.TypePointCloud
		)
		self.app_state.setNewItem(new_item)


	def _applyMontecarloSampling(self, event):
			item = self.app_state.current_item
			if (item is None or item.data is None):
				return

			if (item.type != item.TypeMesh):
				self.app_state.showError(
					'This operation can only be applyed to be a Mesh object.')
				return

			if (len(self.tf_montecarlo_point_count.text()) <= 0):
				return

			count = int(self.tf_montecarlo_point_count.text())

			item.data.pos = item.data.pos.float()
			new_data = MontecarloSampling(count)(item.data)
			new_item = Item(
				name='{}-Montecarlo'.format(item.name),
				data=new_data,
				type=Item.TypePointCloud
			)
			self.app_state.setNewItem(new_item)

	def _applyFaceImportanceSampling(self, event):
		item = self.app_state.current_item
		if (item is None or item.data is None):
			return

		if (item.type != item.TypeMesh):
			self.app_state.showError(
				'This operation can only be applyed to be a Mesh object.')
			return

		if (len(self.tf_importance_point_count.text()) <= 0):
			return

		count = int(self.tf_importance_point_count.text())

		item.data.pos = item.data.pos.float()
		new_data = SamplePoints(count)(item.data)
		new_item = Item(
			name= '{}-ImportanceSamped'.format(item.name),
			data= new_data,
			type= Item.TypePointCloud
		)
		self.app_state.setNewItem(new_item)

	def _show_pp2_step(self, event):
		item = self.app_state.current_item
		if (item is None or item.data is None):
			return

		if (item.type != item.TypePointCloud):
			self.app_state.showError(
				'This operation can only be applyed to a Point Clouds.')
			return

		if (len(self.tf_show_pp2_centroids.text()) <= 0
			or len(self.tf_show_pp2_centroids_with_ball.text()) <= 0):
			return

		count = int(self.tf_show_pp2_centroids.text())
		rateo = count / item.data.pos.size(0)
		if (rateo >= 1):
			self.app_state.showError(
				'The number of point to select with FPS({}) have to be less than the total number of points({}).'.format(
					count, item.data.pos.size(0)))
			return

		with_ball = int(self.tf_show_pp2_centroids_with_ball.text())
		if(with_ball > count):
			self.app_state.showError(
				'The number of point for which plot the radius({}), have to be less than the sampled ammount({}).'.format(
					with_ball, count))
			return


		item.data.pos = item.data.pos.double()
		idx = FPS(item.data.pos, torch.zeros(item.data.pos.size(0)).long(), rateo)

		radius = 0.0 if len(self.tf_show_pp2_radius.text()) <=0 \
			else float(self.tf_show_pp2_radius.text())

		render = CenterAndRadious(item.data.pos.size(0),
				  centroids_idx=idx,
				  centroid_to_draw=with_ball,
				  radius=radius)

		self.app_state.setNewItem(item, render)

	def _applySaveEdit(self, event):
		sourceItem = self.app_state.current_item

		item = Item(
			data= sourceItem.data,
			name= sourceItem.name,
			type= sourceItem.type
		)

		self.app_state.addItem(item)