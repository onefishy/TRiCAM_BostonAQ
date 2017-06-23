def gen_rand_pts(min_x, min_y, delta_x, delta_y, y_cell, x_cell, rand_num):
    ''' Inputs: latitude min, latitude max, longitude min, longitude max, number of x and y cells, number of random points
    Actions: First, it creates random points within the boundaries of a single cell. Then, it translates these random points
    to each cell.
    Outputs: a list of arrays of random points per cell '''
    #generate random points of a single cell
    rand_x_grid = np.random.uniform(min_x, min_x + delta_x, rand_num)
    rand_y_grid = np.random.uniform(min_y, min_y + delta_y, rand_num)
    old_grid_pts = np.array(list(zip(rand_x_grid, rand_y_grid)))
    
    list_of_pts = []  
    new_grid_pts = np.copy(old_grid_pts)
    
    for y_tick in range(y_cell):
        for x_tick in range(x_cell):
            new_grid_pts[:, 0] =  old_grid_pts[:, 0] + delta_x * x_tick #shift horizontally
            list_of_pts.append(np.copy(new_grid_pts))
        new_grid_pts[:, 1] += delta_y #shift vertically
    return list_of_pts


#Testing the function above
x = [ -71.20197, -70.96679]
y = [42.291441, 42.420578]
x_cell = 100
y_cell = 100
num_pts = 100
delta_x = abs(x[1] - x[0]) * 1. / x_cell
delta_y = abs(x[1] - x[0]) * 1. / y_cell

rand_pts = gen_rand_pts(x[0], y[0], delta_x, delta_y, x_cell, y_cell, num_pts)

np.save('correct_randpts', np.array(rand_pts))