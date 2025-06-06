import random
from Parameters import *

class MaterialAgent:
    def __init__(self):
        self.Inventory = [0,0,0,0,0,0,0]
        self.Prices = [2500,8500,3450,75000,2995,2350,8300]
        self.orders = [[0 for _ in range(7)] for _ in range(Builder_count) ]
        self.orders_by_material = [[0 for _ in range(Builder_count)] for _ in range(7) ]
        self.total_orders = [0] * 7

        # 1. door, 2. outside-door, 3. window, 4. wall-module, 5. toilet-seat, 6. tab, 7. shower-cabin

    def Restock(self):
        self.Inventory = [500, 500, 500, 500, 2000, 1000, 500]

    def reinitialize_orders(self):
        self.orders = [[0 for _ in range(7)] for _ in range(Builder_count) ]
        self.orders_by_material = [[0 for _ in range(Builder_count)] for _ in range(7) ]
        self.total_orders = [0] * 7

    def get_orders_by_element(self):
        for material in range(7):
            for builder in range(Builder_count):
                self.orders_by_material[material][builder] = self.orders[builder][material]
                self.total_orders[material] += self.orders[builder][material]

    def sell(self, pop):
        self.get_orders_by_element()
        for material in range(7):
            while self.total_orders[material] > 0 and self.Inventory[material] > 0:
                found = False
                while not found:
                    chosen_builder = random.randint(0, Builder_count-1)
                    if self.orders_by_material[material][chosen_builder] > 0:
                        found = True
                self.Inventory[material] -= 1
                pop[chosen_builder].funds -= self.Prices[material]
                pop[chosen_builder].Inventory[material] += 1
                self.orders_by_material[material][chosen_builder] -= 1
                self.total_orders[material] -= 1

        self.reinitialize_orders()
