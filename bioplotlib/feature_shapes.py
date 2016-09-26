""" Shapes for drawing genes and gene features. """

__contributors = [
    "Darcy Jones <darcy.ab.jones@gmail.com>"
    ]


############################ Import all modules ##############################

from math import sin
from math import radians

import numpy as np
from matplotlib.patches import PathPatch
from matplotlib.path import Path


################################## Classes ###################################

class Shape(object):

    """ Base class for drawing genomic features.

    Shape objects are templates for later drawing.
    """

    def __init__(
            self,
            offset=0,
            width=1,
            by=None,
            **kwargs
            ):
        """ . """
        self.offset = offset
        self.width = width
        self.properties = kwargs
        self.by = by
        return

    def __call__(self, *args, **kwargs):
        """ The call method simply calls the draw() method. """
        return self.patch(*args, **kwargs)

    def path(self, start, end, offset=0, *args, **kwargs):
        """ . """
        return

    def patch(self, start, end, offset=0, *args, **kwargs):
        """ . """
        return PathPatch(
            self.path(start, end, offset, *args, **kwargs),
            **self.properties
            )

    def draw(self, *args, **kwargs):
        """ . """
        return self.patch(*args, **kwargs)


class Rectangle(Shape):

    """ Rectangle. """

    def path(self, start, end, offset=0, *args, **kwargs):
        """ . """

        offset += self.offset

        codes = np.array([
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ])

        path = np.array([
            [start, offset],  # bottom left
            [start, offset + self.width],  # top left
            [end, offset + self.width],  # top right
            [end, offset],  # bottom right
            [start, offset]  # bottom left
            ])

        if self.by == "y":
            path = path[:,::-1]

        return Path(path, codes)


class Triangle(Shape):

    """ Triangle. """

    def path(self, start, end, offset=0, *args, **kwargs):
        """ . """

        offset += self.offset

        middle = (start + end) / 2

        codes = np.array([
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ])

        path = np.array([
            [start, offset],
            [start, offset + self.width],
            [end, offset + (self.width / 2)],
            [start, offset]
            ])

        if self.by == "y":
            path = path[:,::-1]

        return Path(path, codes)


class Arrow(Shape):

    """ Arrow. """

    def __init__(
            self,
            tail_width=1,
            head_length=1,
            **kwargs
            ):
        """ . """
        super().__init__(**kwargs)
        self.tail_width = tail_width
        self.head_length = head_length
        return

    def path(self, start, end, offset=0, *args, **kwargs):
        """ . """
        offset += self.offset

        if self.head_length >= abs(end - start):
            return Triangle.path(self, start, end, offset, *args, **kwargs)

        tail_width = self.width * self.tail_width
        tail_offset = offset + (self.width - tail_width) / 2

        codes = np.array([
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ])

        path = np.array([
            [start, tail_offset],
            [start, tail_offset + tail_width],
            [end - self.head_length, tail_offset + tail_width],
            [end - self.head_length, offset + self.width],
            [end, offset + (self.width / 2)],
            [end - self.head_length, offset],
            [end - self.head_length, tail_offset],
            [start, tail_offset]
            ])

        if self.by == "y":
            path = path[:,::-1]

        return Path(path, codes)


class OpenTriangle(Shape):

    """ . """

    def path(self, start, end, offset=0, *args, **kwargs):
        """ . """

        offset += self.offset

        codes = np.array([
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            ])

        path = np.array([
            [start, offset],
            [(start + end) / 2, offset + self.width],
            [end, offset],
            ])

        if self.by == "y":
            path = path[:,::-1]

        return Path(path, codes)


class OpenRectangle(Shape):

    """ . """

    def path(self, start, end, offset=0, *args, **kwargs):
        """ . """

        offset += self.offset

        codes = np.array([
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO
            ])

        path = np.array([
            [start, offset],  # bottom left
            [start, offset + self.width],  # top left
            [end, offset + self.width],  # top right
            [end, offset],  # bottom right
            ])

        if self.by == "y":
            path = path[:,::-1]

        return Path(path, codes)

class OpenSemicircle(Shape):

    """ . """

    def path(self, start, end, offset=0, *args, **kwargs):
        """ . """

        offset += self.offset

        codes = np.array([
            Path.MOVETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.LINETO,
            ])

        path = np.array([
            [start, offset],  # bottom left
            [start, offset + self.width],  # top left
            [end, offset + self.width],  # top right
            [end, offset],  # bottom right
            ])

        if self.by == "y":
            path = path[:,::-1]

        return Path(path, codes)

'''

class Hexagon(Shape):

    """ Hexagon. """

    def __init__(self):
        return


class Ellipse(Shape):

    """ Ellipse. """

    def __init__(self):
        return


class Trapeziod(Shape):

    """ Trapeziod. """

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
'''
