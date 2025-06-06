from xmlrpc.client import Fault

Builder_count = 20
Number_Generations = 100
Cycles_Per_Generation = 10
Crossover_rate = 0.6
Mutation_rate = 0.05
Initial_funds = 10000000

#Order used for the whole project of each type of component
# 0. door, 1. outside-door, 2. window, 3. wall, 4. toilet, 5. tab, 6. shower
# 7. house, 8. floor, 9. garret, 10. hall, 11. Bed_room, 12. bath_room, 13. living_room

#List indicating, for each constructible component, of the required components to build it
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


# The components we can build, rest of the components are in the inventory
Components = [House, Floor, Garret, Hall, Bedroom, Bathroom, LivingRoom]
FitnessPoints = [50, 10, 1, 1, 1, 1, 1]
ComponentNames = ["House", "Floor", "Garret", "Hall", "Bedroom", "Bathroom", "LivingRoom"] # For printing purposes
RawMaterials = ["door", "outside-door", "window", "wall-module", "toilet-seat", "tab", "shower-cabin"] # For printing purposes

