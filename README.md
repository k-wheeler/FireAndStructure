# FireAndStructure

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
