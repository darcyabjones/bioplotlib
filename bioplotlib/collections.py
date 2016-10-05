""" Extension of matplotlib collections.

Classes for the efficient drawing of large collections of objects that
share most properties, e.g., a large number of line segments or
polygons.

The classes are not meant to be as flexible as their single element
counterparts (e.g., you may not be able to select all line styles) but
they are meant to be fast for common use cases (e.g., a large set of solid
line segemnts)
"""

############################ Import all modules ##############################

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from copy import copy
from collections import defaultdict

import numpy as np
import matplotlib.transforms as transforms
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.patches import Patch

from matplotlib.collections import Collection

import feature_shapes
from feature_shapes import Triangle
from feature_shapes import OpenTriangle


__contributors = [
    "Darcy Jones <darcy.ab.jones@gmail.com>"
    ]

def new_shape(c, **kwargs):
     """ . """
     def callable(*a, **k):
         kwargs.update(k)
         return c(*a, **kwargs)
     return callable

################################## Classes ###################################

class Feature(Collection):

    """ Groups shapes into features so that they stay together
    in stacked tracks. """

    def __init__(
            self,
            blocks,
            shape=new_shape(Triangle),
            between_shape=None,
            strand=None,
            offset=0,
            by_axis=None,
            name=None,
            **kwargs
            ):
        if type(shape) in (tuple, list):
            self._shape = shape
        else:
            self._shape = [shape]

        if type(between_shape) in (tuple, list, type(None)):
            self._between_shape = between_shape
        else:
            self._between_shape = [between_shape]

        self._blocks = blocks
        self._strand = strand
        self._offset = offset
        self._by_axis = by_axis
        self._name = name

        self._paths = None
        self._patches = None

        Collection.__init__(self, **kwargs)
        self._draw_patches()
        return

    @property
    def blocks(self):
        return self._blocks

    @blocks.setter
    def blocks(self, blocks):
        self._blocks = blocks

    @property
    def strand(self):
        return self._strand

    @strand.setter
    def strand(self, strand):
        self._strand = strand
        for patch in self.patches:
            if patch.strand is not None:
                patch.strand = strand

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, offset):
        self._offset = offset
        if offset != 0:
            for patch in self.patches:
                patch.offset += offset

    @property
    def by_axis(self):
        return self._by_axis

    @by_axis.setter
    def by_axis(self, by_axis):
        self._by_axis = by_axis
        if by_axis is not None:
            for patch in self.patches:
                if patch.by_axis is not None:
                    patch.by_axis = by_axis

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, shape):
        self._shape = shape
        self._draw_patches()

    @property
    def between_shape(self):
        return self._between_shape

    @between_shape.setter
    def between_shape(self, shape):
        self._between_shape = shape
        self._draw_patches()

    @property
    def patches(self):
        return self._patches

    @patches.setter
    def patches(self, patches):
        self._patches = patches
        self._set_paths()
        self._set_props()
        return

    @property
    def paths(self):
        return self._paths

    @paths.setter
    def paths(self, paths):
        self._paths = paths
        return

    def get_paths(self):
        """ alias for paths property """
        return self.paths

    def set_paths(self, paths):
        """ alias for paths.setter """
        self.paths = paths
        return

    def _set_paths(self):
        self.paths = [
            p.get_transform().transform_path(p.get_path())
            for p in self.patches
            ]
        return

    def _set_props(self):

        def determine_facecolor(patch):
            if patch.get_fill():
                return patch.get_facecolor()
            return [0, 0, 0, 0]

        props = defaultdict(list)
        valid = {
            "facecolors": (self.set_facecolor, determine_facecolor),
            "edgecolors": (self.set_edgecolor, Patch.get_edgecolor),
            "linewidths": (self.set_linewidth, Patch.get_linewidth),
            "linestyles": (self.set_linestyle, Patch.get_linestyle),
            "antialiaseds": (self.set_antialiased, Patch.get_antialiased),
            }

        for p in self.patches:
            for key, (set_, get) in valid.items():
                props[key].append(get(p))

        for key, (set_, get) in valid.items():
            set_(props[key])
        return

    def _draw_patches(self):
        start = 0
        end = None

        patches = list()

        length_blocks = len(self.blocks)

        # Draw the between shapes first
        between_shape_pos = 0
        between_blocks = []
        if self.between_shape is not None:
            between_blocks = list(zip(
                range(0, length_blocks - 1),
                range(1, length_blocks)
                ))
        length_between_blocks = len(between_blocks)

        # Note that if between shape is none there is nothing to iterate over.
        for h, (i, j) in enumerate(between_blocks):
            first = self.blocks[i]
            second = self.blocks[j]
            min_dist = min([(0, 0), (0, 1), (1, 0), (1, 1)],
                key=lambda t: abs(second[t[0]] - first[t[1]])
                )
            start = first[min_dist[1]]
            end = second[min_dist[0]]

            strand_first = None
            strand_second = None
            try:
                strand_first = first[2]
                strand_second = second[2]
            except:
                pass

            if strand_first == strand_second:
                strand = strand_first
            else:
                strand = None

            if len(self.between_shape) > 1 and h + 1 == length_between_blocks:
                between_shape_pos = -1

            patches.append(self.between_shape[between_shape_pos](
                start=start,
                end=end,
                strand=None
                ))

            if len(self.between_shape) > 2:
                between_shape_pos = 1

        # Now do the blocks
        shape_pos = 0

        for i, block in enumerate(self.blocks):
            if len(self.shape) > 1 and i + 1 == length_blocks:
                shape_pos = -1

            start = block[0]
            end = block[1]

            strand = None
            try:
                strand = block[2]
            except:
                pass

            patches.append(self.shape[shape_pos](
                start=start,
                end=end,
                strand=strand
                ))

            if len(self.shape) > 2:
                shape_pos = 1

        if self.offset != 0:
            for patch in patches:
                patch.offset += self.offset

        self._patches = patches
        self._set_paths()
        self._set_props()
        return


