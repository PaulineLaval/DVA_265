"""
Code for the LAB 3 of Artificial Intelligence 2,
Khalid Hasan Ador and Pauline Laval
"""


import random
import time

def evaluation_program(pop_size, tmax, fitness_func, crossover_rate, mutation_rate):
    start_time = time.time()
    num_genes = 50
    t = 0

    #initialization of pop : an array of each population at every generation.
    #The population at generation t is composed of an array of individuals, each modelised by an array of the form :
    # [dna, fitness]
    pop = [[[[random.randint(0,1) for _ in range(num_genes)], 0] for _ in range(pop_size)]]

    #Computing the fitness of each individual
    for ind in pop[0]:
        ind[1] = fitness_func(ind[0])

    #print_generation(pop, t)


    #Main loop creating each generation
    while (max(pop[t], key=lambda ind: ind[1])[1] != num_genes) and t < tmax:
        t += 1
        pop.append([])

        for _ in range(pop_size//2):
            #Selection of the parents that will be combined
            parent1 = select_one(pop[t-1])
            parent2 = select_one(pop[t-1])

            #creation o the offspring
            offspring1 = [[0]*num_genes, 0]
            offspring2 = [[0]*num_genes, 0]

            for i in range(num_genes):
                #Chossing at random if we switch the parents genes or not in the offspring
                switch = random.random() <= crossover_rate
                offspring1[0][i] = parent1[0][i] if not switch else parent2[0][i]
                offspring2[0][i] = parent1[0][i] if switch else parent2[0][i]

                #Choosing whether to have a mutation in each offspring
                mutation_o1 = random.random() <= mutation_rate
                mutation_o2 = random.random() <= mutation_rate
                if mutation_o1 : offspring1[0][i] = 1-offspring1[0][i]
                if mutation_o2: offspring2[0][i] = 1-offspring2[0][i]

            #Calculating the fitness of the offspring
            offspring1[1] = fitness_func(offspring1[0])
            offspring2[1] = fitness_func(offspring2[0])

            #Sorting the parents and offspring by their fitness to select which ones will go into the new generation
            sorted_group = sorted([parent1, parent2, offspring1, offspring2], key=lambda ind: ind[1], reverse=True)
            pop[t].append(sorted_group[0])
            pop[t].append(sorted_group[1])

        #print_generation(pop, t)
    total_time = time.time() - start_time
    print(f"population size : {pop_size}, mutation rate : {mutation_rate}, crossover rate : {crossover_rate} : number of generations {t}, max fitness : {max(pop[t], key=lambda ind: ind[1])[1]}, time : {round(total_time, 4)}")


def print_generation(pop, t):
    print(f"\nGeneration {t} : ")
    for i in range(len(pop[t])):
        print_ind(pop[t][i])
    print(f"max fitness of generation {t}:", max(pop[t], key=lambda ind: ind[1])[1])


def print_pop(pop_t):
    for i in range(len(pop_t)):
        print(pop_t[i])

def print_ind(ind):
    string = "dna :"
    for gene in ind[0]:
        string += str(gene)
    string += f", fitness = {ind[1]}"
    print(string)

def fitness_sum(dna):
    return sum(dna)

def select_one(pop_t):
    #Roulette wheel selection
    max = sum([ind[1] for ind in pop_t])
    pick = random.uniform(0, max)
    current = 0
    for ind in pop_t:
        current += ind[1]
        if current > pick:
            return ind

if __name__ == '__main__':
    #evaluation_program(50, 50, fitness_sum, 0.6, 0.03)
    for pop_size in [20, 50, 100]:
        for crossover_rate in [0.1, 0.3, 0.5]:
            for mutation_rate in [0.01, 0.03, 0.05, 0.1]:
                evaluation_program(pop_size, 150, fitness_sum, crossover_rate, mutation_rate)