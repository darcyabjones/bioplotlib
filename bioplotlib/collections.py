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

from copy import copy

import numpy as np
import matplotlib.transforms as transforms
from matplotlib.path import Path
from matplotlib.patches import PathPatch

from gene_shapes import Rectangle
from gene_shapes import OpenTriangle

def new_shape(c, **kwargs):
    """ . """
    def callable(*p, **k):
        d = kwargs
        d.update(k)
        return c(*p, **d)
    return callable


class Feature(object):

    """ Groups shapes into features so that they stay together
    in stacked tracks. """

    def __init__(
            self,
            blocks=list(),
            shape=new_shape(Rectangle, width=1, y_offset=-0.5),
            between_shape=new_shape(OpenTriangle, width=0.5, facecolor='none'),
            first_shape=None,
            last_shape=None,
            by=None,
            name=None,
            ):
        """ . """
        self.blocks = list()
        self.shape = shape
        self.between_shape = between_shape
        self.first_shape = first_shape
        self.last_shape = last_shape
        self.by = by
        self.name = name
        self.add(blocks)
        return

    def add(self, blocks):
        """ . """
        if len(blocks) == 0:
            return

        blocks = np.array(blocks)
        iby = -1 if self.by == 'y' else 1
        if len(blocks.shape) == 1:
            s, e = blocks
            self.blocks.extend(np.array([
                [[s, e], [0, 0]][::iby]
                ]))

        elif len(blocks.shape) == 2:
            self.blocks.extend(np.array([
                [(s, e), (0, 0)][::iby] for s, e in blocks
                ]))
        else:
            self.blocks = blocks

        # TODO:  Find the width + offset to get bounds of it.
        #  Precalculate min and max values for x and y for sorting.

        xvals = np.array(self.blocks)[:,:,0].flatten()
        yvals = np.array(self.blocks)[:,:,1].flatten()
        self.xrange = xvals.min(), xvals.max()
        self.yrange = yvals.min(), xvals.max()
        return

    def __call__(self):
        """ . """
        return self.draw()

    def draw(self):
        """ . """
        block_patches = list()
        between_patches = list()

        prev_block = None
        for i, block in enumerate(self.blocks):
            x, y = block

            #  Draw blocks (ie exons)
            if i == 0 and self.first_shape is not None:
                s = self.first_shape(x, y)
            elif i == len(self.blocks) - 1 and self.last_shape is not None:
                s = self.last_shape(x, y)
            else:
                s = self.shape(x, y)
            block_patches.append(s.draw())

            if prev_block is None or self.between_shape is None:
                prev_block = block
                continue

            #  Draw between blocks (ie introns).
            #  `-` just catches the bits that we aren't interested in.
            (_, x1), (_, y1) = prev_block
            (x2, _), (y2, _) = block

            s = self.between_shape([x1, x2], [y1, y2])
            between_patches.append(s.draw())

            prev_block = block

        #  Add between patches first to draw blocks on top.
        patches = between_patches
        patches.extend(block_patches)
        return patches


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
