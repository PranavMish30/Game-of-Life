import random
from copy import deepcopy

def survive(row, column, array):
    alive_count = 0
    rows, columns = len(array), len(array[0])
    
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue  # Skip the current cell
            neighbor_row, neighbor_col = row + i, column + j
            if 0 <= neighbor_row < rows and 0 <= neighbor_col < columns:
                alive_count += array[neighbor_row][neighbor_col]
    
    # Apply Game of Life rules
    if alive_count == 3:
        return 1
    elif alive_count == 2:
        return array[row][column]
    else:
        return 0

def population(array):
    return sum(sum(row) for row in array)

def gol(total_gen_duration, rows, columns):
    simulation_data = {}
    life_grid = [[0 for _ in range(columns)] for _ in range(rows)]
    
    # Initialize the grid
    for i in range(1, rows - 1):
        for j in range(1, columns - 1):
            life_grid[i][j] = random.randint(0, 1)
    
    # Run generations
    for current_gen_count in range(total_gen_duration):
        simulation_data[current_gen_count] = (deepcopy(life_grid), population(life_grid))
        
        next_life_grid = [[0 for _ in range(columns)] for _ in range(rows)]
        
        for i in range(1, rows - 1):
            for j in range(1, columns - 1):
                next_life_grid[i][j] = survive(i, j, life_grid)
        
        life_grid = next_life_grid
    
    return simulation_data
