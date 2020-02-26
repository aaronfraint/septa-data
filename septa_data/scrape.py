"""
Summary of ``scrape.py``
------------------------

This module provides Python wrappers for the SEPTA APIs
listed here: http://www3.septa.org/hackathon/

"""

import requests
import pandas as pd
import geopandas as gpd
from typing import Union


def bus_stops_by_route(
        route_id: Union[str, int],
        output_epsg: Union[int, bool] = False
) -> gpd.GeoDataFrame:
    """
    Get all stops for a given route ID, and return as a geodataframe

    :param route_id: any valid SEPTA route ID as string or integer.
    :param output_epsg: if provided, transform projection before returning
    :return: ``geopandas.GeoDataFrame`` with stops as points
    """

    url = f"http://www3.septa.org/hackathon/Stops/{route_id}"
    response = requests.get(url)

    if response:
        df = pd.read_json(response.content)
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lng, df.lat))
        gdf.crs = "epsg:4326"

        if output_epsg:
            gdf = gdf.to_crs(output_epsg)

        return gdf

    else:
        print('API failed:', response.text)

        return None


if __name__ == "__main__":
    gdf = bus_stops_by_route(42)

    print(gdf.crs)
    print(gdf.shape)
