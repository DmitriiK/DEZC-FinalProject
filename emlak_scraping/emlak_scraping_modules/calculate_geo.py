import geopandas as gpd
from shapely.geometry import Point


from  hepsiemlak_store import db_worker
from settings import MEDITERRANEAN_SEA_GEO_FILE


def get_meditterranean_sea():
    fpath = 'zip://' + MEDITERRANEAN_SEA_GEO_FILE # os.path.join(os.getcwd(), MEDITERRANEAN_SEA_GEO_FILE)
    # print(f'{fpath=}')
    med_sea = gpd.read_file(fpath, encoding='utf-8')
    return med_sea


def get_geo_emlak(crs):
    dbw = db_worker()
    data=dbw.get_geo_data()
    print(f'{len(data)} of new records to calculate')
    gdf_emlak = gpd.GeoDataFrame(
    data,
    columns=["id", "Longitude", "Latitude"],
    geometry=[Point(x, y) for _, x, y in data],
    crs=crs, # "EPSG:4326" WGS_1984# geografical
    )
    return gdf_emlak

def calc_geo():
    gf_med_sea = get_meditterranean_sea()
    med_sea = gf_med_sea [gf_med_sea['id'] == '28B']['geometry'] # .iloc[0]  # Mediterranean Sea - Eastern Basin
    gdf_emlak = get_geo_emlak(med_sea.crs)
    proj_crs = 32636 
    # WGS_1984_UTM_Zone_36N  https://pro.arcgis.com/en/pro-app/latest/help/mapping/properties/pdf/projected_coordinate_systems.pdf
    gdf_emlak = gdf_emlak.to_crs(proj_crs)
    med_sea = med_sea.to_crs(proj_crs)
    dist_series = gdf_emlak.distance(med_sea.iloc[0])
    gdf_emlak['dist_to_sea'] = dist_series
    # print(gdf_emlak)
    return gdf_emlak
    

def save_calulations(df):
    df = df[["id", "dist_to_sea"]]
    db_worker.save_calc_data(df)


def calc_and_save():
    gdf = calc_geo()
    save_calulations(gdf)
    

if __name__ == '__main__':
   calc_and_save()


