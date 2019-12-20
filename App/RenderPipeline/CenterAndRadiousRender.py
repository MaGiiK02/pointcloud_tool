import numpy
from Normalization.Normalization import Normalize

class CenterAndRadious():
	def __init__(self, item_count, centroid_to_draw, centroids_idx, radius):
		self.centroids_mask = centroids_idx.numpy()
		self.radius = radius
		self.normalizer = Normalize()
		self.centroids_to_show = centroid_to_draw

	def __call__(self, item, ax):
		#fig.pause(1000)
		data = self.normalizer(item.data)
		centroids = data.pos[self.centroids_mask].transpose(0,1)
		pos = numpy.delete(data.pos.numpy(), self.centroids_mask, 0).transpose(-1,0) #all the point except the centroids

		ax.scatter(pos[0], pos[1], pos[2], c='r', marker='.')
		ax.scatter(centroids[0], centroids[1], centroids[2], c='b', marker='.')

		## Draw centroids radius
		if(self.radius > 0):
			centroids = centroids.transpose(-1, 0)
			for c in centroids[:self.centroids_to_show]:
				# Make data
				u = numpy.linspace(0, 2*numpy.pi, 100)
				v = numpy.linspace(0, numpy.pi, 100)
				x = (self.radius * numpy.outer(numpy.cos(u), numpy.sin(v))) + c[0].numpy()
				y = (self.radius * numpy.outer(numpy.sin(u), numpy.sin(v))) + c[1].numpy()
				z = (self.radius * numpy.outer(numpy.ones(numpy.size(u)), numpy.cos(v))) +c[2].numpy()
				ax.plot_surface(x, y, z, color=(0.0, 0.0, 0.5, 0.1))


		return ax
