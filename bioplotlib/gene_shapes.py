""" Shapes for drawing genes and gene features. """

from matplotlib.path import Path
import numpy as np
from math import sin
from math import radians
from matplotlib.patches import PathPatch


class Shape(object):

    """ Base class for drawing genomic features. """

    def __init__(
            self,
            x,
            y,
            x_offset=0,
            y_offset=0,
            width=1,
            by=None,
            **kwargs
            ):
        """ . """
        self.x = x
        self.y = y
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.width = width
        self.properties = kwargs
        self.by = by
        return

    def __call__(self):
        """ . """
        return self.draw()


class Rectangle(Shape):

    """ Rectangle. """

    def draw(self):
        """ . """
        x1, x2 = self.x
        y1, y2 = self.y

        x1 += self.x_offset
        x2 += self.x_offset
        y1 += self.y_offset
        y2 += self.y_offset

        codes = np.array([
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ])

        path = np.array([
            [x1, y1],  # bottom left
            [x2, y2],  # bottom right
            [x2, y2 + self.width],  # top right
            [x1, y1 + self.width],  # top left
            [x1, y1]  # bottom left
            ])

        if self.by == 'y':
            path[2] = [x2 + self.width, y2]
            path[3] = [x1 + self.width, y1]

        return PathPatch(Path(path, codes), **self.properties)


class Triangle(Shape):

    """ Triangle. """

    def draw(self):
        """ . """
        x1, x2 = self.x
        y1, y2 = self.y
        x1 += self.x_offset
        x2 += self.x_offset
        y1 += self.y_offset
        y2 += self.y_offset
        xm = (x1 + x2) / 2
        ym = (y1 + y2)/2

        codes = np.array([
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ])

        path = np.array([
            [x1, y1],
            [x1, y2 + self.width],
            [x2, ym + (self.width / 2)],
            [x1, y1]
            ])
        if self.by == 'y':
            path[1] = [x1 + (self.width / 2), y2]
            path[2] = [x2 + self.width, y1]

        return PathPatch(Path(path, codes), **self.properties)


class OpenTriangle(Shape):

    """ . """

    def draw(self):
        """ . """
        x1, x2 = self.x
        y1, y2 = self.y

        x1 += self.x_offset
        x2 += self.x_offset
        y1 += self.y_offset
        y2 += self.y_offset
        xm = (x1 + x2) / 2
        ym = (y1 + y2)/2

        codes = np.array([
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            ])
        path = np.array([
            [x1, y1],
            [xm, ym + self.width],
            [x2, y1],
            ])
        if self.by == 'y':
            path[1] = [xm + (self.width / 2), ym]
            path[2] = [x2 + self.width, y2]

        return PathPatch(Path(path, codes), **self.properties)


class OpenRectangle(Shape):

    """ . """

    def draw(self):
        """ . """
        x1, x2 = self.x
        y1, y2 = self.y

        x1 += self.x_offset
        x2 += self.x_offset
        y1 += self.y_offset
        y2 += self.y_offset

        codes = np.array([
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO
            ])

        path = np.array([
            [x1, y1],  # bottom left
            [x2, y2],  # bottom right
            [x2, y2 + self.width],  # top right
            [x1, y1 + self.width],  # top left
            ])

        if self.by == 'y':
            path[2] = [x2 + self.width, y2]
            path[3] = [x1 + self.width, y1]

        return PathPatch(Path(path, codes), **self.properties)


'''
class Arrow(Shape):

    """ Arrow. """

    def __init__(
            self,
            tail_width=0.8,
            tip_angle=90,
            **kwargs
            ):
        """ . """
        super().__init__(**kwargs)
        self.tail_width = tail_width
        self.tip_angle = tip_angle
        self.head_length = (sin(radians(90 - (self.tip_angle/2))) * self.width/2) / sin(radians(self.tip_angle/2))
        return

    def _draw(
            self,
            x,
            y,
            length
            ):
        """ . """
        x += self.x_offset
        y += self.y_offset

        tail_offset = (self.width - (self.width * self.tail_width)) / 2

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
        # TODO: add conditional formatting for case head_length > length
        path = np.array([
            [x, y + tail_offset],
            [x, y + self.width - tail_offset],
            [x + length - self.head_length, y + self.width - tail_offset],
            [x + length - self.head_length, y + self.width],
            [x + length, y + (self.width / 2)],
            [x + length - self.head_length, y],
            [x + length - self.head_length, y + tail_offset],
            [x, y + tail_offset]
            ])

        return path, codes


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
