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


def plot_ppc_multinomial(
    axes, idata, msts, categories, groupcol=None, colors=None
):
    """Posterior predictive check for a multinomial model, one ax per category.

    Observed and predicted counts are shown as fractions of each row's total.
    colors optionally maps each level of groupcol to a colour.
    """
    ycol = f"c({', '.join(categories)})"
    yrep = idata.posterior_predictive[ycol]
    frac_rep = yrep / yrep.sum(f"{ycol}_dim")
    qlow, qhigh = (
        frac_rep.quantile([0.01, 0.99], dim=["chain", "draw"])
        .transpose("quantile", "__obs__", f"{ycol}_dim")
        .to_numpy()
    )
    total = msts.select(categories).sum_horizontal()
    if groupcol is None:
        groupcol = "dummy"
        msts = msts.with_columns(dummy=1.0)
    for i, (ax, category) in enumerate(zip(axes, categories)):
        plot_df = msts.with_columns(
            frac=msts[category] / total, qlow=qlow[:, i], qhigh=qhigh[:, i]
        )
        plot_df = plot_df.sort(groupcol, "frac").with_row_index()
        for (groupname,), subdf in plot_df.group_by(groupcol, maintain_order=True):
            sct = ax.scatter(
                subdf["index"],
                subdf["frac"],
                s=7,
                label=groupname,
                color=None if colors is None else colors[groupname],
            )
            ax.vlines(
                subdf["index"],
                subdf["qlow"],
                subdf["qhigh"],
                zorder=10,
                alpha=0.3,
                color=sct.get_facecolors()[-1],
            )
        ax.set(title=category, xlabel="index", ylabel="fraction", ylim=(-0.05, 1.05))
    axes[0].legend(frameon=False)
    return axes


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


def forestplot_oz(
    ax, ts, xlabel="Test statistic", qlow=0.025, qhigh=0.975, sign_probs=False
):
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
    if sign_probs:
        # Annotate each line with P(statistic > 0)
        for y, xhigh, t in zip(ys, xhighs, ts.values()):
            ax.annotate(
                f"SP={np.mean(np.asarray(t) > 0):.2f}",
                (xhigh, y),
                xytext=(3, 0),
                textcoords="offset points",
                va="center",
                fontsize=6,
                annotation_clip=False,
            )
    ax.set_yticks(ytickys, [""] + list(ts.keys()) + [""])
    # az.plot_forest(ts, ax=ax, combined=True, textsize=12, linewidth=3, hdi_prob=0.95);
    ax.axvline(0.0, linestyle="--", color="black", zorder=0)
    ax.set(title="", xlabel=xlabel)
    ax.tick_params(axis="y", which="both", left=False, right=False)
    return ax


def set_symmetric_xlim(ax, ts, qlow=0.025, qhigh=0.975, pad=1.2):
    """Set x limits symmetric around zero that fit all intervals in ts."""
    biggest = max(np.abs(np.quantile(t, [qlow, qhigh])).max() for t in ts.values())
    ax.set_xlim(-pad * biggest, pad * biggest)
    return ax
