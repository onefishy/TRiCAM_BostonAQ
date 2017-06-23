import numpy as np
import pandas as pd
import datascience
from datascience.predicates import are
import shapely
from shapely.geometry import Polygon
from shapely.geometry import LineString


x = [ -71.20197, -70.96679]
y = [42.291441, 42.420578]
x_cell = 50
y_cell = 50


x_min = -71.20197
x_max = -70.96679
y_min = 42.291441
y_max = 42.420578

#Create ticks
x_s = np.linspace(x_min, x_max, x_cell + 1)
y_s = np.linspace(y_min, y_max, y_cell + 1)

#Create grid
x_coord, y_coord = np.meshgrid(x_s, y_s)


'''Function Description: given the x and y coordinates of a grid, turns each grid element into a polygon. I will move from left to right, bottom to top

Input: x-coords, y-coords is a list of lists of x and y coordinates for the grid

Output: a list of polygons, one for each grid '''

def make_polygon(x_coords, y_coords):
    polygons = []
    for a in range(0, len(x_coords[0])-1, 1):
        x = x_coord[0][a:a+2]
        #grabs each x-coordinate pair for each grid element
        for b in range(0, len(y_coords)-1, 1):
            grid = []
            #initiate list to store points for each grid element
            y = tuple([y[0] for y in y_coords[b:b+2]])
            #for each x-coordinate pair, get all corresponding y-coordinates
            for j in range(0, len(y)):
                grid.append((x[0], y[j]))
                grid.append((x[1], y[j]))
                #append grid points of polygon into the grid list 
                g= [grid[0]] + grid[2:4] + [grid[1]]
                #reorder for shapely's Polygon function to read
            polygon = Polygon(g)
            polygons.append(polygon)
        #turn grid into shapely polygon and append to polygon list
    return(polygons)

data_beg = []
data_end = []

begin_lat = exp["begin lat"]
begin_long = exp["begin long"]
end_lat = exp["end lat"]
end_long = exp["end long"]

for x in range(0,len(begin_lat)) :
    data_beg.append(tuple([begin_long[x], begin_lat[x]]))
    data_end.append(tuple([end_long[x], end_lat[x]]))

'''Function Description: turns two lists of beginning and end locations into linestring objects

Input: begin_lst and end_lst are tuples of the form (longitude, latitude). 

Output: list of linestring objects'''

def make_lines(begin_lst, end_lst):
        return ([LineString([begin_lst[i], end_lst[i]]) for i in np.arange(0, len(begin_lst), 1)])


'''Function Description: given the start and end points of a line and a full grid, tells how many grid elements the line go through 

Input: line is a linestring shapely object. grid is a list of latitude, longitude tuples detailing a rectangular grid

Output: integer representing the number of grids that line interests'''

def how_many(line, poly_list):
    grids_thru = 0
    for poly in poly_list:
        thru = poly.intersects(line)
        inside = poly.contains(line)
        if thru or inside:
            grids_thru += 1
    return (grids_thru)


lines = make_lines(data_beg, data_end)
polygons = make_polygon(x_coord, y_coord)

grids_thru = []
for i in lines:
    grids_thru.append(how_many(i, polygons))

d = {"begin": data_beg, "end": data_end, "grids through": grids_thru}
final = pd.DataFrame(data=d)