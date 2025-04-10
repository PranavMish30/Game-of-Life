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

    def survive(self, grid, min_density=0.2, max_density=3.0):
        """Determine if the animal survives based on population density in its current cell."""
        current_density = len(grid[self.x][self.y])
        return min_density <= current_density <= max_density  # Survives if within bounds

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

    def mutate(self, mutation_rate=0.1):
        """Mutate the gene code by adding small random variations."""
        mutation_mask = np.random.rand(len(self.gene_code)) < mutation_rate  # Boolean mask for mutations
        mutation_values = np.random.normal(0, 0.1, size=len(self.gene_code))  # Small mutations from normal distribution
        mutated_gene_code = self.gene_code + mutation_mask * mutation_values  # Apply mutations selectively
        return mutated_gene_code

    def reproduce(self, mutation_rate=0.1, grid=None):
        """Create a new animal with a mutated gene code."""
        offspring_gene_code = self.mutate(mutation_rate)
        offspring = Animal(self.x, self.y, self.grid_size, gene_code=offspring_gene_code)
        if grid:
            grid[self.x][self.y].append(offspring)  # Add offspring to the grid
        return offspring  # Return the new animal instance


def simulate(grid_size=(10, 10), generations=10, steps_per_generation=10, min_density=0.2, max_density=3.0, reproduction_threshold=(1.0, 2.5)):
    """Run a simulation with specified generations, steps per generation."""
    # Create an empty grid
    grid = [[[] for _ in range(grid_size[1])] for _ in range(grid_size[0])]

    # Initialize animals
    animals = [Animal(np.random.randint(0, grid_size[0]), np.random.randint(0, grid_size[1]), grid_size) for _ in range(20)]

    # Place animals in the grid
    for animal in animals:
        grid[animal.x][animal.y].append(animal)

    # Run simulation for generations
    for generation in range(generations):
        print(f"Generation {generation + 1}")
        
        # Run steps for each generation
        for step in range(steps_per_generation):
            print(f"  Step {step + 1}")

            # Each animal thinks and acts
            for animal in animals:
                animal.think_and_act(grid)

        # After all steps, check survival and reproduction
        next_generation = []
        for animal in animals:
            if animal.survive(grid, min_density, max_density):
                next_generation.append(animal)  # Animal survives
            
                # Check reproduction conditions based on population density
                current_density = len(grid[animal.x][animal.y])
                if reproduction_threshold[0] <= current_density <= reproduction_threshold[1]:
                    next_generation.append(animal.reproduce(mutation_rate=0.2, grid=grid))  # Animal reproduces

        animals = next_generation  # Update population for next generation

        # Print population size after each generation
        print(f"    Population size: {len(animals)}")

# Run the simulation with default parameters
simulate()
