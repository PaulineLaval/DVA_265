import random
from material_agent import MaterialAgent
from builder_agent import BuilderAgent

Builder_count = 3
Crossover_rate = 0.6
Mutation_rate = 0.05
Initial_funds = 1000000

def init_pop():
    return [BuilderAgent(Initial_funds) for _ in range(Builder_count)]

def evaluate_population(population):
    return [builder.CalculateFitness() for builder in population]

def select_parents(population, fitnesses):
    total_fitness = sum(fitnesses)
    if total_fitness == 0:
        return random.sample(range(len(population)), 2)  # Random selection if all fitnesses are zero
    
    # Roulette wheel selection
    selection_probs = [fitness / total_fitness for fitness in fitnesses]
    selected_indices = random.choices(range(len(population)), weights=selection_probs, k=2)
    return population[selected_indices[0]], population[selected_indices[1]]

def crossover(builder1: BuilderAgent, builder2: BuilderAgent):
    if random.random() < Crossover_rate:
        point = random.randint(0, len(builder1.BuildOrder) - 1)
        builder1.BuildOrder = builder1.BuildOrder[:point] + builder2.BuildOrder[point:]
        builder2.BuildOrder = builder2.BuildOrder[:point] + builder1.BuildOrder[point:]
    return builder1, builder2


def Run():
    g=0
    population=init_pop()
    fitnesses = evaluate_population(population)
    print(fitnesses)
    material_agent = MaterialAgent()

    for g in range(5):
        if any(material_agent.Inventory[i] == 0 for i in range(len(material_agent.Inventory))):
            material_agent.Restock()
        #print(matAgent.Inventory)
        g += 1

        for i in range(len(population)//2):
            i1, i2 = select_parents(range(0, len(population)), fitnesses)
            population[i1], population[i2] = crossover(population[i1], population[i2])
            population[i1].Mutate(Mutation_rate)
            population[i2].Mutate(Mutation_rate)

        fitnesses = evaluate_population(population)
        
        buy = select_parents(range(0, len(population)), fitnesses)
        for i in buy:
            population[i].TryToBuy(material_agent)

        print(f"----GEN: {g}----")
        for i in range(len(population)):
            print(population[i].BuildOrder)
            print(population[i].Fitness)
            print(population[i].funds)

# Run()


def simulate():
    material_agent = MaterialAgent()
    population = [BuilderAgent(100000) for _ in range(3)]
    
    for i in range(len(population)):
        population[i].runOrder()
        population[i].TryToBuy(material_agent)
        population[i].runOrder()


    gen=0
    simulation_time=3

    for g in range(5):
        if any(material_agent.Inventory[i] == 0 for i in range(len(material_agent.Inventory))):
            material_agent.Restock()
        #print(matAgent.Inventory)
        g += 1


