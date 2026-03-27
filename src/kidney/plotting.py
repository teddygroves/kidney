import numpy as np
from matplotlib import pyplot as plt


def plot_ppc(ax, idata, msts, ycol, xcol=None, groupcol=None):
    qlow, qhigh = (
        idata.posterior_predictive[ycol]
        .quantile([0.01, 0.99], dim=["chain", "draw"])
        .to_numpy()
    )
    plot_df = msts.with_columns(qlow=qlow, qhigh=qhigh)
    if groupcol is None:
        groupcol = "dummy"
        plot_df = plot_df.with_columns(dummy=1.0)
    if xcol is None:
        xcol = "index"
        plot_df = plot_df.sort(groupcol).with_row_index()
    for (groupname,), subdf in plot_df.group_by(groupcol, maintain_order=True):
        sct = ax.scatter(subdf[xcol], subdf[ycol], s=7, label=groupname)
        ax.vlines(
            subdf[xcol],
            subdf["qlow"],
            subdf["qhigh"],
            zorder=10,
            alpha=0.1,
            color=sct.get_facecolors()[-1],
        )
    ax.set(xlabel=xcol, ylabel=ycol)
    ax.legend(frameon=False)
    return ax


def forestplot(ax, ts, xlabel="Test statistic", qlow=0.025, qhigh=0.975):
    ylimlow, ylimhigh = ax.get_ylim()
    ytickys = np.linspace(ylimlow, ylimhigh, len(ts) + 2)
    ys = ytickys[1:-1]
    xlows = [np.quantile(t, qlow) for t in ts.values()]
    xhighs = [np.quantile(t, qhigh) for t in ts.values()]
    xmeans = [np.mean(t) for t in ts.values()]
    xbiggest = max(np.abs(xlows + xhighs)) + 0.1
    ax.set_xlim(-xbiggest, xbiggest)
    line_label = f"{qlow * 100}%-{qhigh * 100}% interquantile range"
    for i, (y, xlow, xhigh, xmean) in enumerate(zip(ys, xlows, xhighs, xmeans)):
        line = ax.hlines(
            y=y,
            xmin=xlow,
            xmax=xhigh,
            linewidth=2,
            label=line_label if i == 0 else "",
        )
        ax.plot(
            xmean,
            y,
            marker="o",
            color=line.get_colors()[0],
            label="posterior mean" if i == 0 else "",
        )
    ax.set_yticks(ytickys, [""] + list(ts.keys()) + [""])
    # az.plot_forest(ts, ax=ax, combined=True, textsize=12, linewidth=3, hdi_prob=0.95);
    ax.axvline(0.0, linestyle="--", color="black")
    ax.set(title="", xlabel=xlabel)
    ax.tick_params(axis="y", which="both", left=False, right=False)
    return ax


def forestplot_oz(ax, ts, xlabel="Test statistic", qlow=0.025, qhigh=0.975):
    ylimlow, ylimhigh = ax.get_ylim()
    ytickys = np.linspace(ylimlow, ylimhigh, len(ts) + 2)
    ys = ytickys[1:-1]
    xlows = [np.quantile(t, qlow) for t in ts.values()]
    xhighs = [np.quantile(t, qhigh) for t in ts.values()]
    xmeans = [np.mean(t) for t in ts.values()]
    xbiggest = max(np.abs(xlows + xhighs)) + 0.1
    ax.set_xlim(-xbiggest, xbiggest)
    line_label = f"{qlow * 100}%-{qhigh * 100}% interquantile range"
    colors = ['r' if 'fa/fa' in key and not 'fa/fa - fa/+' in key else 'k' for key in ts.keys()]
    for i, (y, xlow, xhigh, xmean, cl) in enumerate(zip(ys, xlows, xhighs, xmeans, colors)):
        line = ax.hlines(
            y=y,
            xmin=xlow,
            xmax=xhigh,
            linewidth=1.3,
            label=line_label if i == 0 else "",
            color=cl
        )
        ax.plot(
            xmean,
            y,
            marker="o",
            mew=0,
            ms=6,
            color=line.get_colors()[0],
            label="posterior mean" if i == 0 else "",
        )
    ax.set_yticks(ytickys, [""] + list(ts.keys()) + [""])
    # az.plot_forest(ts, ax=ax, combined=True, textsize=12, linewidth=3, hdi_prob=0.95);
    ax.axvline(0.0, linestyle="--", color="black", zorder=0)
    ax.set(title="", xlabel=xlabel)
    ax.tick_params(axis="y", which="both", left=False, right=False)
    return ax
