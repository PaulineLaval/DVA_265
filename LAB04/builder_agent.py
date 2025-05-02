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
fitness_points = [50, 15, 1, 1, 1, 1, 1]
ComponentNames = ["House", "Floor", "Garret", "Hall", "Bedroom", "Bathroom", "LivingRoom"] # For printing purposes
RawMaterials = ["door", "outside-door", "window", "wall-module", "toilet-seat", "tab", "shower-cabin"] # For printing purposes


class BuilderAgent:
    def __init__(self,funds):
        self.Inventory = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.MissingItems = [0,0,0,0,0,0,0] # Missing raw materials, will try to buy those

        # Build plan for the agent
        # self.BuildOrder = [random.randint(0, 6) for _ in range(Individual_size)] # [1,1,3,4]
        self.BuildOrder = random.sample(range(7), 7)

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

    def TryToBuy(self, material_agent: MaterialAgent):
        for i in range(len(self.MissingItems)):
            if self.MissingItems[i] > 0 and material_agent.Inventory[i]>= self.MissingItems[i]:
                if self.funds >= material_agent.Prices[i] * self.MissingItems[i]:
                    self.funds -= material_agent.Prices[i] * self.MissingItems[i]
                    material_agent.Inventory[i] -= self.MissingItems[i]
                    self.Inventory[i] += self.MissingItems[i]
                    self.MissingItems[i] = 0
                    # print(f"----Builder has bought necessary {RawMaterials[i]} from the seller.")


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
