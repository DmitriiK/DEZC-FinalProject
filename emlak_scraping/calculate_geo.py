from  hepsiemlak_store import db_worker
import geopandas as gpd
from shapely.geometry import Point
def calc_geo():
    dbw = db_worker()
    data=dbw.get_geo_data()
    gdf = gpd.GeoDataFrame(
    data,
    columns=["ID", "Longitude", "Latitude"],
    geometry=[Point(x, y) for _, x, y in data],
    crs="EPSG:4326",
)

    # Print the resulting GeoDataFrame
    print(gdf)

if __name__ == '__main__':
   calc_geo()


