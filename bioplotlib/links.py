from matplotlib.transforms import Bbox
from matplotlib.transforms import TransformedBbox
from matplotlib.transforms import blended_transform_factory
from mpl_toolkits.axes_grid1.inset_locator import BboxPatch
from mpl_toolkits.axes_grid1.inset_locator import BboxConnector
from mpl_toolkits.axes_grid1.inset_locator import BboxConnectorPatch
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np

class CrossLink(object):

    """ . """

    def __init__(
            self,
            ax1,
            ax2=None,
            ax1_xrange=None,  # (0, 1)
            ax2_xrange=None,
            ax1_yrange=None,  # (0, 1)
            ax2_yrange=None,
            ax1_cpoint=None,
            ax2_cpoint=None,
            cpoint_offset=0.,
            by=None,
            **kwargs
            ):
        """
        Keyword Arguments:
        ax1 -- The matplotlib axes instance.
        ax2 -- The matplotlib axes instance.
        ax1_xrange -- tuple as (xmin, xmax).
        ax2_xrange -- tuple as (xmin, xmax).
        ax1_yrange -- tuple as (ymin, ymax).
        ax2_yrange -- tuple as (ymin, ymax).
        ax1_cpoint -- float, control point for bezier drawing.
        ax2_cpoint -- float, control point for bezier drawing.
        See <http://matplotlib.org/api/patches_api.html#matplotlib.patches.Patch>
        for valid kwargs.
        """
        self.ax1 = ax1
        if ax2 is None:
            self.ax2 = ax1
        else:
            self.ax2 = ax2

        self.figure = ax1.figure
        self.by = by

        self.ax1_cpoint = ax1_cpoint
        self.ax2_cpoint = ax2_cpoint
        self.cpoint_offset = cpoint_offset

        self.ax1_xrange = ax1_xrange
        self.ax2_xrange = ax2_xrange
        self.ax1_yrange = ax1_yrange
        self.ax2_yrange = ax2_yrange

        if self.by == 'y':
            if self.ax1_xrange is None:
                self.ax1_xrange = [0, 1]
            if self.ax2_xrange is None:
                self.ax2_xrange = self.ax1_xrange
        else:
            if self.ax1_yrange is None:
                self.ax1_yrange = [0, 1]
            if self.ax2_yrange is None:
                self.ax2_yrange = self.ax1_yrange

        self.transform_ax1 = None
        self.transform_ax2 = None

        self.valid_kwargs = {
            "alpha", "animated", "antialiased",
            "axes", "capstyle", "clip_box",
            "clip_on", "clip_path", "color",
            "contains", "edgecolor", "facecolor",
            "figure", "fill", "gid", "hatch",
            "joinstyle", "label", "linestyle",
            "linewidth", "lod", "path_effects",
            "picker", "rasterized", "sketch_params",
            "snap", "transform", "url",
            "visible", "zorder", "ec", "fc",
            }
        self.properties = dict()
        self.properties['clip_on'] = False
        self.properties['zorder'] = 0
        for key, value in kwargs.items():
            if key in self.valid_kwargs:
                self.properties[key] = value
        return

    def __call__(self):
        return self.draw()

    def in_limits(self):
        if self.by == 'y':
            s1, e1 = self.ax1_yrange
            s2, e2 = self.ax2_yrange
            ls1, le1 = self.ax1.get_ylim()
            ls2, le2 = self.ax2.get_ylim()
        else:
            s1, e1 = self.ax1_xrange
            s2, e2 = self.ax2_xrange
            ax1_xlim = self.ax1.get_xlim()
            ax2_xlim = self.ax2.get_xlim()
            ls1, le1 = min(ax1_xlim), max(ax1_xlim)
            ls2, le2 = min(ax2_xlim), max(ax2_xlim)

        checks = [
            (ls1 <= s1 <= le1),
            (ls1 <= e1 <= le1),
            (ls2 <= s2 <= le2),
            (ls2 <= e2 <= le2),
            ]

        return all(checks)

    def draw(self):
        """ . """

        x1 = np.array(self.ax1_xrange)
        x2 = np.array(self.ax2_xrange)
        y1 = np.array(self.ax1_yrange)
        y2 = np.array(self.ax2_yrange)

        def orient(s, e):
            if s == e:
                return 1
            else:
                return (e - s) / abs(e - s)

        if (orient(y1[0], y1[1]) != orient(y2[0], y2[1])) and self.by != 'y':
            inverted = True
        elif (orient(x1[0], x1[1]) != orient(x2[0], x2[1])) and self.by == 'y':
            inverted = True
        else:
            inverted = False

        def_cp = 0 if inverted else 1  # Default for straight comparisons is 1
        # If the control point is None we set to def_cp (straight line for inverted, curved for not inverted)
        ax1_cp = self.ax1_cpoint if self.ax1_cpoint is not None else def_cp
        ax2_cp = self.ax2_cpoint if self.ax2_cpoint is not None else ax1_cp

        if self.by != 'y':
            ax1_orient = orient(y1[0], y1[1])
            ax2_orient = orient(y2[0], y2[1])
        else:
            ax1_orient = orient(x1[0], x1[1])
            ax2_orient = orient(x2[0], x2[1])

        if self.ax1_cpoint is None:
            ax1_cp *= ax1_orient
        if self.ax2_cpoint is None:
            ax2_cp *= ax2_orient

        if self.by == 'y':
            s1, e1 = y1
            s2, e2 = y2
            iby = -1
        else:
            s1, e1 = x1
            s2, e2 = x2
            iby = 1

        if self.transform_ax1 is not None:
            transform_ax1 = self.transform_ax1
        else:
            transform_ax1 = blended_transform_factory(
                *[self.ax1.transData, self.ax1.transAxes][::iby]
                )
        if self.transform_ax2 is not None:
            transform_ax2 = self.transform_ax2
        else:
            transform_ax2 = blended_transform_factory(
                *[self.ax2.transData, self.ax2.transAxes][::iby]
                )

        loffset = 1 - self.cpoint_offset
        uoffset = 1 + self.cpoint_offset

        # Find the distance between the points in figure coords
        if inverted:
            cmps = [(s1, e2), (s2, e1), (s1, s2), (e1, e2)]
            cmp_idxs = [[0, 3], [2, 1], [0, 2], [1, 3]]
        else:
            cmps = [(s1, e2), (e1, s2)] * 2
            cmp_idxs = [[0, 3], [1, 2]] * 2


        distances = np.array([
            np.absolute(transform_ax1.transform([s, 0][::iby]) -
                transform_ax2.transform([e, 0][::iby]))
            for s, e in cmps
            ])
        dist_max = max(distances, key=lambda t: t[0])
        dist_min = min(distances, key=lambda t: t[0])
        max_idxs = (distances[:,0] == dist_max[0]).nonzero()[0]
        min_idxs = (distances[:,0] == dist_min[0]).nonzero()[0]

        trans = self.figure.transFigure.inverted().transform
        distances = np.apply_along_axis(trans, 1, distances)[:,0]

        dists = np.array([None] * 4)
        for i, idxs in zip(range(4), cmp_idxs):
            if i in max_idxs:
                dists[idxs] = uoffset * distances[i]
            elif i in min_idxs:
                dists[idxs] = loffset * distances[i]
            else:
                dists[idxs] = distances[i]

        d1 = dists[0:2] #[::iby]
        d2 = dists[2:4] #[::iby]

        path = np.array([
            [x1[0], y1[1]],  # 0
            [x1[0], y1[1] + ax1_cp * d1[0]],  # 1
            [x2[1], y2[1] + ax2_cp * d2[1]],  # 2
            [x2[1], y2[1]],  # 3
            [x2[1], y2[0]],  # 4
            [x2[0], y2[0]],  # 5
            [x2[0], y2[1]],  # 6
            [x2[0], y2[1] + ax2_cp * d2[0]],  # 7
            [x1[1], y1[1] + ax1_cp * d1[1]],  # 8
            [x1[1], y1[1]],  # 9
            [x1[1], y1[0]],  # 10
            [x1[0], y1[0]],  # 11
            [x1[0], y1[1]],  # 12
            [x1[0], y1[0]],  # 13
            ])

        codes = np.array([
            Path.MOVETO,  # 0
            Path.CURVE4,  # 1
            Path.CURVE4,  # 2
            Path.CURVE4,  # 3
            Path.LINETO,  # 4
            Path.LINETO,  # 5
            Path.LINETO,  # 6
            Path.CURVE4,  # 7
            Path.CURVE4,  # 8
            Path.CURVE4,  # 9
            Path.LINETO,  # 10
            Path.LINETO,  # 11
            Path.LINETO,  # 12
            Path.CLOSEPOLY,  # 13
            ])

        if self.by == 'y':
            path[1] = [x1[0] + ax1_cp * dist_a, y1[1]]
            path[2] = [x2[1] + ax2_cp * dist_a, y2[1]]
            path[7] = [x2[0] + ax2_cp * dist_b, y2[1]]
            path[8] = [x1[1] + ax1_cp * dist_b, y1[1]]

        if inverted:
            path[2:8] = path[2:8][::-1]

        transforms = [
            transform_ax1.transform,
            transform_ax1.transform,
            transform_ax2.transform,
            transform_ax2.transform,
            transform_ax2.transform,
            transform_ax2.transform,
            transform_ax2.transform,
            transform_ax2.transform,
            transform_ax1.transform,
            transform_ax1.transform,
            transform_ax1.transform,
            transform_ax1.transform,
            transform_ax1.transform,
            transform_ax1.transform,
            ]

        path = np.array([t(xy) for t, xy in zip(transforms, path)])
        path = np.apply_along_axis(
            self.figure.transFigure.inverted().transform,
            1,
            path
            )
        return Path(path, codes)
