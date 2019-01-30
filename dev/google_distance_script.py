# -*- coding: utf-8 -*-

from sumo_tools import get_buildings, create_grid, crop_grid, add_nearest_point, create_destination_matrix

building = get_buildings('Lörrach , Baden-Württemberg, Germany')

grid_boundary = create_grid(building, 500, 500)

grid_cropped = crop_grid(building, grid_boundary)

grid_point = add_nearest_point(building, grid_cropped)

points = grid_point.set_geometry('nearest_point').geometry

destination_matrix = create_destination_matrix(points)
