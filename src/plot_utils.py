import numpy as np
def truncate_colormap(cmapIn, minval=0.0, maxval=1.0, n=100):
    from matplotlib import colors
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmapIn.name, a=minval, b=maxval),
        cmapIn(np.linspace(minval, maxval, n)))
    return new_cmap

def gradientbars_sliced(bars, cmap):
    ax = bars[0].axes
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    
    for bar in bars:
        bar.set_zorder(1)
        bar.set_facecolor("none")
        x, y = bar.get_xy()
        w, h = bar.get_width(), bar.get_height()
        grad = np.linspace(y, y + h, 256).reshape(256, 1)
        ax.imshow(grad, extent=[x, x + w, y, y + h], aspect="auto", zorder=0, origin='lower',
                  vmin=ymin, vmax=ymax, cmap=cmap)
    ax.axis([xmin, xmax, ymin, ymax])
    
dictCoreSymbol = {
    "1cycle":"star",
    "spiro":"hourglass",
    "fused":"diamond-tall",
    "bridged":"x",
    "bridged&fused":"circle",
    "pyrrole":"hourglass",
}

dictHeteroColor = {
    "sulfur":"yellow",
     "oxygen":"red",
     "nitrogen":"green",
}