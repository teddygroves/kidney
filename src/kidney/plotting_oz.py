import numpy as np
import matplotlib.pyplot as plt

from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


VARIABLE_LABELS = dict(
    bfi_orig = "BFI (dim. less)",
    frequency = "Frequency (Hz)",
    power_norm = "Normalized power (dim. less)",
    blood_pressure = "Blood pressure (mmHg)"
)

def plot_var_vs_bloodpressure(data, var='bfi_orig', band=None, panel_size=2, **kwgs):
    """ Scatter plot `var` against blood pressure stored in `data` for
    each blood vessel. If `var` is `"power_norm"` or `"frequency"`, then
    `band` must be either `"canonical"` or `"lofreq"`.
    
    Parameters
    ----------
    
     - data : xr.Dataset
         Contains variable selected with `var`. Must contain variable `blood_pressure`
         
     - var : str
         Key to variable selected from `data`.
         
     - band : str, optional
         Required when `var` is not 'bfi_orig'. Can be 'canonical' or 'lowfreq'.
         
     - panel_size : float
         Determines figsize = (num_cols * panel_size, num_rows * panel_size).
         
     - kwgs : dict
         Keyword arguments passed to `plot_phase_trajectory`.
    
    Returns
    -------
     - figure
     - axes
    
    Notes
    -----
     - uses a dictionary `var_labels` to write meaningful y-axis label.
    
    """
    
    vessels = data.vessel.values
    n_vessels = len(vessels)

    # Approximately square grid
    ncols = int(np.ceil(np.sqrt(n_vessels)))
    nrows = int(np.ceil(n_vessels / ncols))

    fig, axes = plt.subplots(
        nrows,
        ncols,
        figsize=(panel_size * ncols, 
                 panel_size * nrows),
        sharex=True,
        sharey=True,
    )

    for ax, vessel_idx in zip(axes.flat, vessels):
        
        
        # ax.scatter(
        #     data.blood_pressure,
        #     data.sel(band=band, vessel=vessel_idx)[var] if band else data[var].sel(vessel=vessel_idx),
        #     s=10,
        #     alpha=0.6,
        # )
        
        plot_phase_trajectory(
            data.blood_pressure,
            data.sel(band=band, vessel=vessel_idx)[var] if band else data[var].sel(vessel=vessel_idx),
            figax=(fig, ax)
        )

        ax.set_title(f"Vessel {vessel_idx}")
        ax.grid(alpha=0.2)

    fig.supylabel(VARIABLE_LABELS[var])
    fig.supxlabel("Blood pressure (mmHg)")

    fig.tight_layout()
    
    return fig, axes

def plot_phase_trajectory(
    xdata,
    ydata,
    xlabel=None,
    ylabel=None,
    cmap="viridis",
    linewidth=2,
    marker_size=15,
    figsize=None,
    figax=None,
    add_colorbar=True
):
    """Plot a 2D trajectory with color indicating temporal direction."""

    xdata = np.asarray(xdata)
    ydata = np.asarray(ydata)

    if len(xdata) != len(ydata):
        raise ValueError("xdata and ydata must have the same length.")

    # Line segments between consecutive points
    points = np.column_stack([xdata, ydata]).reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Color according to time
    t = np.arange(len(xdata))
    norm = Normalize(t.min(), t.max())

    lc = LineCollection(
        segments,
        cmap=cmap,
        norm=norm,
        linewidth=linewidth,
    )
    lc.set_array(t)

    # Figure
    return_ = False
    if figax is None:
        fig, ax = plt.subplots(figsize=figsize)
        return_ = True
    else:
        fig, ax = figax

    ax.add_collection(lc)

    # Individual observations
    ax.scatter(
        xdata,
        ydata,
        c=t,
        cmap=cmap,
        norm=norm,
        s=marker_size,
        zorder=3,
    )

    ax.autoscale()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if add_colorbar:
        # Small colorbar inside the axis
        cax = inset_axes(
            ax,
            width="5%",
            height="30%",
            bbox_to_anchor=(0, -0.55, 0.97, 1),
            bbox_transform=ax.transAxes,
            borderpad=1,
        )

        cbar = fig.colorbar(lc, cax=cax, extend='max',extendfrac=0.2)
        cbar.set_label("Time", fontsize=10)
        cbar.set_ticks([])
        # cax.text(x=0.5, y=0.05, s='Early', rotation=90, color='w', transform=cax.transAxes, ha='center')
        # cax.text(x=0.5, y=0.95, s='Late', rotation=90, color='k', transform=cax.transAxes, ha='center', va='top')

    if return_:
        return fig, ax
    
    
    
###################################
###################################
###################################

# COLOR_BEFORE = 'royalblue'
# COLOR_AFTER = 'tomato'

# COLOR_CONTROL = '#567AE2'# '#1D4ED8' #'#008080' #'k'
# COLOR_DIABET = '#F97316' # '#FF6F61' #'tomato'

COLOR_CONTROL = '#567AE2'# '#1D4ED8' #'#008080' #'k'
COLOR_DIABET = '#F97316' # '#FF6F61' #'tomato'

# COLOR_MEAN = 'k'
# STEP_TREATMENT = 0.3 # Space between treatments (e.g., Baseline, Empa)
width_of_mean_bar = 0.3 # Half width of the horizontal bar showing the mean value

xlocs = {
    ('young', 'F'): 0,
    ('young', 'M'): 2,
    ('adult', 'F'): 1,
    ('adult', 'M'): 3,
}

