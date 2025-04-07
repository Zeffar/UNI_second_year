import math
import numpy as np
import matplotlib.pyplot as plt
from random import randrange


class GeneticAlgorithm:
    def __init__(self, fitness_function, lower_bound, upper_bound, num_bits, population_size, mutation_probability, num_iterations, elitism_size=1):
        self.fitness_function = fitness_function
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.num_bits = num_bits
        self.population_size = population_size
        self.mutation_probability = mutation_probability
        self.num_iterations = num_iterations
        self.elitism_size = elitism_size  
        self.population = np.linspace(lower_bound, upper_bound, population_size)
        self.x_values = np.linspace(lower_bound, upper_bound, 100)
        self.true_fitness_curve = [fitness_function(x) for x in self.x_values]

    def calculate_num_bits(self, precision):
        return math.ceil(math.log2((self.upper_bound - self.lower_bound) * 10 ** precision))

    def compute_discretization(self):
        return (self.upper_bound - self.lower_bound) / (1 << self.num_bits)

    def encode(self, real_value):
        normalized_value = round(((real_value - self.lower_bound) / (self.upper_bound - self.lower_bound)) * ((1 << self.num_bits) - 1))
        return format(normalized_value, f'0{self.num_bits}b')

    def decode(self, binary_string):
        integer_value = int(binary_string, 2)
        step_size = self.compute_discretization()
        return self.lower_bound + integer_value * step_size

    def select_individual(self, fitness_values):
        total_fitness = sum(fitness_values)
        cumulative_fitness = np.cumsum(fitness_values)
        random_value = np.random.random()
        index = 0
        while cumulative_fitness[index] / total_fitness < random_value:
            index += 1
        return index

    def mutate_individual(self, individual, mutation_point):
        binary_representation = self.encode(individual)
        mutated_binary = self.mutate(binary_representation, mutation_point)
        return self.decode(mutated_binary)

    def crossover(self, individual_a, individual_b, crossover_point):
        binary_a = self.encode(individual_a)
        binary_b = self.encode(individual_b)

        new_binary_a = binary_a[:crossover_point] + binary_b[crossover_point:]
        new_binary_b = binary_b[:crossover_point] + binary_a[crossover_point:]

        new_individual_a = self.decode(new_binary_a)
        new_individual_b = self.decode(new_binary_b)

        return new_individual_a, new_individual_b

    def mutate(self, binary_string, mutation_point):
        mutated_binary = binary_string[:mutation_point] + ('1' if binary_string[mutation_point] == '0' else '0') + binary_string[mutation_point + 1:]
        return mutated_binary

    def run(self):
        # Compute initial fitness values
        fitness_values = [self.fitness_function(individual) for individual in self.population]

        # Plot initial population and fitness curve
        plt.plot(self.x_values, self.true_fitness_curve)
        plt.plot(self.population, fitness_values, 'o')
        plt.title('Initial Population')
        plt.show()

        for iteration in range(self.num_iterations):
            # Sort population by fitness (descending order)
            sorted_indices = np.argsort(fitness_values)[::-1]
            self.population = self.population[sorted_indices]
            fitness_values = [self.fitness_function(individual) for individual in self.population]

            # Implement elitism: Keep the best individuals
            elites = self.population[:self.elitism_size]

            # Select parents and create new population
            new_population = []
            for _ in range(self.population_size - self.elitism_size):
                parent_a_index = self.select_individual(fitness_values)
                parent_b_index = self.select_individual(fitness_values)

                # Crossover
                crossover_point = randrange(self.num_bits)
                child_a, child_b = self.crossover(self.population[parent_a_index], self.population[parent_b_index], crossover_point)
                new_population.extend([child_a, child_b])

            # Add elites to the new population
            new_population = list(elites) + new_population[:self.population_size - self.elitism_size]
            self.population = np.array(new_population)

            # Mutation
            for i in range(self.population_size):
                if np.random.random() < self.mutation_probability:
                    mutation_point = randrange(self.num_bits)
                    self.population[i] = self.mutate_individual(self.population[i], mutation_point)

            # Update fitness values
            fitness_values = [self.fitness_function(individual) for individual in self.population]

            # Plot population every 2 iterations
            if iteration % 2 == 0:
                plt.clf()
                plt.plot(self.x_values, self.true_fitness_curve)
                plt.plot(self.population, fitness_values, 'o')
                plt.title(f'Iteration {iteration + 1}')
                plt.show()


if __name__ == "__main__":
    def quadratic_function(x):
        return -1 * x * x + 4 * x - 1

    lower_bound, upper_bound = 1, 3
    num_bits = 20
    population_size = 100
    mutation_probability = 0.1
    num_iterations = 20

    ga = GeneticAlgorithm(
        fitness_function=quadratic_function,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        num_bits=num_bits,
        population_size=population_size,
        mutation_probability=mutation_probability,
        num_iterations=num_iterations
    )
    ga.run()