class FeatureGroup(Collection):

    """ Generic collection for genomic tracks.

    Methods
    -------
    stack
        Determines how to stack features in a track
    """

    def __init__(
            self,
            features,
            width=1,
            offset=0,
            stack=None,
            by_axis=None,
            name=None,
            **kwargs
            ):
        """ . """
        self._features = features
        self._width = width
        self._stack = stack
        self._by_axis = by_axis
        self._offset = offset
        self.name = name

        self._patches = None
        self._paths = None


        Collection.__init__(self, **kwargs)
        self._draw_patches()
        return

    @property
    def features(self):
        return self._features

    @features.setter
    def features(self, features):
        """ . """
        self._features = features
        self._draw_patches()
        return

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, offset):
        self._offset = offset
        self._draw_patches()
        return

    @property
    def by_axis(self):
        return self._by_axis

    @by_axis.setter
    def by_axis(self, by_axis):
        self._by_axis = by_axis
        if by_axis is not None:
            for patch in self.patches:
                if patch.by_axis is not None:
                    patch.by_axis = by_axis
        return

    @property
    def paths(self):
        return self._paths

    @paths.setter
    def paths(self, paths):
        self._paths = paths
        return

    def get_paths(self):
        """ alias for paths property """
        return self.paths

    def set_paths(self, paths):
        """ alias for paths.setter """
        self.paths = paths
        return

    def _set_paths(self):
        self.paths = [
            p.get_transform().transform_path(p.get_path())
            for p in self._patches
            ]
        return

    def _set_props(self):

        def determine_facecolor(patch):
            if patch.get_fill():
                return patch.get_facecolor()
            return [0, 0, 0, 0]

        props = defaultdict(list)
        valid = {
            "facecolors": (self.set_facecolor, determine_facecolor),
            "edgecolors": (self.set_edgecolor, Patch.get_edgecolor),
            "linewidths": (self.set_linewidth, Patch.get_linewidth),
            "linestyles": (self.set_linestyle, Patch.get_linestyle),
            "antialiaseds": (self.set_antialiased, Patch.get_antialiased),
            }

        for p in self._patches:
            for key, (set_, get) in valid.items():
                props[key].append(get(p))

        for key, (set_, get) in valid.items():
            set_(props[key])
        return

    def _draw_patches(self):
        """ . """
        patches = list()
        for feature in self.features:
            if self._offset != 0:
                feature.offset = self._offset
            if isinstance(feature, Patch):
                patches.append(feature)
            elif isinstance(feature, Feature):
                patches.extend(feature.patches)
            elif isinstance(feature, FeatureGroup):
                patches.extend(feature.patches)
            else:
                pass

        self._patches = patches
        return


