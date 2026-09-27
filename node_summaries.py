"""Summary tables and histograms of node (building) attributes, overall or by group."""
#Note: some of the formatting improvements here were done by Claude Code, but they were decided on by Kathryn.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import Markdown, display

#Attributes plotted as histograms: bin width and x-axis label
HIST_SETTINGS = {
    "degree_10":       (1,   "Buildings within 10 m"),
    "degree_50":       (2,   "Buildings within 50 m"),
    "degree_100":      (5,   "Buildings within 100 m"),
    "clustering_coef": (0.1, "Clustering coefficient"),
    "mean_ssd":        (2,   "Mean separation distance (m)"),
    "min_ssd":         (2,   "Min separation distance (m)"),
}

#Attributes that get a table of summary stats per group
TABLE_COLS = ["degree_10", "degree_50", "clustering_coef", "mean_ssd"]


def _format_stats(stats):
    """Style a summary stats table: thousands separators, whole numbers for the counts."""
    float_cols = stats.select_dtypes("float").columns
    return stats.style.format("{:,.3f}", subset=float_cols, na_rep="").format("{:,}", subset=["count", "missing"])


def _median_after_mean(stats):
    """Rename describe()'s "50%" column to "median" and move it next to the mean."""
    stats = stats.rename(columns={"50%": "median"})
    stats.insert(stats.columns.get_loc("mean") + 1, "median", stats.pop("median"))
    return stats


def _decimal_places(values, max_places=6):
    """Number of decimal places the values are given to, ignoring trailing zeros.

    Returns the fewest places that every value can be rounded to without changing it,
    or "more than max_places" for values that aren't rounded (e.g. calculated distances).
    """
    values = values.dropna().to_numpy()
    for places in range(max_places + 1):
        #Small tolerance because values like 0.1 aren't stored exactly as floats
        if np.allclose(values, np.round(values, places), rtol=0, atol=1e-9):
            return str(places)
    return f"more than {max_places}"


def summarize_nodes(nodes, group_col=None, top_n=5):
    """Show summary tables and histograms of node attributes, overall or by group.

    Parameters
    ----------
    nodes : DataFrame or GeoDataFrame
        Node table with the columns in HIST_SETTINGS. clustering_coef must already be float.
    group_col : str, optional
        Column to group by, e.g. "county" or "ecoregion". None summarizes all nodes together.
    top_n : int
        Number of groups (those with the most nodes) to include in the histograms.

    Returns
    -------
    dict of DataFrames
        With no grouping: "summary", one row per attribute in HIST_SETTINGS.
        With a grouping: "counts" (nodes per group) plus one summary stats table per
        column in TABLE_COLS, one row per group.
    """
    tables = {}

    if group_col is None:
        by_text = "for all buildings"

        #One table with a row per attribute (column by column to avoid copying the data)
        cols = list(HIST_SETTINGS)
        summary = pd.DataFrame({col: nodes[col].describe() for col in cols}).T
        summary = _median_after_mean(summary)
        summary["count"] = summary["count"].astype(int)
        summary.insert(1, "missing", pd.Series({col: nodes[col].isna().sum() for col in cols}))
        summary.insert(2, "decimal_places", pd.Series({col: _decimal_places(nodes[col]) for col in cols}))
        tables["summary"] = summary

        display(Markdown(f"### Summary of all {len(nodes):,} buildings"))
        display(_format_stats(summary))

        masks = {"All buildings": np.ones(len(nodes), dtype=bool)}

    else:
        by_text = f"by {group_col}"
        groups = nodes[group_col]

        #Counts of nodes per group, largest first (nodes with no group show as NaN)
        counts = groups.value_counts(dropna=False).rename("n_nodes").to_frame()
        counts.index.name = group_col
        counts["percent"] = (100 * counts["n_nodes"] / len(nodes)).round(2)
        tables["counts"] = counts

        display(Markdown(f"### Number of nodes {by_text}"))
        display(counts.style.format({"n_nodes": "{:,}", "percent": "{:.2f}"}))

        #Summary stats per group, highest mean at the top
        grouped = nodes.groupby(groups, dropna=False, observed=True)
        for col in TABLE_COLS:
            stats = _median_after_mean(grouped[col].describe())
            stats["count"] = stats["count"].astype(int)
            # describe's count skips missing values, so the difference is the number missing
            stats.insert(1, "missing", grouped[col].size() - stats["count"])
            stats = stats.sort_values("mean", ascending=False)
            tables[col] = stats

            display(Markdown(f"### {col} {by_text} (sorted by mean)"))
            display(_format_stats(stats))

        #Histograms only for the groups with the most nodes
        top_groups = counts.index.dropna()[:top_n]
        masks = {group: (groups == group).to_numpy() for group in top_groups}

    #With several groups, overlay outlines and show each as a fraction of its own nodes
    #So groups of very different sizes can be compared
    compare = len(masks) > 1

    fig, axes = plt.subplots(2, 3, figsize=(15, 8))

    for ax, (col, (width, label)) in zip(axes.flat, HIST_SETTINGS.items()):
        values = nodes[col]
        # bins centered on multiples of the bin width, out to the column's max
        bins = np.arange(0, values.max() + 2 * width, width) - width / 2
        for group, mask in masks.items():
            group_values = values[mask].dropna()
            if compare:
                weights = np.full(len(group_values), 1 / max(len(group_values), 1))
                ax.hist(group_values, bins=bins, weights=weights, histtype="step", linewidth=1.5, label=group)
            else:
                ax.hist(group_values, bins=bins)
        ax.set_title(col)
        ax.set_xlabel(label)
        ax.set_ylabel("Fraction of group's buildings" if compare else "Number of buildings")

    if compare:
        axes.flat[0].legend(fontsize=8)
        fig.suptitle(f"Distributions {by_text}, {len(masks)} groups with the most nodes")
    else:
        fig.suptitle(f"Distributions {by_text}")

    plt.tight_layout()
    plt.show()

    return tables
