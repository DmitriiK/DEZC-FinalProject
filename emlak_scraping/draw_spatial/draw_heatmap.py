from PIL import Image
import os
import math
import timeit
from datetime import datetime
import sys
import os

import numpy
import json
import geopandas as gp
import pandas as pnd
from shapely.geometry import Point

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from  emlak_scraping_modules.hepsiemlak_dwh import db_worker
from emlak_scraping_modules.calculate_geo import get_meditterranean_sea
from emlak_scraping_modules.settings import SPATIAL_INTERPOLATION_SITE_PATH


# set boundaries in

# CITI_NAME ='Antalya'
CITI_NAME ='Antalya'

if CITI_NAME =='Antalya':
    CITY_ID = 7
    MIN_LAT = 36.825
    MAX_LAT = 36.985
    MIN_LON = 30.572
    MAX_LON = 30.857
if CITI_NAME =='Izmir':
    CITY_ID = 35
    MIN_LAT = 38.328
    MAX_LAT = 38.545
    MIN_LON = 27.016
    MAX_LON = 27.272

# change these to change how detailed the generated image is
# (1000x1000 is good, but very slow)
MAX_X = 100
MAX_Y = 100

DRAW_DOTS = True
CALC_DATE =datetime.now()
# at what distance should we stop making predictions?
IGNORE_DIST = 0.01



def load_prices():
    dbw = db_worker()
    raw_prices = dbw.get_geo_data_for_spatial_interpolation(CITY_ID)
 
    slope, y_intercept = linear_regression([(bedrooms, rent) for (bedrooms, rent, lat, lon) in raw_prices])
    print("slope = %s" % slope)
    print("y intercept = %s" % y_intercept)
    x_intercept = -(y_intercept) / slope
    print("x intercept =", x_intercept)
    num_phantom_bedrooms = -x_intercept  # positive now

    # prices = [(rent / (bedrooms + num_phantom_bedrooms), lat, lon, bedrooms) for (bedrooms, rent, lat, lon) in raw_prices] comm dk
    prices = [(rent, lat, lon, bedrooms) for (bedrooms, rent, lat, lon) in raw_prices]
    return prices, num_phantom_bedrooms

  
def pixel_to_ll(x, y, long_first=False):
    delta_lat = MAX_LAT - MIN_LAT
    delta_lon = MAX_LON - MIN_LON

    # x is lon, y is lat
    # 0,0 is MIN_LON, MAX_LAT

    x_frac = float(x) / MAX_X
    y_frac = float(y) / MAX_Y

    lon = MIN_LON + x_frac * delta_lon
    lat = MAX_LAT - y_frac * delta_lat

    calc_x, calc_y = ll_to_pixel(lat, lon)

    if abs(calc_x - x) > 1 or abs(calc_y - y) > 1:
        print
        "Mismatch: %s, %s => %s %s" % (
            x, y, calc_x, calc_y)
    if long_first:
        return lon, lat
    else:
        return lat, lon


def ll_to_pixel(lat, lon):
    adj_lat = lat - MIN_LAT
    adj_lon = lon - MIN_LON

    delta_lat = MAX_LAT - MIN_LAT
    delta_lon = MAX_LON - MIN_LON

    # x is lon, y is lat
    # 0,0 is MIN_LON, MAX_LAT

    lon_frac = adj_lon / delta_lon
    lat_frac = adj_lat / delta_lat

    x = int(lon_frac * MAX_X)
    y = int((1 - lat_frac) * MAX_Y)

    return x, y


def linear_regression(pairs):
    xs = [x for (x, y) in pairs]
    ys = [y for (x, y) in pairs]

    A = numpy.array([xs, numpy.ones(len(xs))])
    w = numpy.linalg.lstsq(A.T, ys, rcond=None)[0]
    return w[0], w[1]


def distance_squared(x1, y1, x2, y2):
    return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)


def distance(x1, y1, x2, y2):
    return math.sqrt(distance_squared(x1, y1, x2, y2))


def greyscale(price):
    grey = int(256 * float(price) / 3000)
    return grey, grey, grey


def color(val, buckets):
    if val is None:
        return (255, 255, 255, 0)

    colors = [(255, 0, 0),
              (255, 91, 0),
              (255, 127, 0),
              (255, 171, 0),
              (255, 208, 0),
              (255, 240, 0),
              (255, 255, 0),
              (218, 255, 0),
              (176, 255, 0),
              (128, 255, 0),
              (0, 255, 0),
              (0, 255, 255),
              (0, 240, 255),
              (0, 213, 255),
              (0, 171, 255),
              (0, 127, 255),
              (0, 86, 255),
              (0, 0, 255),
              ]

    for price, color in zip(buckets, colors):
        if val > price:
            return color
    return colors[-1]


gaussian_variance = IGNORE_DIST / 2
gaussian_a = 1 / (gaussian_variance * math.sqrt(2 * math.pi))
gaussian_negative_inverse_twice_variance_squared = -1 / (2 * gaussian_variance * gaussian_variance)


