
import random

def survive(row,column,array):
    aliveCount = 0
    neighbours = [array[row-1][column-1],array[row-1][column],array[row-1][column+1],array[row][column-1],array[row][column+1],array[row+1][column+1],array[row+1][column],array[row+1][column+1]]
    aliveCount = sum(neighbours)
    if aliveCount == 3:
        return 1
    elif aliveCount == 2:
        return array[row][column]
    elif aliveCount <= 1:
        return 0
    else:
        return 0 

def population(row,column,array):
    return sum(sum(row) for row in array)


def gol(totalGenDuration,rows,columns):
    simulationData = {}
    lifeGrid = [[0 for _ in range(columns)] for _ in range(rows)]
    nextLifeGrid = [[0 for _ in range(columns)] for _ in range(rows)]
    for i in range(rows):
        for j in range(columns):

            if i == 0 or i == (rows-1) or j == 0 or j == (columns-1):
                lifeGrid[i][j] = 0
            else:
                lifeGrid[i][j] = random.randint(0,1)


    for currentGenCount in range(totalGenDuration):

        simulationData[currentGenCount] = (lifeGrid,population(rows,columns,lifeGrid))
        
        '''
        print("Current Generation :",currentGenCount)
        print(lifeGrid)
        print(population(rows,columns,lifeGrid))
        '''

        for i in range(1,rows-1):
            for j in range(1,columns-1):
                nextLifeGrid[i][j] = survive(i,j,lifeGrid)
            
        lifeGrid = nextLifeGrid

    return simulationData
