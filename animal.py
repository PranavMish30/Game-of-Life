import numpy as np

class Animal:
    def __init__(self, x, y, grid_size, gene_code=None):
        self.x = x
        self.y = y
        self.grid_size = grid_size  # Grid dimensions (width, height)
        
        self.input_size = 4  # Population density in 4 directions
        self.hidden_size = 2  # 2 hidden neurons
        self.output_size = 5  # 5 possible actions

        # If no gene code is provided, generate a random one
        if gene_code is None:
            self.gene_code = self.generate_gene_code()
        else:
            self.gene_code = gene_code
        
        # Decode gene code into weight matrices
        self.decode_gene_code()
    
    def __str__(self):
        return self.gene_code
        

    def generate_gene_code(self):
        """Generate a random gene code as a flattened weight matrix."""
        return np.random.uniform(-1, 1, size=(self.input_size * self.hidden_size + 
                                              self.hidden_size * self.output_size))

    def decode_gene_code(self):
        """Convert gene code into weight matrices."""
        input_to_hidden_size = self.input_size * self.hidden_size
        self.weights_input_hidden = self.gene_code[:input_to_hidden_size].reshape((self.hidden_size, self.input_size))
        self.weights_hidden_output = self.gene_code[input_to_hidden_size:].reshape((self.output_size, self.hidden_size))

    def get_population_density(self, grid):
        """Calculate population density in 4 directions (left, right, forward, backward)."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Left, Right, Backward, Forward
        densities = []

        for dx, dy in directions:
            count, blocks = 0, 0
            for i in range(1, 3):  # Vision range = 2 blocks
                nx, ny = self.x + dx * i, self.y + dy * i
                if 0 <= nx < self.grid_size[0] and 0 <= ny < self.grid_size[1]:  # Check within bounds
                    blocks += 1
                    count += len(grid[nx][ny])  # Count animals in that block
            densities.append(count / blocks if blocks > 0 else 0)  # Avoid division by zero

        return densities

    def think_and_act(self, grid):
        """Decide an action and move based on current state."""
        population_densities = self.get_population_density(grid)
        
        # Process inputs through neural network
        inputs = np.array(population_densities).reshape((self.input_size, 1))  # Ensure column vector
        hidden_activations = np.tanh(self.weights_input_hidden @ inputs)  # Hidden layer activation
        output_activations = self.weights_hidden_output @ hidden_activations  # Output layer
        
        action = np.argmax(output_activations)  # Choose action with highest activation
        self.move(action, grid)

    def move(self, action, grid):
        """Move the animal based on chosen action."""
        move_map = {
            0: (-1, 0),  # Move left
            1: (1, 0),   # Move right
            2: (0, 1),   # Move forward
            3: (0, -1),  # Move backward
            4: (0, 0)    # Do nothing
        }

        dx, dy = move_map[action]
        new_x, new_y = self.x + dx, self.y + dy

        # Ensure movement stays within grid bounds
        if 0 <= new_x < self.grid_size[0] and 0 <= new_y < self.grid_size[1]:
            grid[self.x][self.y].remove(self)  # Remove from old position
            self.x, self.y = new_x, new_y
            grid[self.x][self.y].append(self)  # Add to new position

# Example usage
grid_size = (5, 5)  # Define a 10x10 grid
grid = [[[] for _ in range(grid_size[1])] for _ in range(grid_size[0])]  # Each cell holds multiple animals

# Initialize animals at random positions
animals = [Animal(np.random.randint(0, 5), np.random.randint(0, 5), grid_size) for _ in range(5)]

# Place them in the grid
for animal in animals:
    grid[animal.x][animal.y].append(animal)


# Let each animal think and move
for animal in animals:
    animal.think_and_act(grid)



