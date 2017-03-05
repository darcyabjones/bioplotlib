from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from builtins import (
    bytes, dict, int, list, object, range, str,
    ascii, chr, hex, input, next, oct, open,
    pow, round, super, filter, map, zip
    )

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

class Shape(matplotlib.patches.Patch):

    """ Base class for drawing genomic features.

    Shape objects are templates for later drawing.
    """

    def __init__(
            self,
            start,
            end,
            strand=None,
            width=1,
            offset=0,
            by_axis=None,
            name=None,
            **kwargs
            ):
        """ . """
        super().__init__(**kwargs)
        self._start = start
        self._end = end
        self._strand = strand
        self._offset = offset
        self._width = width
        self._by_axis = by_axis
        self.name = name
        self._draw_path()
        return

    def __repr__(self):
        clss = type(self).__doc__.strip().strip(".")
        return ("{obj}(start={_start}, "
                      "end={_end}, "
                      "offset={_offset}, "
                      "width={_width}, "
                      "by_axis={_by_axis})").format(obj=clss, **self.__dict__)

    def _draw_vertices(self):
        raise NotImplementedError
        return

    def _draw_path(self):
        self._draw_vertices()
        try:
            self._path.vertices = self._vertices
        except AttributeError:
            self._path = Path(self._vertices, self._codes)

    @property
    def path(self):
        return self._path

    def get_path(self):
        # Alias to path
        return self.path

    @property
    def vertices(self):
        return self._vertices

    @vertices.setter
    def vertices(self, vertices):
        self._vertices = vertices
        self._draw_path()
        return

    @property
    def codes(self):
        return self._codes

    @codes.setter
    def codes(self, codes):
        self._codes = codes
        self._draw_path()
        return

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        self._start = start
        self._draw_path()
        return

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        self._end = end
        self._draw_path()
        return

    @property
    def strand(self):
        return self._strand

    @strand.setter
    def strand(self, strand):
        self._strand = strand
        self._draw_path()
        return

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, offset):
        self._offset = offset
        self._draw_path()
        return

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width
        self._draw_path()
        return

    @property
    def by_axis(self):
        return self._by_axis

    @by_axis.setter
    def by_axis(self, by_axis):
        self._by_axis = by_axis
        self._draw_path()


class Rectangle(Shape):

    """ Rectangle. """

    def __init__(
            self,
            start,
            end,
            strand=None,
            width=1,
            offset=0,
            by_axis=None,
            name=None,
            **kwargs
            ):

        self._codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ]

        super().__init__(
            start=start,
            end=end,
            strand=strand,
            offset=offset,
            width=width,
            by_axis=by_axis,
            name=name,
            **kwargs
            )
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

        if self.by_axis == "y":
            self._vertices = self._vertices[:,::-1]

        return


class Triangle(Shape):

    """ Triangle. """
    def __init__(
            self,
            start,
            end,
            strand=None,
            width=1,
            offset=0,
            by_axis=None,
            name=None,
            **kwargs
            ):

        self._codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ]

        super(self).__init__(
            start=start,
            end=end,
            strand=strand,
            offset=offset,
            width=width,
            by_axis=by_axis,
            name=name,
            **kwargs
            )
        return

    def _draw_vertices(self):
        """ . """

        start = self.start
        end = self.end
        width = self.width
        offset = self.offset
        strand = self.strand

        if strand == -1:
            start = self.end
            end = self.start

        self._vertices = np.array([
            [start, offset],
            [start, offset + width],
            [end, offset + (width / 2)],
            [start, offset]
            ])

        if self.by_axis == "y":
            self._vertices = self._vertices[:,::-1]
        return


