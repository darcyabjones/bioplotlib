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

import numpy as np
import matplotlib.transforms as transforms
from matplotlib.path import Path
from matplotlib.patches import PathPatch

from matplotlib.collections import PathCollection

import feature_shapes
from feature_shapes import Triangle
from feature_shapes import OpenTriangle


__contributors = [
    "Darcy Jones <darcy.ab.jones@gmail.com>"
    ]

################################## Classes ###################################

class Feature(object):

    """ Groups shapes into features so that they stay together
    in stacked tracks. """

    valid_kwargs = [
        "edgecolors",
        "facecolors",
        "linewidths",
        "antialiaseds",
        "offsets",
        "transOffset",
        "offset_position",
        "norm",
        "cmap",
        "hatch",
        "zorder"
        ]

    def __init__(
            self,
            offset=0,
            by=None,
            name=None,
            **kwargs
            ):
        """ . """

        self.shapes = kwargs
        for shape, obj in self.shapes.items():
            if isinstance(obj, feature_shapes.Shape):
                obj = [obj]

            if not (0 < len(obj) <= 3):
                raise ValueError((
                        "The shape {} has an invalid number of elements."
                        "Each shape must have 1, 2, or 3 elements."
                        ).format(shape)
                    )

        self.offset = offset
        self.by = by
        self.name = name
        return

    def __call__(self):
        """ . """
        return self.draw()

    def __extend_dict(self, old_dict, new_dict):
        """ . """
        length = 0
        for k, v in old_dict.items():
            if len(v) > length:
                length = len(v)

        for key, val in new_dict:
            if key not in old_dict:
                old_dict[key] = [None] * length

            old_dict[key].extend(list(val))

        return old_dict

    def draw(self):
        """ . """

        paths = list()
        properties = dict()

        start = 0
        end = None

        paths.extend([self.shapes[start].path(*p) for
                      p in self.blocks])

        shape_pos = 0
        length_blocks = len(self.blocks)
        for i, block in enumerate(self.blocks):
            if len(self.shapes) > 1 and i + 1 == length_blocks:
                shape_pos = -1

            paths.append(self.shapes[shape_pos].path(*block))
            properties = self.__extend_dict(
                properties,
                self.shapes[shape_pos].properties
                )

            if len(self.shapes) > 1:
                shape_pos = 1

        return paths, properties


class FeatureTrack(object):

    """ Generic collection for genomic tracks.

    Methods
    -------
    stack
        Determines how to stack features in a track
    """

    def __init__(
            self,
            x=0,
            y=0,
            width=1,
            name=None,
            features=list(),
            stacking_method=None,
            angle=0,
            by='x',
            ):
        """ . """
        self.x = x
        self.y = y
        self.width = width
        self.features = list()
        self.features.extend(features)
        self.name = name
        self.stacking_method = stacking_method
        self.angle = angle  # Currently doesn't do anything.
        self.by = by
        return

    def __call__(self):
        return self.draw()

    def draw(self, ax=None):
        """ . """
        patches = list()
        for f in self.features:
            patches.extend(f.draw())

        if ax is not None:
            for patch in patches:
                ax.add_patch(patch)

        return patches

    def add_bpfeatures(
            self,
            features,
            obj=Feature
            ):
        ''' . '''
        new_features = list()
        for feature in features:
            blocks = list()
            reverse = feature.strand == -1
            parts = sorted(
                feature.location.parts,
                key=lambda f: min(f.start, f.end),
                reverse=reverse
                )
            for part in parts:
                #  Add blocks as [start, end].
                block = [
                    int(min(part.start, part.end)),
                    int(max(part.start, part.end))
                    ][::feature.strand]
                blocks.append(block)

            o = obj()
            o.add(blocks)
            o.name = feature.id
            new_features.append(o)

        self.features.extend(new_features)
        return new_features


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
