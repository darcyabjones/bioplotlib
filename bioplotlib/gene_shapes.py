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

	def _rotate(self):
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
		x += self.x_offset * length
		y += self.y_offset * width

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


class Arrow(Shape):

	""" Arrow. """

	def __init__(
			self,
			angle=0,
			x_offset=0,
			y_offset=0,
			tail_width=0.8
			):
		""" . """
		self.angle = angle
		self.x_offset = x_offset
		self.y_offset = y_offset
		self.tail_width = tail_width
		return

	def _draw(
			self,
			x,
			y,
			length,
			width
			):

		x += self.x_offset * length
		y += self.y_offset * width

		tail_offset = (width - self.tail_width) / 2

		path = np.array([
			[x, y + tail_offset],
			[]
			])
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


class OpenTriangle(Shape):

	""" . """

	def __init__(self):
		return


class OpenRectangle(Shape):

	""" . """

	def __init__(self):
		return


class SineWave(Shape):

	""" . """

	def __init__(self):
		return


class SawtoothWave(Shape):

	""" . """

	def __init__(self):
		return


class SquareWave(Shape):

	""" . """

	def __init__(self):
		return


class TriangleWave(Shape):

	""" . """

	def __init__(self):
		return


class Helix(Shape):

	""" . """

	def __init__(self):
		return


class DoubleHelix(Shape):

	""" . """

	def __init__(self):
		return