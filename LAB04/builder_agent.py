import random
from material_agent import MaterialAgent

# 1. door, 2. outside-door, 3. window, 4. wall, 5. toilet, 6. tab, 7. shower
# 8. house, 9. floor, 10. garret, 11. hall, 12. Bed_room, 13. bath_room, 14. living_room

# For STRIPS like behaviour
# House components: 1 floor, 1 garret
House = [0,0,0,0,0,0,0,0,1,1,0,0,0,0]
# Floor components: 4 bedrooms, 2 bathrooms, 1 living room
Floor = [0,0,0,0,0,0,0,0,0,0,0,4,2,1]
# Bedroom components: 2 windows, 1 door,1 wall
Bedroom = [1,0,2,1,0,0,0,0,0,0,0,0,0,0]
# Bathroom components: 1 door, 1 toilet, 1 tab, 1 shower, 1 wall
Bathroom = [1,0,0,1,1,1,1,0,0,0,0,0,0,0]
# Living room components: 1 door, 3 window, 1 wall
LivingRoom = [1,0,3,1,0,0,0,0,0,0,0,0,0,0]
# Hall components: 1 outside-door, 1 window, 1 wall
Hall = [0,1,1,1,0,0,0,0,0,0,0,0,0,0]
# Garret components: 3 window, 1 door, 1 wall
Garret = [1,0,3,1,0,0,0,0,0,0,0,0,0,0]

# Our final goal is to build a house, so we need 1 house, 1 floor, 1 garret, 1 hall, 4 bedrooms, 2 bathrooms and 1 living room
Required_comps = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 4, 2, 1]

# The components we can build, rest of the components are in the inventory
Components = [House, Floor, Garret, Hall, Bedroom, Bathroom, LivingRoom]
fitness_points = [15,8,6,1,1,1,1]
ComponentNames = ["House", "Floor", "Garret", "Hall", "Bedroom", "Bathroom", "LivingRoom"] # For printing purposes
RawMaterials = ["door", "outside-door", "window", "wall-module", "toilet-seat", "tab", "shower-cabin"] # For printing purposes


class BuilderAgent:
    current_id = 0

    def __init__(self,funds):
        self._id = BuilderAgent.current_id
        BuilderAgent.current_id += 1

        self.Inventory = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.MissingItems = [0,0,0,0,0,0,0] # Missing raw materials, will try to buy those

        # Build plan for the agent
        # self.BuildOrder = [random.randint(0, 6) for _ in range(Individual_size)] # [1,1,3,4]
        self.BuildOrder = random.sample(range(7), 7)
        self.items_to_order = [0] * 7
        self.funds = funds
        self.house = 0 
        self.Fitness = 0 # Fitness represents any new material build
        
    
    def RunOrder(self):
        for action in self.BuildOrder:
            # Components[action] returns an array with 14 elements (from the 7 defined above)
            # House,.. Index 7-13 in the inventory but 0-6 in the components so we add 7 to the index
            # print(f"-----Step-{action} Builder is trying to build {ComponentNames[action]}")
            if self.TryToBuild(Components[action]) and self.Inventory[action+7] < Required_comps[action+7]:
                self.Inventory = [self.Inventory[i] - Components[action][i] for i in range(len(self.Inventory))] # Used materials are removed from the inventory
                self.Inventory[action+7] += 1 # New component build
                # print(f"-----Builder has built {ComponentNames[action]}.")

            
                if action == 0: # If we build a house, increase fitness by 1
                    self.house += 1
                    # print(f"------Builder has built a house. Total houses Built: {self.house}.")
                    self.Inventory[7]-= 1
                self.Fitness += fitness_points[action]

    def getFitness(self):
        return self.Fitness
    
    # component is a list of 14 elements 
    def TryToBuild(self, component):
        for i in range(len(component)):
            if self.Inventory[i] < component[i]:
                if i < 7:
                    self.MissingItems[i] = component[i] - self.Inventory[i]
                    # print(f"-----Builder is missing {self.MissingItems[i]} {RawMaterials[i]} to build {ComponentNames[self.BuildOrder[0]]}.")
                return False
        return True
    
    def Mutate(self, mutation_rate):
        for i in range(len(self.BuildOrder)):
            if random.random() < mutation_rate:
                self.BuildOrder[i] = random.randint(0, 6)

    def mutation(self, mutation_rate):
        if random.random() < mutation_rate:
            index_elmt_to_move = random.randint(0, len(self.BuildOrder) - 1)
            elmt = self.BuildOrder[index_elmt_to_move]
            new_position = random.randint(0, len(self.BuildOrder) - 1)
            self.BuildOrder.remove(elmt)
            self.BuildOrder = self.BuildOrder[:new_position] + [elmt] + self.BuildOrder[new_position:]

    def TryToBuy(self, material_agent: MaterialAgent):
        for i in range(len(self.MissingItems)):
            if self.MissingItems[i] > 0 and material_agent.Inventory[i]>= self.MissingItems[i]:
                if self.funds >= material_agent.Prices[i] * self.MissingItems[i]:
                    self.funds -= material_agent.Prices[i] * self.MissingItems[i]
                    material_agent.Inventory[i] -= self.MissingItems[i]
                    self.Inventory[i] += self.MissingItems[i]
                    self.MissingItems[i] = 0
                    # print(f"----Builder has bought necessary {RawMaterials[i]} from the seller.")

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
                            estimated_remaining_funds -= material_agent.Prices[material]
                            self.items_to_order[material] += 1
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


    def __repr__(self):
        return f'''INVENTORY: {self.Inventory}
                   BuildOrder: {self.BuildOrder}
                   MissingItems: {self.MissingItems}
                   Funds: {self.funds}
                   Fitness: {self.Fitness}'''

    def getId(self):
        return self._id

    def printOrder(self):
        for action in self.BuildOrder:
            print(ComponentNames[action], end=" ")
        print()

    def construct(self):
        for action in self.BuildOrder:
            required_components = Components[action]

            #Check if we have all the required components in the inventory
            possible = True
            for material in range(len(required_components)):
                if required_components[material] > self.Inventory[material]: possible = False

            #If we do, we build the component
            if possible:
                for material in range(len(required_components)):
                    self.Inventory[material] -= required_components[material]
                self.Inventory[action+7] += 1
                self.Fitness += fitness_points[action]
                if action == 0: self.house += 1
                #print(f"{self.getId()} built {ComponentNames[action]}")