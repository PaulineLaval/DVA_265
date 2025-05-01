class MaterialAgent:
    def __init__(self):
        self.Inventory = [0,0,0,0,0,0,0]
        self.Prices = [2500,8500,3450,75000,2995,2350,8300]
        # 1. door, 2. outside-door, 3. window, 4. wall-module, 5. toilet-seat, 6. tab, 7. shower-cabin

    def Restock(self):
        self.Inventory = [100, 100, 100, 100, 100, 100, 100]