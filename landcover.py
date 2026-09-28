"""Summarize land cover rasters (NLCD land cover, tree canopy cover) in a neighborhood around each building."""

import numpy as np
import pandas as pd
import rasterio
from rasterio.windows import Window

# NLCD land cover classes grouped into broader cover types
NLCD_GROUPS = {
    "water":       [11, 12],          # open water, perennial ice/snow
    "developed":   [21, 22, 23, 24],  # developed open space, low, medium, high intensity
    "barren":      [31],
    "forest":      [41, 42, 43],      # deciduous, evergreen, mixed
    "shrub":       [52],
    "grassland":   [71],
    "agriculture": [81, 82],          # pasture/hay, cultivated crops
    "wetland":     [90, 95],          # woody, emergent herbaceous
}

# cover types counted as vegetation when picking each building's dominant vegetation
VEGETATION_GROUPS = ["forest", "shrub", "grassland", "agriculture", "wetland"]


def _neighborhood_offsets(radius_m, res):
    """Row/col offsets of the pixels whose centers are within radius_m of the center pixel."""
    r = int(np.ceil(radius_m / res))
    d_row, d_col = np.mgrid[-r:r + 1, -r:r + 1]
    inside = (d_row * res) ** 2 + (d_col * res) ** 2 <= radius_m ** 2
    return d_row[inside], d_col[inside], r


def _sample_neighborhoods(raster_path, points, radius_m, reducer, n_out, strip_rows=2048):
    """Apply reducer to the pixels around each point, reading the raster one strip of rows at a time.

    Reading in strips keeps memory low (a California-wide raster would be ~2 GB) and
    only reads the part of the raster that has buildings in it.
    """
    with rasterio.open(raster_path) as src:
        pts = points.to_crs(src.crs)
        # pixel row/col of each point
        cols, rows = ~src.transform * (pts.x.to_numpy(), pts.y.to_numpy())
        rows = np.floor(rows).astype(np.int64)
        cols = np.floor(cols).astype(np.int64)

        d_row, d_col, r = _neighborhood_offsets(radius_m, src.res[0])
        out = np.full((len(points), n_out), np.nan, dtype=np.float32)

        order = np.argsort(rows, kind="stable")
        sorted_rows = rows[order]
        for strip_start in range(sorted_rows[0], sorted_rows[-1] + 1, strip_rows):
            lo, hi = np.searchsorted(sorted_rows, [strip_start, strip_start + strip_rows])
            if lo == hi:
                continue
            idx = order[lo:hi]
            # window covering these points plus the neighborhood radius on every side
            row0 = strip_start - r
            col0 = cols[idx].min() - r
            window = Window(col0, row0, cols[idx].max() + r + 1 - col0, strip_rows + 2 * r)
            data = src.read(1, window=window, boundless=True, fill_value=src.nodata or 0)
            out[idx] = reducer(data, rows[idx] - row0, cols[idx] - col0, d_row, d_col)

    return out


def nlcd_cover_fractions(raster_path, points, radius_m=100):
    """Percent of each NLCD cover group within radius_m of each point.

    Parameters
    ----------
    raster_path : str
        NLCD land cover GeoTIFF (local path or GDAL virtual path).
    points : GeoSeries
        One point per building.
    radius_m : float
        Neighborhood radius in meters.

    Returns
    -------
    DataFrame indexed like points, with a pct_<group> column per group in NLCD_GROUPS,
    plus dominant_cover (group with the largest share) and dominant_vegetation
    (largest of VEGETATION_GROUPS, NaN if there is no vegetation nearby).
    """
    groups = list(NLCD_GROUPS)
    # lookup table from NLCD class code to group index; anything else (nodata) is -1
    lut = np.full(256, -1, dtype=np.int8)
    for i, group in enumerate(groups):
        lut[NLCD_GROUPS[group]] = i

    def reducer(data, rows, cols, d_row, d_col):
        counts = np.zeros((len(rows), len(groups)), dtype=np.uint16)
        n_valid = np.zeros(len(rows), dtype=np.uint16)
        point_idx = np.arange(len(rows))
        for dr, dc in zip(d_row, d_col):
            group_idx = lut[data[rows + dr, cols + dc]]
            valid = group_idx >= 0
            counts[point_idx[valid], group_idx[valid]] += 1
            n_valid += valid
        with np.errstate(invalid="ignore", divide="ignore"):
            return 100 * counts / n_valid[:, None]

    pct = _sample_neighborhoods(raster_path, points, radius_m, reducer, n_out=len(groups))
    cover = pd.DataFrame(pct, index=points.index, columns=[f"pct_{g}" for g in groups])

    has_data = cover.notna().all(axis=1)
    cover["dominant_cover"] = pd.Series(pd.NA, index=cover.index, dtype="str")
    cover.loc[has_data, "dominant_cover"] = cover.loc[has_data, [f"pct_{g}" for g in groups]].idxmax(axis=1).str[4:]

    veg_cols = [f"pct_{g}" for g in VEGETATION_GROUPS]
    has_veg = cover[veg_cols].sum(axis=1) > 0
    cover["dominant_vegetation"] = pd.Series(pd.NA, index=cover.index, dtype="str")
    cover.loc[has_veg, "dominant_vegetation"] = cover.loc[has_veg, veg_cols].idxmax(axis=1).str[4:]

    return cover


def mean_tree_canopy(raster_path, points, radius_m=100):
    """Mean percent tree canopy cover within radius_m of each point.

    Pixel values above 100 (nodata / not mapped) are ignored.

    Returns
    -------
    Series indexed like points (NaN where no valid pixels were found).
    """
    def reducer(data, rows, cols, d_row, d_col):
        total = np.zeros(len(rows), dtype=np.float32)
        n_valid = np.zeros(len(rows), dtype=np.uint16)
        for dr, dc in zip(d_row, d_col):
            values = data[rows + dr, cols + dc]
            valid = values <= 100
            total += np.where(valid, values, 0)
            n_valid += valid
        with np.errstate(invalid="ignore", divide="ignore"):
            return (total / n_valid)[:, None]

    canopy = _sample_neighborhoods(raster_path, points, radius_m, reducer, n_out=1)
    return pd.Series(canopy[:, 0], index=points.index, name="tree_canopy_pct")
