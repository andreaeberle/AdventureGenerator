"""
Plant Class
"""

class Plant:
    
    def __init__(self, plant_dict):
        
        self.keys = list(plant_dict.keys())
        
        self.name = self.keys[0] # Setting plant name
        
        self.plant_dict = plant_dict[self.name] # Pulling out plant dict
        
        # Pulling out list of growth biomes
        self.growth_biomes = self.plant_dict["growth_biomes"] 
        
        
    def getName(self):
        return self.name
    
    def getGrowthBiomes(self):
        return self.growth_biomes