class LinkCollection(object):

    """ . """

    def __init__(
            self,
            obj,
            links=list(),
            add_to_fig=False,
            by=None
            ):
        """ . """
        self.links = list()
        self.links.extend(links)
        self.obj = obj
        self.add_to_fig = add_to_fig
        self.by = by
        lobj = obj()
        self.figure = lobj.figure

        return

    def add(self, blocks, by=None, **kwargs):
        """
        Keyword arguments:
        blocks -- a 2, 3, or 4 dimensional array
            2 dimensions: [[ax1_x1, ax1_x2], [ax2_x1, ax1_x2]] # single record
            3 dimensions:
                [
                [[ax1_x1, ax1_x2], [ax2_x1, ax2_x2]],
                [[ax1_x1, ax1_x2], [ax2_x1, ax2_x2]],
                ...
                ]
            4 dimensions:
                [
                    [
                    [[ax1_x1, ax1_x2], [ax1_y1, ax1_y2]],
                    [[ax2_x1, ax2_x2], [ax2_y1, ax2_y2]],
                    ],
                    [
                    [[ax1_x1, ax1_x2], [ax1_y1, ax1_y2]],
                    [[ax2_x1, ax2_x2], [ax2_y1, ax2_y2]],
                    ],
                    ...
                ]
        """
        by = self.by if by is None else by
        obj = self.obj

        if len(blocks) == 0:
            return list()

        blocks = np.array(blocks)
        if len(blocks.shape) == 2:
            if by == 'x' or self.by is None:
                pblocks = np.array([
                    [[ax_xrange, None] for ax_xrange in blocks]
                    ])
            elif by == 'y':
                pblocks = np.array([
                    [[None, ax_yrange] for ax_yrange in blocks]
                    ])
        elif len(blocks.shape) == 3:
            if by == 'x' or self.by is None:
                pblocks = np.array([
                    [[ax1_xrange, None],
                     [ax2_xrange, None]]
                    for ax1_xrange, ax2_xrange in blocks
                    ])
            elif by == 'y':
                pblocks = np.array([
                    [[None, ax1_yrange],
                     [None, ax2_yrange]]
                    for ax1_yrange, ax2_yrange in blocks
                    ])
        else:
            pblocks = blocks

        new_links = list()
        for block in pblocks:
            ((ax1_xrange, ax1_yrange), (ax2_xrange, ax2_yrange)) = block
            params = dict() #copy(kwargs)
            params['by'] = by
            params['ax1_xrange'] = ax1_xrange
            params['ax1_yrange'] = ax1_yrange
            params['ax2_xrange'] = ax2_xrange
            params['ax2_yrange'] = ax2_yrange
            params = {k:v for k, v in params.items() if v is not None}
            lobj = obj()
            lobj.__dict__.update(params)
            lobj.properties.update(kwargs)
            self.links.append(lobj)
            new_links.append(lobj)

        return new_links

    def __call__(self):
        return self.draw()

    def draw(self):
        """ . """
        patches = list()
        for link in self.links:
            if not link.in_limits():
                continue

            path = link.draw()
            link_patch = PathPatch(
                path,
                transform=self.figure.transFigure,
                **link.properties
                )
            rax = link.ax1
            qax = link.ax2

            patches.append(link_patch)
        if self.add_to_fig:
            self.figure.patches.extend(patches)
        return patches



################################# Functions ##################################
