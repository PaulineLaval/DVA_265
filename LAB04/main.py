import random
from material_agent import MaterialAgent
from builder_agent import BuilderAgent

Builder_count = 4
Crossover_rate = 0.6
Mutation_rate = 0.05
Initial_funds = 1000000
Num_generations = 20


def init_pop():
    return [BuilderAgent(Initial_funds) for _ in range(Builder_count)]


def evaluate_population(population: list[BuilderAgent]):
    fitnesses = [agent.getFitness() for agent in population]
    return fitnesses


def select_parents(population: list[BuilderAgent], fitnesses):
    total_fitness = sum(fitnesses)
    if total_fitness == 0:
        return random.sample(range(len(population)), 2)  # Random selection if all fitnesses are zero

    # Roulette wheel selection
    selection_probs = [fitness / total_fitness for fitness in fitnesses]
    selected_indices = random.choices(range(len(population)), weights=selection_probs, k=2)
    return population[selected_indices[0]], population[selected_indices[1]]


# def crossover(builder1: BuilderAgent, builder2: BuilderAgent):
#     if random.random() < Crossover_rate:
#         point = random.randint(0, len(builder1.BuildOrder) - 1)
#         builder1.BuildOrder = builder1.BuildOrder[:point] + builder2.BuildOrder[point:]
#         builder2.BuildOrder = builder2.BuildOrder[:point] + builder1.BuildOrder[point:]
#     return builder1, builder2

def crossover(builder1: BuilderAgent, builder2: BuilderAgent):
    if random.random() < Crossover_rate:
        point1 = random.randint(0, len(builder1.BuildOrder) - 1)
        point2 = random.randint(0, len(builder1.BuildOrder) - 1)
        while point1 == point2:
            point2 = random.randint(0, len(builder1.BuildOrder) - 1)

        better_Agent = builder1 if builder1.Fitness > builder2.Fitness else builder2
        other_Agent = builder2 if better_Agent == builder1 else builder1

        desiredNumber1 = better_Agent.BuildOrder[point1]
        desiredNumber2 = better_Agent.BuildOrder[point2]

        for i in range(len(other_Agent.BuildOrder)):
            if other_Agent.BuildOrder[i] == desiredNumber1:
                x = other_Agent.BuildOrder[i]
                other_Agent.BuildOrder[i] = other_Agent.BuildOrder[point1]
                other_Agent.BuildOrder[point1] = x
            elif other_Agent.BuildOrder[i] == desiredNumber2:
                x = other_Agent.BuildOrder[i]
                other_Agent.BuildOrder[i] = other_Agent.BuildOrder[point2]
                other_Agent.BuildOrder[point2] = x
    return builder1, builder2


def crossover2(builder1: BuilderAgent, builder2: BuilderAgent):

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


def initializing(population: list[BuilderAgent], material_agent):
    for agent in population:
        agent.RunOrder()
        agent.TryToBuy(material_agent)
    fitnesses = evaluate_population(population)
    return fitnesses


def Run():
    g = 0
    population = init_pop()
    fitnesses = evaluate_population(population)
    print(fitnesses)
    material_agent = MaterialAgent()

    fitnesses = initializing(population, material_agent)  # To kick start things

    for g in range(Num_generations):
        if any(material_agent.Inventory[i] == 0 for i in range(len(material_agent.Inventory))):
            material_agent.Restock()
        # print(matAgent.Inventory)
        g += 1

        # Iterating half, each time two parents are selected and crossover is performed on their buildOrder, rest properties are intact
        for i in range(len(population) // 2):
            i1, i2 = select_parents(range(0, len(population)), fitnesses)
            population[i1], population[i2] = crossover2(population[i1], population[i2])
            # population[i1].Mutate(Mutation_rate)
            # population[i2].Mutate(Mutation_rate)
            # For some reasons the above code was not able to identify the Mutate function. So called it separately
            agent1: BuilderAgent = population[i1]
            agent2: BuilderAgent = population[i2]
            #agent1.Mutate(Mutation_rate)
            #agent2.Mutate(Mutation_rate)
            population[i1] = agent1
            population[i2] = agent2

        for _ in range(10):
            for agent in population:
                agent.RunOrder()


        fitnesses = evaluate_population(population)

        buy = select_parents(range(0, len(population)), fitnesses)
        for i in buy:
            population[i].TryToBuy(material_agent)

        # Try to swap material
        if g % 2 == 0:
            # Attempt to swap materials between agents
            for i in range(len(population)):
                for j in range(i + 1, len(population)):
                    population[i].swap_with(population[j])

        print(f"----GEN: {g}----")
        for i in range(len(population)):
            print(f"\nbuilder agent {i}")
            print(" order :", population[i].BuildOrder)
            print(" fitness:", population[i].Fitness)
            print(" funds :", population[i].funds)
            print(" inventory : ", population[i].Inventory)
            print(" number of houses :", population[i].house)


Run()
