import geopandas as gpd
from shapely.geometry import Point
import os
from  hepsiemlak_store import db_worker
MEDITERRANEAN_SEA_GEO_FILE = 'emlak_scraping/geo_data/iho.zip'

def get_meditterranean_sea():
    fpath = 'zip://' + os.path.join(os.getcwd(), MEDITERRANEAN_SEA_GEO_FILE)
    med_sea = gpd.read_file(fpath, encoding='utf-8')
    mseb = med_sea[med_sea['id'] == '28B']# .iloc[0]  # Mediterranean Sea - Eastern Basin
    pol = mseb['geometry'] 
    return pol

def get_geo_emlak(crs):
    dbw = db_worker()
    data=dbw.get_geo_data()
    gdf_emlak = gpd.GeoDataFrame(
    data,
    columns=["ID", "Longitude", "Latitude"],
    geometry=[Point(x, y) for _, x, y in data],
    crs=crs, # "EPSG:4326" WGS_1984# geografical
    )
    return gdf_emlak

def calc_geo():
    med_sea =get_meditterranean_sea()
    gdf_emlak=get_geo_emlak(med_sea.crs)
    proj_crs =32636 
    # WGS_1984_UTM_Zone_36N  https://pro.arcgis.com/en/pro-app/latest/help/mapping/properties/pdf/projected_coordinate_systems.pdf
    gdf_emlak=gdf_emlak.to_crs(proj_crs)
    med_sea = med_sea.to_crs(proj_crs)
    dist_series = gdf_emlak.distance(med_sea.iloc[0])
    gdf_emlak['distance_to_sea'] = dist_series
    # print(gdf_emlak)

if __name__ == '__main__':
   calc_geo()


