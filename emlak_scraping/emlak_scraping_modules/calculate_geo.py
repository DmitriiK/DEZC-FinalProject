import geopandas as gpd
from shapely.geometry import Point

from hepsiemlak_dwh import db_worker
from settings import MEDITERRANEAN_SEA_GEO_FILE, GEO_CLAUSE_TO_SEA_CODE


def get_meditterranean_sea():
    fpath = 'zip://' + MEDITERRANEAN_SEA_GEO_FILE  # os.path.join(os.getcwd(), MEDITERRANEAN_SEA_GEO_FILE)
    # print(f'{fpath=}')
    med_sea = gpd.read_file(fpath, encoding='utf-8')
    return med_sea


def get_geo_emlak(crs, geo_clause):
    dbw = db_worker()
    data = dbw.get_geo_data(geo_clause)
    print(f'{len(data)} of new records to calculate')
    gdf_emlak = gpd.GeoDataFrame(
        data,
        columns=["id", "Longitude", "Latitude"],
        geometry=[Point(x, y) for _, x, y in data],
        crs=crs,  # "EPSG:4326" WGS_1984# geografical
    )
    return gdf_emlak


def calc_geo(geo_clause, geo_code):
    gf_med_sea = get_meditterranean_sea()
    # '28B'
    med_sea = gf_med_sea[gf_med_sea['id'].isin([geo_code])]['geometry']  # .iloc[0]  
    # '28B'- Mediterranean Sea - Eastern Basin,'28h'
    gdf_emlak = get_geo_emlak(med_sea.crs, geo_clause)
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
    for c2s in GEO_CLAUSE_TO_SEA_CODE:
        gdf = calc_geo(geo_clause=c2s[0], geo_code=c2s[1])
        save_calulations(gdf)


if __name__ == '__main__':
    calc_and_save()
