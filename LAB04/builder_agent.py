import random
import math
from Parameters import *
from material_agent import MaterialAgent


class BuilderAgent:
    current_id = 0

    def __init__(self,funds):
        self._id = BuilderAgent.current_id
        BuilderAgent.current_id += 1

        self.Inventory = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.MissingItems = [0,0,0,0,0,0,0] # Missing raw materials, will try to buy those

        # Build plan for the agent : each of the 6 constructible elements ina random order at first
        self.BuildOrder = random.sample(range(7), 7)
        self.amount_to_build = [2] + [abs(math.floor(random.gauss(0, 2))) + 1  for _ in range(6)] #represents how many of each element we will try to build
        self.items_to_order = [0] * 7
        self.funds = funds
        self.houses = 0
        self.fitness = 0 # Fitness represents any new material build


    def get_fitness(self):
        return self.fitness

    def __repr__(self):
        return f'''INVENTORY: {self.Inventory}
                   BuildOrder: {self.BuildOrder}
                   MissingItems: {self.MissingItems}
                   Funds: {self.funds}
                   Fitness: {self.fitness}'''

    def getId(self):
        return self._id

    def mutation(self, mutation_rate):
        """a mutation changes the order of operations by "sliding" one of the elemnts to a random new place
            (the other elements stay in the same order relative to each other). It will also modify at random the amount
            of that element the builder will try to build at once"""
        if random.random() < mutation_rate:
            index_elmt_to_move = random.randint(0, len(self.BuildOrder) - 1)
            elmt = self.BuildOrder[index_elmt_to_move]
            new_position = random.randint(0, len(self.BuildOrder) - 1)
            self.BuildOrder.remove(elmt)
            self.BuildOrder = self.BuildOrder[:new_position] + [elmt] + self.BuildOrder[new_position:]
            if elmt != 0: #If the mutated element is not a house, we change the amount built (if it is a house, it stays at 2)
                self.amount_to_build[elmt] = abs(math.floor(random.gauss(0, 2))) + 1


    def order_materials(self, material_agent: MaterialAgent):
        estimated_remaining_funds = self.funds
        self.items_to_order = [-self.Inventory[material] for material in range(7)]
        for action in self.BuildOrder: #We will try to buy the components for each possible action, in order
            required_components = Components[action] #For each action, we try to buy the components required to execute it
            for material in range(len(required_components)):
                if material < 7 and required_components[material] > 0: #If it is for sale(index <7) and we want to buy it, we can try ordering it
                    #print("\n",material, required_components[material], end =" ")
                    for i in range(required_components[material]): #We try to buy as many as required
                        #print(f"elem {i}", end=" ")
                        if estimated_remaining_funds >= material_agent.Prices[material]:
                            #if it's possible to buy it, we order as many as we can, until the quantity we want to reach
                            amount_ordered = min(self.amount_to_build[material], (estimated_remaining_funds//material_agent.Prices[material]))
                            estimated_remaining_funds -= material_agent.Prices[material] * amount_ordered
                            self.items_to_order[material] += amount_ordered
        material_agent.orders[self.getId()] = self.items_to_order
        #print(self.items_to_order)


    def swap_with(self, other_agent):
        # Try to swap a component I have extra of, for one I need
        for i in range(len(self.MissingItems)):
            if self.MissingItems[i] > 0:
                for j in range(len(self.Inventory)):
                    # If I have extra of item j, and the other has extra of item i
                    if self.Inventory[j] > 1 and other_agent.Inventory[i] > 1:
                        # Swap one unit
                        self.Inventory[j] -= 1
                        self.Inventory[i] += 1
                        other_agent.Inventory[j] += 1
                        other_agent.Inventory[i] -= 1
                        return True
        return False

    def print_build_order(self):
        for action in self.BuildOrder:
            print(ComponentNames[action], end=" ")
        print()

    def print_amount_constructed(self):
        print("amount of each component built per cycle: ", end="")
        for i in range(7):
            print(ComponentNames[i], ":", self.amount_to_build[i], end=", ")
        print()

    def construct(self):
        for action in self.BuildOrder:
            required_components = Components[action]

            #Check how many of it we can build
            amount_buildable = self.amount_to_build[action]
            for material in range(len(required_components)):
                if required_components[material] > 0:
                    amount_buildable = min(amount_buildable, self.Inventory[material]//required_components[material])

            #We build as many of the component as we can
            for material in range(len(required_components)):
                self.Inventory[material] -= required_components[material] * amount_buildable
            self.Inventory[action+7] += amount_buildable
            self.fitness += FitnessPoints[action] * amount_buildable
            if action == 0: self.houses += amount_buildable
            #print(f"{self.getId()} built {ComponentNames[action]}")