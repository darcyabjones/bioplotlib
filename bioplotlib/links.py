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

    def __init__(self,
            ax1,
            ax2=None,
            y1_range=(0, 1),
            y2_range=None,
            y1_control_point=None,
            y2_control_point=None,
            control_point_offset=0.1,
            add_to_fig=True,
            **kwargs
            ):
        """
        Keyword Arguments:
        ax -- The upper matplotlib axes instance.
        yrange -- tuple as (ymin, ymax) where ymin \
            and ymax are between [0, 1]. default = (0, 1).
        add_to_axes -- add the patches to the axes (default = True).

        See <http://matplotlib.org/api/patches_api.html#matplotlib.patches.Patch>
        for valid kwargs.
        """
        self.ax1 = ax1
        if ax2 is None:
            self.ax2 = ax1
        else:
            self.ax2 = ax2

        self.figure = ax1.figure

        self.y1_control_point = y1_control_point
        self.y2_control_point = y2_control_point
        self.control_point_offset = control_point_offset

        self.y1_range = y1_range
        if y2_range is None:
            self.y2_range = y1_range
        else:
            self.y2_range = y2_range

        self.y1_control_point = y1_control_point
        self.y2_control_point = y2_control_point

        self.transform_ax1 = blended_transform_factory(
            self.ax1.transData,
            self.ax1.transAxes
            )
        self.transform_ax2 = blended_transform_factory(
            self.ax2.transData,
            self.ax2.transAxes
            )

        self.add_to_fig = add_to_fig

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

    def __call__(
            self,
            x1_start,
            x1_length,
            x2_start,
            x2_length,
            y1_control_point=None,
            y2_control_point=None,
            **kwargs
            ):
        """ . """
        properties = self.properties.copy()
        properties.update(kwargs)

        if y1_control_point is None:
            y1_control_point = self.y1_control_point
        if y2_control_point is None:
            y2_control_point = self.y2_control_point

        path, codes = self._draw(
            x1_start,
            x1_length,
            x2_start,
            x2_length,
            y1_control_point=y1_control_point,
            y2_control_point=y2_control_point
            )

        link_patch = patches.PathPatch(
            Path(path, codes),
            transform=self.figure.transFigure,
            **properties
            )

        if self.add_to_fig:
            self.figure.patches.append(link_patch)

        return link_patch, path, codes

    def _draw(
            self,
            x1_start,
            x1_length,
            x2_start,
            x2_length,
            y1_control_point,
            y2_control_point
            ):
        """ . """

        y1 = self.y1_range
        y2 = self.y2_range

        if y1[1] - y1[0] != y2[1] - y2[0]:
            inverted = True
        else:
            inverted = False

        # If the control point is None we set to 0 (straight line)
        y1_cp = y1_control_point if y1_control_point is not None else 0
        y2_cp = y2_control_point if y2_control_point is not None else y1_cp

        if y1_control_point is not None and \
                y2_control_point is None and \
                inverted:
            y2_cp *= -1

        length_a = self.transform_ax1.transform([x1_start, 0]) - \
                   self.transform_ax2.transform ([x2_start + x2_length, 0])
        width_a = self.figure.transFigure.inverted().transform(
            np.absolute(length_a)
            )[0]
        width_a *= 1 + self.control_point_offset

        length_b = self.transform_ax1.transform([x1_start + x1_length, 0]) - \
                   self.transform_ax2.transform ([x2_start, 0])
        width_b = self.figure.transFigure.inverted().transform(
            np.absolute(length_a)
            )[0]
        width_b *= 1 - self.control_point_offset

        codes = np.array([
            Path.MOVETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ])

        path = np.array([
            self.transform_ax1.transform([x1_start, y1[1]]),
            self.transform_ax1.transform([x1_start, y1[1] + y1_cp * width_a]),
            self.transform_ax2.transform(
                [x2_start + x2_length, y2[1] + y2_cp * width_a]
                ),
            self.transform_ax2.transform([x2_start + x2_length, y2[1]]),
            self.transform_ax2.transform([x2_start + x2_length, y2[0]]),
            self.transform_ax2.transform([x2_start, y2[0]]),
            self.transform_ax2.transform([x2_start, y2[1]]),
            self.transform_ax2.transform([x2_start, y2[1] + y2_cp * width_b]),
            self.transform_ax1.transform(
                [x1_start + x1_length, y1[1] + y1_cp * width_b]
                ),
            self.transform_ax1.transform([x1_start + x1_length, y1[1]]),
            self.transform_ax1.transform([x1_start + x1_length, y1[0]]),
            self.transform_ax1.transform([x1_start, y1[0]]),
            self.transform_ax1.transform([x1_start, y1[1]]),
            self.transform_ax1.transform([x1_start, y1[0]]),
            ])

        if inverted:
            path[2:8] = path[2:8][::-1]

        path = np.apply_along_axis(
            self.figure.transFigure.inverted().transform,
            1,
            path
            )

        return path, codes
