"""
Creature Class
"""

class Creature:
    
    def __init__(self, creature_dict):
        
        self.keys = list(creature_dict.keys())
        
        self.name = self.keys[0] # Setting creature name
        
        self.creature_dict = creature_dict[self.name] # Pulling out creature dict
        
        # Pulling out list of growth biomes
        self.habitat_biomes = self.creature_dict["habitat_biomes"] 
        
        
    def getName(self):
        return self.name
    
    def getHabitatBiomes(self):
        return self.habitat_biomes