kw = dict(rasterized=True, alpha=0.7, ms=3, between_rats=0.12)


def plot_dots(data, xloc=0, ax=None, color='r', markers=None, alpha=0.3, show_meansem=False, jitter=0, mew=0, mfc=None, rasterized=False, ms=None):
    
    if ax is None:
        f,ax = plt.subplots()
    
    xs = np.random.randn(data.size)*jitter + xloc
    
    if markers is None:
        markers = ['.']*data.size
        ax.plot(xs, data, ls='', marker='.', color=color, alpha=alpha, mew=0, ms=ms, rasterized=rasterized)
    else:
        if type(markers) == str:
            markers = [markers]*data.size
        for xi, di, mkr in zip(xs, data, markers):
            ax.plot(xi, di, ls='', marker=mkr, color=color, alpha=alpha, mew=mew, ms=ms, mfc=mfc, rasterized=rasterized)
    if show_meansem:
        ax.errorbar(xloc+0.2, y=data.mean(), yerr=data.std()/np.sqrt(len(data)), color=color, marker='o', mew=1.5)
        
        
def plot_dots_rat_columns(data, varname, xloc=0, ax=None, between_rats=0.1, **kw):
    """Plot dots grouped into columns by 'rat'"""
    
    if ax is None:
        f,ax = plt.subplots()
        
    n_rats = data['rat'].drop_duplicates().size
    rat_locs = np.arange(0, n_rats*between_rats, between_rats)
    rat_locs = (rat_locs - rat_locs.mean()) + xloc
    
    for x0, (rat, grp) in zip(rat_locs, data.groupby('rat')):
        plot_dots(grp[varname], xloc=x0, ax=ax, **kw)
        
def plot_panel(df, varname):
    f, axs = plt.subplots(1,2, figsize=(2.5,2), sharey=True)
    plt.subplots_adjust(wspace=0.1)

    for gtyp, ax in zip(['fa/+', 'fa/fa'], axs):
        grp = df[df.gtyp==gtyp]
        ax.set_title(gtyp)

        for k, x in grp.groupby(['age', 'sex']):
            plot_dots_rat_columns(x, varname=varname, xloc=xlocs[k], 
                                     color=COLOR_DIABET if gtyp=='fa/fa' else COLOR_CONTROL, 
                                     ax=ax, **kw)
            ax.plot([xlocs[k]-width_of_mean_bar, 
                     xlocs[k]+width_of_mean_bar], [x[varname].mean()]*2, color='k', lw=2)

    for ax in axs:
        ax.set_xticks(np.array(list(xlocs.values())), 
                      list(map(lambda x: ' '.join(x[::-1]), list(xlocs.keys()))),
                      rotation=45, ha='right', rotation_mode='anchor')
        ax.spines[['top', 'right']].set_visible(False) 
        ax.grid(axis='y', ls=':')
        
    return f, axs


kw_one_val = dict(rasterized=False, alpha=1, ms=7, jitter=0.02)
def plot_panel_one_val_per_rat(df, varname):
    
    f, axs = plt.subplots(1,2, figsize=(2.5,2), sharey=True)
    plt.subplots_adjust(wspace=0.1)

    for gtyp, ax in zip(['fa/+', 'fa/fa'], axs):
        grp = df[df.gtyp==gtyp]
        ax.set_title(gtyp)

        for k, x in grp.groupby(['age', 'sex']):
            plot_dots(x[varname], xloc=xlocs[k], 
                         color=COLOR_DIABET if gtyp=='fa/fa' else COLOR_CONTROL, 
                         ax=ax, **kw_one_val)
            ax.plot([xlocs[k]-width_of_mean_bar, 
                     xlocs[k]+width_of_mean_bar], [x[varname].mean()]*2, color='k', lw=2)

    for ax in axs:
        ax.set_xticks(np.array(list(xlocs.values())), 
                      list(map(lambda x: ' '.join(x[::-1]), list(xlocs.keys()))),
                      rotation=45, ha='right', rotation_mode='anchor')
        ax.spines[['top', 'right']].set_visible(False) 
        ax.grid(axis='y', ls=':')
        
    return f, axs


def plot_activity_fractions(
    out,
    figsize=(3, 2),
    jitter=0.1,
    bar_halfwidth=0.2,
    point_size=50,
    show_mean=True,
    ylabel='% of vessels per rat',
    ax=None,
):
    """Plot the fraction of vessels for each activity type."""

    if ax is None:
        _, ax = plt.subplots(figsize=figsize)

    if show_mean:
        n_total = out.n.sum().item()
        mn = out.groupby('activity_type').agg(n = ('n', 'sum'))/n_total

    xlabels = []

    for i, (typ, grp) in enumerate(
        out.groupby('activity_type', sort=False)
    ):
        n = len(grp)
        x = np.random.randn(n) * jitter + i
        y = grp['frac'] * 100
        ax.scatter(x, y, point_size, marker='.', lw=0)

        if show_mean:
            y_mean = mn.loc[typ].n.item() * 100
            ax.plot(
                [i - bar_halfwidth, i + bar_halfwidth],
                [y_mean] * 2,
                color='k',
                lw=3,
                zorder=0
            )
            xlabels.append(f"{typ}\n({y_mean:.1f}%)")
        else:
            xlabels.append(typ)

    ax.set_xticks(range(len(xlabels)), xlabels)
    ax.spines[['top', 'right', 'bottom']].set_visible(False)
    ax.set(ylabel=ylabel)

    return ax
