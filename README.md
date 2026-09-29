# FireAndStructure

An initial exploration of Vibrant Planet's [California structure graph](https://www.vpdatacommons.org/datasets/ca-stucture-graph-data), a network of about 13.6 million buildings in which buildings within 100 m of each other are connected, and how building connectivity relates to wildfire risk.

The exploration looks at:

- How much data there are and the general characteristics of the connectivity attributes (neighbor counts, clustering coefficient, separation distances), overall and by ecoregion and county
- How many buildings are in areas where building connectivity is likely to matter for fire spread: outside the Riley et al. (2025) wildland risk area and in areas with less than 10% tree canopy cover
- Whether building connectivity is correlated with county median family income and racial/ethnic minority percentage
- Whether building connectivity is already captured by CarbonPlan's [Open Climate Risk](https://carbonplan.org/research/climate-risk) building-level risk estimates (Mariposa, Shasta, and Sacramento counties)

## Key findings

- The neighbor counts (buildings within 10, 50, and 100 m) are strongly correlated with each other; the 50 m and 100 m counts are close to redundant (Spearman 0.94).
- Rural counties such as Mariposa have the highest average clustering coefficients and urban counties such as Los Angeles and San Francisco the lowest, because urban buildings have many neighbors spread far enough apart that they are not connected to each other.
- Of all buildings, 39% are outside the Riley et al. (2025) wildland risk area but within 500 m of it. After also removing buildings in areas with 10% or more tree cover, about 8.1 million buildings remain.
- Building connectivity is not strongly correlated with Open Climate Risk's 2047 risk estimates in the three counties examined (strongest Spearman correlation −0.41), and the direction differs between counties, suggesting connectivity could add information not already captured.
- About 102,000 buildings (0.75%) have no building ID or connectivity values. They are concentrated in rural counties and are likely buildings with no other buildings within 100 m.

These are first-pass results; see the notebook for details and caveats.

## Repository contents

| File | Description |
|---|---|
| [`Data_Exploration.ipynb`](Data_Exploration.ipynb) | Main notebook with the full exploration, figures, and notes |
| [`node_summaries.py`](node_summaries.py) | `summarize_nodes()`: summary tables, histograms, and correlation matrices of building attributes, overall or by a grouping such as county or ecoregion |
| [`landcover.py`](landcover.py) | `mean_tree_canopy()` (and `nlcd_cover_fractions()`): summarize land cover rasters in a neighborhood around each building, reading the raster in strips to limit memory |
| [`risk_correlations.py`](risk_correlations.py) | `correlate_connectivity_with_risk()`: match a county's Open Climate Risk building points to building footprints and correlate risk with connectivity |

## Setup

The code uses Python 3.12 with packages from conda-forge:

```bash
conda create -n firestructure -c conda-forge --strict-channel-priority python=3.12 geopandas pandas numpy pyarrow rasterio scipy shapely matplotlib notebook ipykernel
conda activate firestructure
```

Then start Jupyter from the repository folder and open `Data_Exploration.ipynb`:

```bash
jupyter notebook
```

## Running the notebook

