import numpy as np
import pandas as pd
import time
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from collections import Counter
import pickle
from collections import Counter
from matplotlib import pyplot as plt

def land_use_cat(pt, shapes, usage):
    point = Point(pt[0], pt[1]) 
    land_types = []
    for i in range(len(shapes)):
        if any([gon.contains(point) for gon in shapes[i]]):
            land_types.append(usage[i])
    return land_types

def parse(wkt_str):
    gon_list = wkt_str.replace('MULTIPOLYGON ', '').split('), (')
    
    polygons = []
    for gon in gon_list:
        if '), (' in gon:
            return np.nan
        else:
            polygons.append(Polygon(np.array([point.split() for point in gon.replace('(', '').replace(')', '').split(', ')]).astype(float)))
    return polygons

def test_pts(grid, shapes, usage):
    land_use_raster = []
    start = time.time()
    for i in range(len(grid)):    
        if i % 10 == 0:
            end = time.time()
            print 'iter:', i, ', time:', end - start
            start = end
        categories = []    
        for pt in grid[i]:
            categories = land_use_cat(pt, shapes, usage)
            categories += categories
        categories = Counter(categories)
        for key, value in categories.items():
            categories[key] = value * 1. / len(pts[2000])
            
        land_use_raster.append(dict(categories))
    return land_use_raster
    
#def parse_pts(pt):
#    return np.array([pair.replace('[', '').replace(']', '').split() for pair in pt[1:-1].split('\n')]).astype(float)
    
df_land_use = pd.read_csv('land_use_full.csv')
shapes = df_land_use['SHAPE'].apply(parse).values
usage = df_land_use['LU05_DESC'].values

#df_pts = pd.read_csv('Random_Points.csv', index_col=False)
#pts = df_pts['0'].apply(parse_pts)
#with open('correct_randpts.pkl', 'rb') as f:
#    pts = pickle.load(f)
pts = np.loaf('correct_randpts.npy')

land_use_raster = test_pts(pts, shapes, usage)

with open('land_use_raster.pkl', 'wb') as f:
    pickle.dump(land_use_raster, f)