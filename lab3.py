# Course : DVA-265 Artificial Intelligence
# Lab-03

import random
import time
import tracemalloc
from itertools import product

# Parameters -- was using those before applying for all the combinations
# Population_size = 50
# Individual_length = 50
# Num_generations = 150  # Assuming a number for termination and tracking
# Crossover_rate = 0.1 
# Mutation_rate = 0.03

pop_sizes = [20, 50, 100]
mutation_probs = [0.001, 0.03, 0.1]
crossover_probs = [0.4, 0.6, 0.8]
Individual_length = 50
Num_generations = 150 

# Fitness function: sum of 1s in the individual
def fitness_function(individual):
    return sum(individual)


# Create intitial population
def create_population(population_size):
    return [[random.randint(0, 1) for _ in range(Individual_length)] for _ in range(population_size)]

# Roulette wheel selection
def select_parents(population, fitnesses, Population_size):
    total_fitness = sum(fitnesses)
    selection_probs = [fitness / total_fitness for fitness in fitnesses]
    selected_indices = random.choices(range(Population_size), weights=selection_probs, k=2)
    return population[selected_indices[0]], population[selected_indices[1]]

# Crossover function : Single point crossover
def crossover(parent1, parent2, Crossover_rate):
    if random.random() < Crossover_rate:
        point = random.randint(1, Individual_length -1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    return parent1[:], parent2[:]

# Mutation function
def mutate(individual, Mutation_rate):
    return [gene if random.random() > Mutation_rate else (1 - gene) for gene in individual]


# Main genetic algorithm function
def genetic_algorithm(Population_size, Mutation_rate, Crossover_rate):
    population = create_population(Population_size)
    best_fitness = 0
    generation = 0

    # For performance tracking
    start_time = time.time()
    convergence_generation = None
    convergence_time = None

    tracemalloc.start()
    while best_fitness < Individual_length:
        fitnesses = [fitness_function(individual) for individual in population]
        best_fitness = max(fitnesses)
        best_individual = population[fitnesses.index(best_fitness)]

        # See the current best individual
        # print(f"Generation {generation}: Best fitness = {best_fitness}")

        if best_fitness == Individual_length and convergence_generation is None:
            convergence_generation = generation
            convergence_time = time.time() - start_time

        new_population = []
        # Select the next generation, crossover and mutate
        while len(new_population) < Population_size:
            parent1, parent2 = select_parents(population, fitnesses, Population_size)
            child1, child2 = crossover(parent1, parent2, Crossover_rate)
            child1 = mutate(child1, Mutation_rate)
            child2 = mutate(child2, Mutation_rate)
            
            # We have 4 individuals, need to add the best 2
            candidates = [parent1, parent2, child1, child2]
            candidates_fitness = [fitness_function(ind) for ind in candidates]

            best_indices = sorted(range(4), key=lambda i: candidates_fitness[i], reverse=True)[:2]
            new_population.extend([candidates[i] for i in best_indices])

            # Ensure the new population does not exceed the size
            if len(new_population) > Population_size:
                new_population = new_population[:Population_size]

        population = new_population 
        generation += 1

    total_time = time.time() - start_time
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return{
        "pop_size": pop_size,
        "mutation_prob": mutation_prob,
        "crossover_prob": crossover_prob,
        "generations": generation,
        "fitness": best_fitness,
        "time_sec": round(end_time - start_time, 4),
        "peak_memory_kb": round(peak / 1024, 2)
    }

    # print(f"Best individual: {best_individual} with fitness: {best_fitness}")
    # print("Total Time:", round(total_time, 2), "seconds")
    # if convergence_generation is not None:
    #     print(f"Convergence Generation: {convergence_generation}, Time: {round(convergence_time, 2)} seconds")
    # else:
    #     print("No convergence achieved within the specified generations.")



# Run the genetic algorithm
if __name__ == "__main__":
    all_combinations = product(pop_sizes, mutation_probs, crossover_probs)
    results = []

    print("---------Running Genetic Algorithm with different parameters:")
    
    for pop_size, mutation_prob, crossover_prob in all_combinations:
        result = genetic_algorithm(pop_size, mutation_prob, crossover_prob)
        results.append(result)
        print(f"[Pop={pop_size}, Mut={mutation_prob}, Cross={crossover_prob}] "
              f"→ Gen: {result['generations']} | Fit: {result['fitness']} | "
              f"Time: {result['time_sec']}s | Mem: {result['peak_memory_kb']} KB")