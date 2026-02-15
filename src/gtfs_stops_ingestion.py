import zipfile
import pandas as pd
import geopandas as gpd


def load_gtfs_stops(zip_path, txt_filename, PROJECT_CRS):

    # Reading GTFS stops (stops.txt)
    assert zipfile.is_zipfile(zip_path)

    with zipfile.ZipFile(zip_path) as z:
        with z.open(txt_filename) as f:
            stops_df = pd.read_csv(
                f,
                sep=",",
                encoding="utf-8"
            )

    # Convert GTFS stops to geometry (project canonical CRS)
    stops_gdf = gpd.GeoDataFrame(
        stops_df,
        geometry=gpd.points_from_xy(
            stops_df["stop_lon"],
            stops_df["stop_lat"]
        ),
        crs=PROJECT_CRS
    )

    return stops_gdf
