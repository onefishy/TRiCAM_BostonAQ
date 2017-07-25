import shapefile as shp
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from collections import Counter
%matplotlib inline

############################

def test_pt(x, y, shapes):
    '''
    tests for point (x, y) membership in array of polygons. returns indices of polygons
    containing (x, y)

    x: longitude
    y: latitude
    shapes: array or list of polygons
    '''
    point = Point(x, y)

    indices = []
    for i in range(len(shapes)):

        shape = shapes[i]
        if len(shape.parts) == 1:
            gon = Polygon(shape.points)
        else:
            gon = Polygon(shape.points[shape.parts[0]:shape.parts[1]])

        if gon.contains(point):
            indices.append(i)

    return indices

def sample_in_grid(pt, delta_x, delta_y, n):
    '''
    produces random samples inside grid centered at 'pt'. returns a zipped object
    of x, y coordinates

    pt: coordinate of center of grid in tuple form
    delta_x: change in longitude
    delta_y: change in latitude
    '''

    x_coords = np.random.uniform(pt[1] - delta_x, pt[1] + delta_x, size=n)
    y_coords = np.random.uniform(pt[0] - delta_x, pt[0] + delta_y, size=n)

    return zip(x_coords, y_coords)

def grid_LU_extract(grid, shapes, records):
    '''
    produces land use descriptions of a grid. returns a dictionary with keys land use types
    and values land use proportions

    grid: random points from a single grid
    shapes: array of polygons
    records: array of land use records corresponding to the polygons
    '''

    grid_LU = np.array([])

    i = 0
    for x, y in grid:
        out = i * 1. / len(grid) * 100
        sys.stdout.write("\r%d%%" % out)
        sys.stdout.flush()
        i += 1

        indices = test_pt(x, y, shapes)
        if len(indices) > 0:
            grid_LU = np.hstack((grid_LU, records[indices]))
        else:
            print x, y, 'empty'
    sys.stdout.write("\r%d%%" % 100)
    sys.stdout.flush()

    categories = Counter(grid_LU)
    for key, value in categories.items():
        categories[key] = value * 1. / len(grid_LU)

    return dict(categories)

############################

def get_state(state_name, aq_readings):
    state_readings = aq_readings[aq_readings['State Name'] == state_name]
    return state_readings, state_readings['County Name'].unique()

def get_county(county_name, duration, state_readings):
    county_readings = state_readings[(state_readings['County Name'] == county_name)]
    sites = county_readings[['Latitude', 'Longitude']].values
    site_keys = np.array([str(tup) for tup in sites]).reshape((len(sites), 1))
    county_readings = pd.concat((county_readings, pd.DataFrame(site_keys, columns=['Site_keys'], index=county_readings.index)), axis=1)

    contig_sites = np.ascontiguousarray(sites).view(np.dtype((np.void, sites.dtype.itemsize * sites.shape[1])))
    sites = np.unique(contig_sites).view(sites.dtype).reshape(-1, sites.shape[1])
    return county_readings, sites

def get_gis(shp_filename, dbf_filename):
    myshp = open("../EPA/LU_Data/" + shp_filename, "rb")
    mydbf = open("../EPA/LU_Data/" + dbf_filename, "rb")
    city_LU_shp = shp.Reader(shp=myshp, dbf=mydbf)

    shapes = city_LU_shp.shapes()
    records = np.array(city_LU_shp.records())[:, 1]

    return shapes, records


def get_LU(sites, county_readings, county_name, delta_x, delta_y, num_pts, shapes, records):
    LU = []

    for i, site in enumerate(sites):
        print '\t\tchecking site ', i, '...'

        grid = sample_in_grid(site, delta_x, delta_y, num_pts)
        LU.append(str(grid_LU_extract(grid, shapes, records)))

    LU_df = pd.DataFrame(np.array(LU).reshape((len(LU), 1)), columns=['LU'], index=[str(tup) for tup in sites])
    print LU_df

    county_total = county_readings.join(LU_df, on='Site_keys')

    county_total = county_total[county_total['LU'].apply(str).apply(len) > 2]

    county_total.to_csv('../EPA/' + county_name + '.csv', index=False) #Make sure you put in the right path and file name here!

############################

x = [ -71.20197, -70.96679]
y = [42.291441, 42.420578]
x_cell = 50
y_cell = 50
num_pts = 100
delta_x = abs(x[1] - x[0]) * 1. / x_cell
delta_y = abs(y[1] - y[0]) * 1. / y_cell

aq_readings = pd.read_csv('../EPA/annual_conc_by_monitor_2016.csv') #Make sure you put in the right path and file name here!

############################

state_name = 'Rhode Island' #specify your state, create a directory with your state's name

#that's all! the rest will run by itself!
state_readings, counties = get_state(state_name, aq_readings)

counties

for county in counties:
    print '\n********************'
    print county, ':'
    print '********************'

    county_readings, sites = get_county(county, duration, state_readings)

    grid_sites = np.abs(sites.astype(int))

    contig_sites = np.ascontiguousarray(grid_sites).view(np.dtype((np.void, grid_sites.dtype.itemsize * grid_sites.shape[1])))
    grids = np.unique(contig_sites).view(grid_sites.dtype).reshape(-1, grid_sites.shape[1])

    print county, ' spans ', len(grids), ' grids'

    for i, grid in enumerate(grids):
        round_to_even = lambda n: n if n % 2 == 0 else n - 1
        add_leading_0 = lambda n: '0' + n if len(n) < 3 else n
        file_name = 'g' + str(int(grid[0])) + add_leading_0(str(round_to_even(int(grid[1])))) + '/g' + str(int(grid[0])) + add_leading_0(str(round_to_even(int(grid[1]))))

        shp_filename = file_name + '.shp'
        dbf_filename = file_name + '.dbf'

        sites_in_grid = sites[(grid_sites[:, 0]  == grid[0]) & (grid_sites[:, 1]  == grid[1])]
        site_keys = [str(site) for site in sites_in_grid]
        readings_in_grid = county_readings[county_readings['Site_keys'].isin(site_keys)]

        print '\t', len(site_keys), ' sites in grid ', i

        shapes, records = get_gis(shp_filename, dbf_filename)

        county_name = state_name + '/' + county + str(i)
        get_LU(sites_in_grid, readings_in_grid, county_name, delta_x, delta_y, num_pts, shapes, records)

print '\n\nDone'
