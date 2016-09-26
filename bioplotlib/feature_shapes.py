""" Shapes for drawing genes and gene features. """

__contributors = [
    "Darcy Jones <darcy.ab.jones@gmail.com>"
    ]


############################ Import all modules ##############################

from math import sin
from math import radians

import numpy as np

import matplotlib
from matplotlib.patches import PathPatch
from matplotlib.path import Path


################################## Classes ###################################

class Shape(matplotlib.path.Path):

    """ Base class for drawing genomic features.

    Shape objects are templates for later drawing.
    """

    def __init__(
            self,
            start,
            end,
            strand=None,
            offset=0,
            width=1,
            by=None,
            **kwargs
            ):
        """ . """
        self._start = start
        self._end = end
        self._strand = strand
        self._offset = offset
        self._width = width
        self._by = by
        self._draw_vertices()
        self._codes = None
        super().__init__(self._vertices, **kwargs)
        return

    def __repr__(self):
        clss = type(self).__doc__.strip().strip(".")
        return ("{obj}(start={_start}, "
                      "end={_end}, "
                      "offset={_offset}, "
                      "width={_width}, "
                      "by={_by})").format(obj=clss, **self.__dict__)

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        self._start = start
        self._draw_vertices()
        return

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        self._end = end
        self._draw_vertices()
        return

    @property
    def strand(self):
        return self._strand

    @strand.setter
    def strand(self, strand):
        if strand in (True, 0, "+", "forward"):
            strand = "+"
        elif strand in (False, 1, "-", "reverse"):
            strand = "-"
        else:
            strand = None

        self._strand = strand
        self._draw_vertices()
        return

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, offset):
        self._offset = offset
        self._draw_vertices()
        return

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width
        self._draw_vertices()
        return

    @property
    def by(self):
        return self._by

    @end.setter
    def by(self, by):
        self._by = by
        self._draw_vertices()


class Rectangle(Shape):

    """ Rectangle. """

    def _draw_codes(self):
        self._codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ]
        return

    def _draw_vertices(self):
        """ . """

        start = self.start
        end = self.end
        width = self.width
        offset = self.offset

        self._vertices = np.array([
            [start, offset],  # bottom left
            [start, offset + width],  # top left
            [end, offset + width],  # top right
            [end, offset],  # bottom right
            [start, offset]  # bottom left
            ])

        if self.by == "y":
            self._vertices = path[:,::-1]

        self._update_values()
        return


class Triangle(Shape):

    """ Triangle. """

    def _draw_codes(self):
        self._codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ]
        return

    def _draw_vertices(self):
        """ . """

        start = self.start
        end = self.end
        width = self.width
        offset = self.offset
        strand = self.strand

        if strand is None:
            if start > end:
                strand = "-"

        if strand == "-":
            start = self.end
            end = self.start

        self._vertices = np.array([
            [start, offset],
            [start, offset + width],
            [end, offset + (width / 2)],
            [start, offset]
            ])

        if self.by == "y":
            self._vertices = path[:,::-1]

        self._update_values()
        return


class Arrow(Shape):

    """ Arrow. """

    def __init__(
            self,
            start,
            end,
            strand=None,
            offset=0,
            width=1,
            by=None,
            head_length=1,
            tail_width=None,
            **kwargs
            ):
        """ . """
        self._tail_width = tail_width
        self._head_length = head_length

        super().__init__(start, end, strand, offset, width, by, **kwargs)
        return

    @property
    def head_length(self):
        return self._head_length

    @head_length.setter
    def by(self, head_length):
        self._head_length = head_length
        self._draw_vertices()

    @property
    def tail_width(self):
        return self._tail_width

    @tail_width.setter
    def by(self, tail_width):
        self._tail_width = tail_width
        self._draw_vertices()

    def _draw_codes(self):
        self._codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ]
        return

    def _draw_vertices(self):
        """ . """

        start = self.start
        end = self.end
        strand = self.strand
        width = self.width
        offset = self.offset
        head_length = self.head_length
        tail_width = self.tail_width

        length = abs(end - start)
        print("length", length)

        if tail_width is None:
            tail_width = self.width
        print("tw", tail_width)

        if abs(head_length) > abs(length):
            print("abs Head length")
            head_length = length
        print("hl", head_length)

        if strand is None and start > end:
            length *= -1
            head_length *= -1

        if strand == "-":
            start = self.end
            length *= -1
            head_length *= -1

        tail_offset = offset + (width - tail_width) / 2

        print("start", start)
        print("length", length)
        print("hl", head_length)


        self._vertices = np.array([
            [start, tail_offset],
            [start, tail_offset + tail_width],
            [start + length - head_length, tail_offset + tail_width],
            [start + length - head_length, offset + width],
            [start + length, offset + (width / 2)],
            [start + length - head_length, offset],
            [start + length - head_length, tail_offset],
            [start, tail_offset]
            ])

        if self.by == "y":
            self._vertices = path[:,::-1]

        self._update_values()
        return


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
