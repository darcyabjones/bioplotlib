""" Extension of matplotlib collections.

Classes for the efficient drawing of large collections of objects that
share most properties, e.g., a large number of line segments or
polygons.

The classes are not meant to be as flexible as their single element
counterparts (e.g., you may not be able to select all line styles) but
they are meant to be fast for common use cases (e.g., a large set of solid
line segemnts)
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import six
from six.moves import zip
import warnings
import numpy as np
import numpy.ma as ma
import matplotlib as mpl
import matplotlib.cbook as cbook
import matplotlib.colors as mcolors
import matplotlib.cm as cm
from matplotlib import docstring
import matplotlib.transforms as transforms
import matplotlib.artist as artist
from matplotlib.artist import allow_rasterization
import matplotlib.backend_bases as backend_bases
import matplotlib.path as mpath
from matplotlib import _path
import matplotlib.mlab as mlab

from matplotlib.collections import CIRCLE_AREA_FACTOR
from matplotlib.collections import Collection
from matplotlib.collections import PathCollection
from matplotlib.collections import PolyCollection


class Track(Collection):

	""" Generic collection for genomic tracks.

	Methods
	-------
	stack
		Determines how to stack features in a track
	"""

	def __init__(self):
		""" . """
		return


class Feature(Collection):

	""" Groups shapes into features so that they stay together
	in stacked tracks. """

	def __init__(self):
		""" . """
		return