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
    for b in range(0, len(y_coords)-1, 1):
        y = tuple([y[0] for y in y_coords[b:b+2]])
        #grabs each x-coordinate pair for each grid element
        for a in range(0, len(x_coords[0])-1, 1):
            grid = []
            x = x_coords[0][a:a+2]
            #initiate list to store points for each grid element
            #for each x-coordinate pair, get all corresponding y-coordinates
            for j in range(0, len(x)):
                grid.append((x[j], y[0]))
                grid.append((x[j], y[1]))
                g = [grid[0]] + grid[2:4] + [grid[1]] 
                #append grid points of polygon into the grid list 
            polygon = Polygon(g)
            polygons.append(polygon)
        #turn grid into shapely polygon and append to polygon list
    return(polygons)

polygons = make_polygon(x_coord, y_coord)

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

'''Function Description: given the start and end points of a line and a full grid, tells how many grid elements the line go through and which grids. Grids are assigned left to right, bottom to top, starting with the bottom left grid as grid 0  

Input: line is a linestring shapely object. grid is a list of latitude, longitude tuples detailing a rectangular grid

Output: tuple, first element is the number of grids the line interests, and the second element is a list of the grid numbers that line interests'''

def how_many(line, poly_list):
    grids_thru = 0
    polygon = []
    for poly in poly_list:
        thru = poly.intersects(line)
        inside = poly.contains(line)
        if thru or inside:
            grids_thru += 1
            index = poly_list.index(poly)
            polygon.append(index)
    return (grids_thru, polygon)

lines = make_lines(data_beg, data_end)

grids_thru = []
for i in lines:
    grids_thru.append(how_many(i, polygons))   

num_thru = []
which_thru = []
for i in grids_thru:
    num_thru.append(i[0])
    which_thru.append(i[1])


#in final data frame
d = {"begin name": beg
     , "end name": end
     , "begin": data_beg
     , "end": data_end
     , "num through": num_thru
     , "grids through": which_thru}

final_exp = pd.DataFrame(data=d)