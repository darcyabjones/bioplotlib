""" Shapes for drawing genes and gene features. """

from matplotlib.path import Path
import numpy as np


class Shape(object):

	""" Base class for drawing genomic features. """

	def __init__(
			self,
			angle=0,
			x_offset=0,
			y_offset=0,
			):
		""" . """
		self.angle = angle
		self.x_offset = x_offset
		self.y_offset = y_offset
		return

	def __call__(
			self,
			x,
			y,
			length,
			width
			):
		""" . """
		return


class Rectangle(Shape):

	""" Rectangle. """

	def _draw(
			self,
			x,
			y,
			length,
			width
			):
		""" . """
		x += x_offset * length
		y += y_offset * width

		codes = np.array([
			Path.MOVETO,
			Path.LINETO,
			Path.LINETO,
			PATH.LINETO,
			PATH.CLOSEPOLY
			])

		path = np.array([
			[x, y],  # bottom left
			[x + length, y],  # bottom right
			[x + length, y + width],  # top right
			[x, y + width],  # top left
			[x, y]  # bottom left
			])
		return path, codes

	def _rotate(self):
		""" . """
		
		return


class Arrow(Shape):

	""" Arrow. """

	def __init__(self):
		return


class Hexagon(Shape):

	""" Hexagon. """

	def __init__(self):
		return


class Ellipse(Shape):

	""" Ellipse. """

	def __init__(self):
		return


class Triangle(Shape):

	""" Triangle. """

	def __init__(self):
		return


class Trapeziod(Shape):

	""" Trapeziod. """

	def __init__(self):
		return