class Arrow(Shape):

    """ Arrow. """

    def __init__(
            self,
            start,
            end,
            strand=None,
            head_length=1,
            tail_width=None,
            width=1,
            offset=0,
            by_axis=None,
            name=None,
            **kwargs
            ):
        """ . """
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

        self._tail_width = tail_width
        self._head_length = head_length

        super().__init__(
            start=start,
            end=end,
            strand=strand,
            offset=offset,
            width=width,
            by_axis=by_axis,
            name=name,
            **kwargs
            )
        return

    @property
    def head_length(self):
        return self._head_length

    @head_length.setter
    def head_length(self, head_length):
        self._head_length = head_length
        self._draw_vertices()

    @property
    def tail_width(self):
        return self._tail_width

    @tail_width.setter
    def tail_width(self, tail_width):
        self._tail_width = tail_width
        self._draw_vertices()

    def _draw_vertices(self):
        """ . """

        start = self.start
        end = self.end
        strand = self.strand
        width = self.width
        offset = self.offset

        head_length = self.head_length
        tail_width = self.tail_width

        if tail_width is None:
            tail_width = self.width

        if abs(head_length) > abs(end - start):
            head_length = end - start

        if start > end:
            head_length *= -1

        if strand == -1:
            start = self.end
            end = self.start
            head_length *= -1

        tail_offset = offset + (width - tail_width) / 2

        self._vertices = np.array([
            [start, tail_offset],
            [start, tail_offset + tail_width],
            [end - head_length, tail_offset + tail_width],
            [end - head_length, offset + width],
            [end, offset + (width / 2)],
            [end - head_length, offset],
            [end - head_length, tail_offset],
            [start, tail_offset]
            ])

        if self.by_axis == "y":
            self._vertices = self._vertices[:,::-1]

        return


class OpenTriangle(Shape):

    """ . """
    def __init__(
            self,
            start,
            end,
            strand=None,
            width=1,
            offset=0,
            by_axis=None,
            name=None,
            **kwargs
            ):

        self._codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO
            ]

        super().__init__(
            start=start,
            end=end,
            strand=strand,
            offset=offset,
            width=width,
            by_axis=by_axis,
            name=name,
            **kwargs
            )
        return

    def _draw_vertices(self):
        """ . """

        start = self.start
        end = self.end
        offset = self.offset
        width = self.width

        self._vertices = np.array([
            [start, offset],
            [(start + end) / 2, offset + width],
            [end, offset],
            ])

        if self.by_axis == "y":
            self._vertices = self._vertices[:,::-1]

        return


class OpenRectangle(Shape):

    """ . """
    def __init__(
            self,
            start,
            end,
            strand=None,
            width=1,
            offset=0,
            by_axis=None,
            name=None,
            **kwargs
            ):

        self._codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO
            ]

        super().__init__(
            start=start,
            end=end,
            strand=strand,
            offset=offset,
            width=width,
            by_axis=by_axis,
            name=name,
            **kwargs
            )
        return

    def _draw_vertices(self):
        """ . """

        start = self.start
        end = self.end
        offset = self.offset
        width = self.width

        self._vertices = np.array([
            [start, offset],  # bottom left
            [start, offset + width],  # top left
            [end, offset + width],  # top right
            [end, offset],  # bottom right
            ])

        if self.by_axis == "y":
            self._vertices = self._vertices[:,::-1]

        return

class OpenSemicircle(Shape):

    """ . """
    def __init__(
            self,
            start,
            end,
            strand=None,
            width=1,
            offset=0,
            by_axis=None,
            name=None,
            **kwargs
            ):

        self._codes = [
            Path.MOVETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            ]

        super().__init__(
            start=start,
            end=end,
            strand=strand,
            offset=offset,
            width=width,
            by_axis=by_axis,
            name=name,
            **kwargs
            )
        return


    def _draw_vertices(self):
        """ . """
        start = self.start
        end = self.end
        offset = self.offset
        width = self.width

        self._vertices = np.array([
            [start, offset],  # bottom left
            [start, offset + width],  # top left
            [end, offset + width],  # top right
            [end, offset],  # bottom right
            ])

        if self.by_axis == "y":
            self._vertices = self._vertices[:,::-1]

        return

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
