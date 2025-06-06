import random
from material_agent import MaterialAgent
from builder_agent import BuilderAgent
from Parameters import *


def init_pop():
    return [BuilderAgent(Initial_funds) for _ in range(Builder_count)]

def evaluate_population(population: list[BuilderAgent]):
    fitnesses = [agent.get_fitness() for agent in population]
    return fitnesses


def select_parents(population: list[BuilderAgent]):
    fitnesses = [agent.fitness for agent in population]
    total_fitness = sum(fitnesses)
    if total_fitness == 0:
        return random.sample(range(len(population)), 2)  # Random selection if all fitnesses are zero

    # Roulette wheel selection
    selection_probs = [fitness / total_fitness for fitness in fitnesses]
    selected_indices = random.choices(range(len(population)), weights=selection_probs, k=2)
    return population[selected_indices[0]].getId(), population[selected_indices[1]].getId()


def crossover(builder1: BuilderAgent, builder2: BuilderAgent):
    """If two builders crossover, on a specific placement in the list BuildOrder, they check which element is there for
    the other builder, and "slide" their correspondant element to the position. Ex: [1, 2, 3, 4] and [3, 2, 1, 4],
    where the 1st position is chosen : the first parent sees that 3 is in the 1st position of the second, and puts it
    first, to give [3, 1, 2, 4]. The second slides the 1 to the first position, giving [1, 3, 3, 4]"""


    to_swap = [] #List containing information about the places we decided to swap out
    #print("Crossover : ", builder1.BuildOrder, builder2.BuildOrder)


    for i in range(len(builder1.BuildOrder)):
        if random.random()<Crossover_rate:
            to_swap.append((i, builder1.BuildOrder[i], builder2.BuildOrder[i]))


    #print("Crossover : ", builder1.BuildOrder, builder2.BuildOrder)
    #print("swaps: ", to_swap)

    for elmt in to_swap:
        builder1.BuildOrder.remove(elmt[2])
        builder1.BuildOrder = builder1.BuildOrder[:elmt[0]] + [elmt[2]] + builder1.BuildOrder[elmt[0]:]
        builder2.BuildOrder.remove(elmt[1])
        builder2.BuildOrder = builder2.BuildOrder[:elmt[0]] + [elmt[1]] + builder2.BuildOrder[elmt[0]:]

    #print("Done, results : ", builder1.BuildOrder, builder2.BuildOrder)
    return builder1, builder2


def run_cycle(population: list[BuilderAgent], material_agent: MaterialAgent):
    """Each builder goes through their order of operations to choose what to order, then places their order with the
    material agent. The material agents then decides how to prioritise what it sells to who (here at random)
    Finally, the builder agents build as many elements as they can, following their BuildOrder"""

    for builder in population:
        #builder.printOrder()
        builder.order_materials(material_agent)

    material_agent.Restock()
    material_agent.sell(population)
    for builder in population:
        builder.construct()


def reinitialize_population(population: list[BuilderAgent]):
    for builder in population:
        builder.fitness = 0
        builder.houses = 0
        builder.funds = Initial_funds
        builder.Inventory = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]


def run():
    g = 0
    average_fitness_per_gen = []
    population = init_pop()
    material_agent = MaterialAgent()

    for g in range(Number_Generations):
        for _ in range(Cycles_Per_Generation):
            run_cycle(population, material_agent)

        # Iterating half, each time two parents are selected and crossover is performed on their buildOrder, rest properties are intact
        for i in range(len(population) // 2):
            i1, i2 = select_parents(population)
            population[i1], population[i2] = crossover(population[i1], population[i2])
            # population[i1].Mutate(Mutation_rate)
            # population[i2].Mutate(Mutation_rate)
            # For some reasons the above code was not able to identify the Mutate function. So called it separately
            agent1: BuilderAgent = population[i1]
            agent2: BuilderAgent = population[i2]
            agent1.mutation(Mutation_rate)
            agent2.mutation(Mutation_rate)
            population[i1] = agent1
            population[i2] = agent2

        # Try to swap material
        if g % 2 == 0:
            # Attempt to swap materials between agents
            for i in range(len(population)):
                for j in range(i + 1, len(population)):
                    population[i].swap_with(population[j])

        print(f"----GEN: {g}----")
        average_fitness = 0
        for i in range(len(population)):
            average_fitness += population[i].fitness
            print("\nbuilder n°", population[i].getId())
            print("order : ", population[i].BuildOrder)
            population[i].print_build_order()
            print("fitness :", population[i].fitness)
            print("funds : ", population[i].funds)
            print("number of houses built : ", population[i].houses)
            print("inventory : ", population[i].Inventory)
        average_fitness_per_gen.append(average_fitness / len(population))

        reinitialize_population(population)

    print(average_fitness_per_gen)


run()