def gaussian(prices, lat, lon, ignore=None):
    num, dnm, c = 0, 0, 0
    for price, plat, plon, _ in prices:
        if ignore:
            ilat, ilon = ignore
            if distance_squared(plat, plon, ilat, ilon) < 0.0001:
                continue

        weight = gaussian_a * math.exp(distance_squared(lat, lon, plat, plon) *
                                       gaussian_negative_inverse_twice_variance_squared)

        num += price * weight
        dnm += weight

        if weight > 2:
            c += 1

    # don't display any averages that don't take into account at least five data points with significant weight
    if c < 5:
        return None

    return num / dnm


def start():

    priced_points, num_phantom_bedrooms = load_prices()

    adjustments = calculate_adjustments(priced_points)

    prices = predict_prices(priced_points)

    buckets = calculate_buckets(prices)

    make_picture(adjustments, buckets, num_phantom_bedrooms, priced_points, prices)


def make_picture(adjustments, buckets, num_phantom_bedrooms, priced_points, prices):
    # color regions by price
    I = Image.new('RGBA', (MAX_X, MAX_Y))
    IM = I.load()
    for x in range(MAX_X):
        for y in range(MAX_Y):
            IM[x, y] = color(prices.get((x, y)), buckets)
    if DRAW_DOTS:
        for _, lat, lon, _ in priced_points:
            x, y = ll_to_pixel(lat, lon)
            if 0 <= x < MAX_X and 0 <= y < MAX_Y:
                IM[x, y] = (0, 0, 0)

    output_dir =f"{SPATIAL_INTERPOLATION_SITE_PATH}/{CITI_NAME}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir) # todo - need to check whether it works
    out_fname = f"{output_dir}/output.phantom.{MAX_X}" 
    I.save(out_fname + ".png", "PNG")
    with open(out_fname + ".metadata.json", "w") as outf:
        outf.write(json.dumps({
            "calc_date":CALC_DATE.strftime ('%d-%m-%y'),
            "num_phantom_bedrooms": num_phantom_bedrooms,
            "buckets": buckets,
            "n": len(priced_points),
            "adjustments": adjustments}))


def predict_prices(priced_points):
    "pricing all the points..."
    prices = {}
    gf = get_geo_frame()
    for ind, r in gf.iterrows():
        xys = r['xys']
        prices[xys] = gaussian(priced_points, r['lat'], r['lon'])
    return prices


def calculate_buckets(prices):
    # determine buckets
    # we want 18 buckets (17 divisions) of equal area
    all_priced_areas = [x for x in prices.values() if x is not None]
    all_priced_areas.sort()
    total_priced_area = len(all_priced_areas)
    buckets = []
    divisions = 17.0
    stride = total_priced_area / (divisions + 1)
    next_i = int(stride)
    error_i = stride - next_i
    for i, val in enumerate(all_priced_areas):
        if i == next_i:
            buckets.append(val)
            delta_i = stride + error_i
            next_i += int(delta_i)
            error_i = delta_i - int(delta_i)
    buckets.reverse()
    return buckets


def calculate_adjustments(priced_points):
    print
    "computing #bedroom adjustments..."
    # compute what the error would be at each data point if we priced it without being able to take it into account
    # do this on a per-bedroom basis, so that we can compute correction factors
    bedroom_categories = list(sorted(set(bedrooms for _, _, _, bedrooms in priced_points)))
    adjustments = {}
    for bedroom_category in bedroom_categories:
        total_actual, total_predicted = 0, 0
        for i, (price, plat, plon, bedroom) in enumerate(priced_points):
            if bedroom != bedroom_category:
                continue
            predicted_price = gaussian(priced_points, plat, plon, ignore=(plat, plon))

            if predicted_price:
                total_actual += price
                total_predicted += predicted_price

        if total_predicted == 0:  # we might not make any predictions, if we don't have enough data
            adjustment = 1.0
        else:
            adjustment = total_actual / total_predicted
        adjustments[bedroom_category] = adjustment
    return adjustments


def get_geo_frame():
    med_sea = get_meditterranean_sea()
    # mseb = med_sea[med_sea['id'] == '28B']  # .iloc[0]  # Mediterranean Sea - Eastern Basin
    xys = []
    for x in range(MAX_X):
        row = [(x, y) for y in range(MAX_Y)]
        xys.extend(row)
    lon_lat = [pixel_to_ll(*xy, True) for xy in xys]  # list of pairs (longitude, latitude)
    lst_lst = list(zip(*lon_lat))  # list of 2 lists, - first one is for long, second one - for lat
    df = pnd.DataFrame({'xys': xys,'lon': lst_lst[0], 'lat': lst_lst[1], 'coords': lon_lat})  #
    df['coords'] = df['coords'].apply(Point)
    points = gp.GeoDataFrame(df, geometry='coords', crs=med_sea.crs)
    # print(points)
    df2sea = gp.tools.sjoin(points, med_sea, predicate="within", how='left')
    df2sea.drop(df2sea[df2sea['index_right'] >= 0].index, inplace=True) # dropping rows related to the sea # pd.isna(np.nan)

    return df2sea[['xys', 'lon', 'lat']]


if __name__ == "__main__":
    # if len(sys.argv) != 2:        print("usage: python draw_heatmap.py apts.txt")
    # fname = sys.argv[1]
    timer = timeit.timeit(start, number=1)
    print(timer)