1. Download the manual datasets listed under [Data](#data) into a `Data/` folder in the repository. The notebook uses `ca_vpdc_nodes.parquet` and `ca_vpdc_edges_0_10.parquet` from the structure graph, `RDS-2025-0006.zip` from Riley et al. (2025), and the Open Climate Risk county GeoJSON files.
2. Run the notebook from top to bottom. Later sections depend on variables created earlier (for example `points`, `counties`, and `nodes_filtered2`).
3. The other datasets are downloaded or read remotely the first time the notebook runs and are saved to `Data/` so later runs are faster: `ca_counties.gpkg`, `ca_ecoregions.gpkg`, `riley2025_BP_2011ClimateRun_CA.tif`, `nodes_filtered_tree_canopy_2025_100m.parquet`, and `ca_county_acs_2024.csv`. Delete a saved file to recalculate it.

Notes:

- The full node table is large (about 13.5 million building footprints), so the notebook needs a fair amount of memory; it was developed on a computer with 16 GB of RAM.
- The first tree canopy run reads the USFS tree canopy raster over the internet and can take a long time. The result is saved afterward.
- The tree canopy year (`veg_year`) and neighborhood radius (`radius_m`) are set at the top of the notebook.

## Data

The data used in this project are **not included in this repository**. The `Data/` folder is ignored by git; download the datasets below into it to run the notebook.

| Dataset | Source | License | How to get it |
|---|---|---|---|
| California structure graph (building nodes and edges) | Vibrant Planet Data Commons | CC BY-NC-SA 4.0 | Download manually from the [dataset page](https://www.vpdatacommons.org/datasets/ca-stucture-graph-data) |
| Wildfire risk components (burn probability, flame length probability) | Riley et al. 2025, USDA Forest Service Research Data Archive | Public domain | Download `RDS-2025-0006.zip` manually from the [archive page](https://www.fs.usda.gov/rds/archive/catalog/RDS-2025-0006) |
| Open Climate Risk building-level risk (per county) | CarbonPlan | ODbL (building-level data) | Download manually for each county from the [Open Climate Risk map](https://carbonplan.org/research/climate-risk?lat=38.49787&lng=-121.38365&zoom=9.58) (see below) |
| County boundaries (2023 TIGER/Line) | U.S. Census Bureau | Public domain | Downloaded by the notebook |
| Median family income and race/ethnicity by county (ACS 2020–2024 5-year, tables B19113 and B03002) | U.S. Census Bureau | Public domain | Downloaded by the notebook |
| Ecoregions 2017 | RESOLVE | CC BY 4.0 | Downloaded by the notebook |
| NLCD Tree Canopy Cover (v2025.6) | USDA Forest Service | Public domain | Read remotely by the notebook |

### Open Climate Risk county downloads

The notebook compares building connectivity with Open Climate Risk building-level risk (`rps_2047`) for individual counties. For each county:

1. Open the [Open Climate Risk map](https://carbonplan.org/research/climate-risk?lat=38.49787&lng=-121.38365&zoom=9.58) and navigate to the county.
2. Select the county in the **Risk in the region** section of the sidebar and download the building-level data.
3. Save it in `Data/` as `<County>-County-<FIPS>.geojson`. The notebook currently uses:
   - `Mariposa-County-06043.geojson`
   - `Shasta-County-06089.geojson`
   - `Sacramento-County-06067.geojson`

More about the data and methods: [Open Climate Risk documentation](https://open-climate-risk.readthedocs.io/en/stable/) and [explainer](https://carbonplan.org/research/climate-risk-explainer).

### Attribution

**California structure graph data:**
© 2025 Vibrant Planet. Distributed by Vibrant Planet Data Commons. Licensed under CC BY-NC-SA 4.0.
https://www.vpdatacommons.org/datasets/ca-stucture-graph-data

**Wildfire risk components:**
Riley, Karin L.; Zimmer, Scott N.; Kodra, Evan; Grenfell, Isaac C.; Dillon, Gregory K.; Scott, Joe H.; Jaffe, Melissa R.; Olszewski, Julia H.; Vogler, Kevin C.; Finney, Mark A.; Short, Karen C.; Jolly, W. Matthew; Brittain, Stuart E.; Callahan, Michael N. 2025. Spatial datasets of probabilistic wildfire risk components for the conterminous United States (270m) for circa 2011 climate and projected future climate circa 2047. Updated 01 July 2025. Fort Collins, CO: Forest Service Research Data Archive. https://doi.org/10.2737/RDS-2025-0006
The originator notes these data are intended for national-scale strategic planning; applicability to smaller areas varies by location.

**Open Climate Risk:**
CarbonPlan, Open Climate Risk. https://carbonplan.org/research/climate-risk. Building-level data licensed under the Open Database License (ODbL); see the [data access documentation](https://open-climate-risk.readthedocs.io/en/stable/access-data.html).

**Ecoregions:**
Dinerstein, E., et al. 2017. An Ecoregion-Based Approach to Protecting Half the Terrestrial Realm. *BioScience* 67(6): 534–545. https://doi.org/10.1093/biosci/bix014
Data: RESOLVE Ecoregions 2017, https://ecoregions.appspot.com/, licensed under CC BY 4.0.

**Tree canopy cover:** USDA Forest Service, NLCD Tree Canopy Cover, version 2025.6. https://data.fs.usda.gov/geodata/rastergateway/treecanopycover/

**County boundaries:** U.S. Census Bureau, 2023 TIGER/Line Shapefiles: Counties. https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html

**Income and race/ethnicity:** U.S. Census Bureau, American Community Survey 2020–2024 5-year estimates, tables B19113 (median family income) and B03002 (Hispanic or Latino origin by race). https://www.census.gov/programs-surveys/acs

## License

- **Code** (`.py` files and the code in the notebooks) is licensed under the [MIT License](LICENSE).
- **Notebook outputs** (tables, figures, maps and printed data) are derived from the Vibrant Planet California structure graph data and are therefore licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), not MIT. They may be shared and adapted for noncommercial purposes only, with the attribution above, under the same license. Outputs that use Open Climate Risk data also carry the Open Climate Risk attribution above.
- The datasets themselves remain under their original licenses listed above.
