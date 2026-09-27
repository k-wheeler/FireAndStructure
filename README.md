# FireAndStructure

## Data

The data used in this project are **not included in this repository**. The `Data/` folder is ignored by git; download the datasets below into it to run the notebook.

| Dataset | Source | License | How to get it |
|---|---|---|---|
| California structure graph (building nodes and edges) | Vibrant Planet Data Commons | CC BY-NC-SA 4.0 | Download manually from the [dataset page](https://www.vpdatacommons.org/datasets/ca-stucture-graph-data) |
| Wildfire risk components (burn probability, flame length probability) | Riley et al. 2025, USDA Forest Service Research Data Archive | Public domain | Download `RDS-2025-0006.zip` manually from the [archive page](https://www.fs.usda.gov/rds/archive/catalog/RDS-2025-0006) |
| County boundaries (2023 TIGER/Line) | U.S. Census Bureau | Public domain | Downloaded by the notebook |
| Ecoregions 2017 | RESOLVE | CC BY 4.0 | Downloaded by the notebook |
| Annual NLCD land cover (Collection 1.2) | U.S. Geological Survey / MRLC | Public domain | Downloaded by the notebook |
| NLCD Tree Canopy Cover (v2025.6) | USDA Forest Service | Public domain | Read remotely by the notebook |

### Attribution

**California structure graph data:**
© 2025 Vibrant Planet. Distributed by Vibrant Planet Data Commons. Licensed under CC BY-NC-SA 4.0.
https://www.vpdatacommons.org/datasets/ca-stucture-graph-data

**Wildfire risk components:**
Riley, Karin L.; Zimmer, Scott N.; Kodra, Evan; Grenfell, Isaac C.; Dillon, Gregory K.; Scott, Joe H.; Jaffe, Melissa R.; Olszewski, Julia H.; Vogler, Kevin C.; Finney, Mark A.; Short, Karen C.; Jolly, W. Matthew; Brittain, Stuart E.; Callahan, Michael N. 2025. Spatial datasets of probabilistic wildfire risk components for the conterminous United States (270m) for circa 2011 climate and projected future climate circa 2047. Updated 01 July 2025. Fort Collins, CO: Forest Service Research Data Archive. https://doi.org/10.2737/RDS-2025-0006
The originator notes these data are intended for national-scale strategic planning; applicability to smaller areas varies by location.

**Ecoregions:**
Dinerstein, E., et al. 2017. An Ecoregion-Based Approach to Protecting Half the Terrestrial Realm. *BioScience* 67(6): 534–545. https://doi.org/10.1093/biosci/bix014
Data: RESOLVE Ecoregions 2017, https://ecoregions.appspot.com/, licensed under CC BY 4.0.

**Land cover:** U.S. Geological Survey, Annual National Land Cover Database (NLCD), Collection 1.2. https://www.mrlc.gov

**Tree canopy cover:** USDA Forest Service, NLCD Tree Canopy Cover, version 2025.6. https://data.fs.usda.gov/geodata/rastergateway/treecanopycover/

**County boundaries:** U.S. Census Bureau, 2023 TIGER/Line Shapefiles: Counties. https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html

## License

- **Code** (`.py` files and the code in the notebooks) is licensed under the [MIT License](LICENSE).
- **Notebook outputs** (tables, figures, maps and printed data) are derived from the Vibrant Planet California structure graph data and are therefore licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), not MIT. They may be shared and adapted for noncommercial purposes only, with the attribution above, under the same license.
- The datasets themselves remain under their original licenses listed above.
