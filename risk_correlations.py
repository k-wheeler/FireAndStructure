"""Correlations between building connectivity and Open Climate Risk building-level risk, by county."""

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display
from scipy.stats import spearmanr

#Connectivity attributes correlated with risk
CONNECTIVITY_COLS = ["degree_10", "degree_50", "mean_ssd", "clustering_coef"]


def correlate_connectivity_with_risk(nodes, county, risk_file, connectivity_cols=CONNECTIVITY_COLS,
                                     risk_col="rps_2047", max_plot_points=50_000):
    """Match a county's Open Climate Risk points to buildings and correlate risk with connectivity.

    Filters nodes to the county, matches each risk point to the building footprint it falls inside,
    averages risk_col per building, then shows Spearman correlations and scatter plots.

    Parameters
    ----------
    nodes : GeoDataFrame
        Buildings with footprint geometry, objectid, county and the connectivity_cols (e.g. nodes_filtered2).
    county : str
        County name as it appears in nodes["county"], e.g. "Mariposa".
    risk_file : str or Path
        Open Climate Risk GeoJSON of building points for the county.
    connectivity_cols : list of str
        Connectivity attributes to correlate with risk.
    risk_col : str
        Risk column in risk_file to correlate with.
    max_plot_points : int
        Counties with more matched buildings than this are randomly sampled for the scatter plots only.

    Returns
    -------
    county_matched : DataFrame
        One row per matched building (indexed by objectid) with the connectivity_cols and risk_col.
    correlations : DataFrame
        Spearman correlation, p-value and number of buildings for each connectivity attribute.
    """
    county_risk = gpd.read_file(risk_file).to_crs(nodes.crs)
    county_nodes = nodes[nodes["county"] == county]

    #Match each risk point to the building footprint it falls inside. Most points fall inside a footprint;
    #most of the rest are far from any footprint, so they are likely buildings that aren't in the graph
    matched = gpd.sjoin(
        county_risk[[risk_col, "geometry"]],
        county_nodes[["objectid", "geometry"]],
        how="inner",
        predicate="within",
    )
    #A few footprints contain more than one risk point (or overlap), so average risk per building
    building_risk = matched.groupby("objectid")[risk_col].mean()
    county_matched = county_nodes.set_index("objectid")[connectivity_cols].join(building_risk, how="inner")

    print(f"{county}: {len(county_nodes):,} buildings; {len(county_matched):,} matched to a risk point "
          f"({matched.index.nunique():,} of {len(county_risk):,} risk points used)")

    #Spearman (rank) correlation between each connectivity attribute and risk
    rows = []
    for col in connectivity_cols:
        valid = county_matched[[col, risk_col]].dropna()
        rho, p = spearmanr(valid[col], valid[risk_col])
        rows.append({"attribute": col, "spearman": rho, "p_value": p, "n_buildings": len(valid)})
    correlations = pd.DataFrame(rows).set_index("attribute")

    #Scatter plots; large counties are randomly sampled for plotting only (correlations use every building)
    plot_data = county_matched.sample(min(max_plot_points, len(county_matched)), random_state=0)
    fig, axes = plt.subplots(1, len(connectivity_cols), figsize=(4.5 * len(connectivity_cols), 4.5), squeeze=False)
    for ax, col in zip(axes.flat, connectivity_cols):
        ax.scatter(plot_data[col], plot_data[risk_col], s=5, alpha=0.3)
        ax.set_title(f"{col} (Spearman = {correlations.loc[col, 'spearman']:.2f})", fontsize=10)
        ax.set_xlabel(col)
        ax.set_ylabel(risk_col)
    sampled_text = f", {len(plot_data):,} plotted" if len(plot_data) < len(county_matched) else ""
    fig.suptitle(f"Building connectivity vs Open Climate Risk {risk_col}, {county} County "
                 f"({len(county_matched):,} matched buildings{sampled_text})")
    plt.tight_layout()
    plt.show()

    display(correlations.style.format({"spearman": "{:.2f}", "p_value": "{:.3g}", "n_buildings": "{:,}"}))
    return county_matched, correlations
