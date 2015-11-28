import numpy as np
from matplotlib import gridspec
from ticker import SeqFormatter

def compound_axis(
        cols,
        rows,
        gs,
        fig,
        xscaling=None,
        yscaling=None,
        ax_patch=False,
        **kwargs
        ):
    """ . """
    xlengths = np.array([abs(c[1] - c[0]) for c in cols])
    if xscaling is None:
        col_ratios = None
    elif isinstance(xscaling, int):
        xlengths = np.append(xlengths, xscaling - xlengths.sum())
        cols.append(None)
        col_ratios = xlengths / xscaling
    else:
        col_ratios = xscaling

    ylengths = np.array([abs(r[1] - r[0]) for r in rows if r is not None])
    if yscaling is None:
        row_ratios = None
    elif isinstance(yscaling, int):
        ylengths = np.append(ylengths, yscaling - ylengths.sum)
        rows.append(None)
        row_ratios = ylengths / yscaling
    else:
        row_ratios = yscaling

    sgs = gridspec.GridSpecFromSubplotSpec(
        nrows = len(rows),
        ncols = len(cols),
        subplot_spec=gs,
        height_ratios=row_ratios,
        width_ratios=col_ratios,
        **kwargs
        )

    axes = np.empty([len(rows), len(cols)], dtype=object)
    for i, row in enumerate(rows):
        for j, col in enumerate(cols):
            if col is None or row is None:
                axes[i, j] = None
                continue
            params = dict()
            if i > 0:
                params['sharex'] = axes[0, j]
            if j > 0:
                params['sharey'] = axes[i, 0]
            ax = fig.add_subplot(sgs[i, j], **params)
            ax.set_ylim(row)
            ax.set_xlim(col)
            ax.patch.set_fill(ax_patch)
            axes[i, j] = ax


    for ax in axes[0:-1].flatten():
        try:
            ax.tick_params(labeltop='on', labelbottom='off')
        except AttributeError:
            pass

    for ax in axes[1:-1].flatten():
        try:
            ax.tick_params(labeltop='off', labelbottom='off')
        except AttributeError:
            pass

    for ax in axes[:,1:].flatten():
        try:
            ax.tick_params(labelleft='off')
        except AttributeError:
            pass
    return axes
