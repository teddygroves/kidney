import numpy as np
from matplotlib import pyplot as plt
import polars as  pl

# def plot_ppc(ax, idata, msts, ycol, xcol=None, groupcol=None):
#     qlow, qhigh = (
#         idata.posterior_predictive[ycol]
#         .quantile([0.01, 0.99], dim=["chain", "draw"])
#         .to_numpy()
#     )
#     plot_df = msts.with_columns(qlow=qlow, qhigh=qhigh)
#     if groupcol is None:
#         groupcol = "dummy"
#         plot_df = plot_df.with_columns(dummy=1.0)
#     if xcol is None:
#         xcol = "index"
#         plot_df = plot_df.sort(groupcol).with_row_index()
#     for (groupname,), subdf in plot_df.group_by(groupcol, maintain_order=True):
#         sct = ax.scatter(subdf[xcol], subdf[ycol], s=7, label=groupname)
#         ax.vlines(
#             subdf[xcol],
#             subdf["qlow"],
#             subdf["qhigh"],
#             zorder=10,
#             alpha=0.1,
#             color=sct.get_facecolors()[-1],
#         )
#     ax.set(xlabel=xcol, ylabel=ycol)
#     ax.legend(frameon=False)
#     return ax


def plot_ppc(
    ax, idata, msts, ycol,
    xcol=None, groupcol=None,
    separate_by=None, group_gap=0,
    linew=0.3,
):
    qlow, qhigh = (
        idata.posterior_predictive[ycol]
        .quantile([0.01, 0.99], dim=["chain", "draw"])
        .to_numpy()
    )

    plot_df = msts.with_columns(qlow=qlow, qhigh=qhigh)

    if groupcol is None:
        groupcol = "_dummy"
        plot_df = plot_df.with_columns(
            pl.lit("Data").alias(groupcol)
        )

    if separate_by is not None and xcol is not None:
        raise ValueError(
            "separate_by currently requires xcol=None"
        )

    if xcol is None:
        xcol = "_plot_x"

        sort_cols = (
            [separate_by, groupcol]
            if separate_by is not None
            else [groupcol]
        )
        plot_df = plot_df.sort(sort_cols)

        # Add horizontal spacing between groups
        if separate_by is not None:
            groups = plot_df[separate_by].to_list()
            offsets = []
            n_gaps = 0

            for i, group in enumerate(groups):
                if i > 0 and group != groups[i - 1]:
                    n_gaps += 1
                offsets.append(i + n_gaps * group_gap)

        else:
            offsets = list(range(len(plot_df)))

        plot_df = plot_df.with_columns(
            pl.Series(xcol, offsets)
        )

    # Plot observations and predictive intervals
    for (groupname,), subdf in plot_df.group_by(
        groupcol, maintain_order=True
    ):
        ax.vlines(
            subdf[xcol],
            subdf["qlow"],
            subdf["qhigh"],
            color="gray",
            alpha=0.35,
            lw=linew,
            zorder=1,
        )

        ax.scatter(
            subdf[xcol],
            subdf[ycol],
            s=7,
            label=str(groupname),
            zorder=3,
        )

    # Label separated groups on the x-axis
    if separate_by is not None:
        centers = []
        labels = []

        for (name,), subdf in plot_df.group_by(
            separate_by, maintain_order=True
        ):
            centers.append(
                (subdf[xcol].min() + subdf[xcol].max()) / 2
            )
            labels.append(str(name))

        ax.set_xticks(centers, labels)
        ax.set_xlabel(separate_by)
    else:
        ax.set_xlabel("" if xcol == "_plot_x" else xcol)

    ax.set_ylabel(ycol)

    if groupcol != "_dummy":
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
    # colors = ['k' if 'fa/fa' in key and not 'fa/fa - fa/+' in key else 'k' for key in ts.keys()]
    for i, (y, xlow, xhigh, xmean) in enumerate(zip(ys, xlows, xhighs, xmeans)):
        line = ax.hlines(
            y=y,
            xmin=xlow,
            xmax=xhigh,
            linewidth=1.3,
            label=line_label if i == 0 else "",
            color='k'
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
    # if sign_probs:
    #     # Annotate each line with P(statistic > 0)
    #     for y, xhigh, t in zip(ys, xhighs, ts.values()):
    #         ax.annotate(
    #             f"SP={np.mean(np.asarray(t) > 0):.2f}",
    #             (xhigh, y),
    #             xytext=(3, 0),
    #             textcoords="offset points",
    #             va="center",
    #             fontsize=6,
    #             annotation_clip=False,
    #         )

    if sign_probs:
        # Annotate each line with P(statistic is more extreme). "sign probability (SP), i.e. the posterior mass on one side of zero, or max(k, 1-k) where k is the proportion of samples where TS >0"
        for y, xhigh, xlow, t in zip(ys, xhighs, xlows, ts.values()):
            k = np.mean(np.asarray(t) > 0)
            sp = max([k, 1-k])
            x_annot = xhigh if k>.5 else xlow
            ha = 'left' if k>.5 else 'right'
            xytext = (2,0) if k>.5 else (-2,0)
            ax.annotate(
                f"{sp:.2f}",
                (x_annot, y),
                xytext=xytext,
                textcoords="offset points",
                va="center",
                ha=ha,
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
