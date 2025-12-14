"""
Plant Manager Class
"""

import numpy as np
from .Plant import *

class PlantManager:
    
    def __init__(self, all_flora_dicts):
        
        self.all_plants = [] # List of all Plant objects
        
        # Converting plant dicts to Plant objects
        for plant in all_flora_dicts:
            oPlant = Plant(plant)
            self.all_plants.append(oPlant)
            
    def assignSpreads(self, map_size):
        plant_spreads = {}
        for plant in self.all_plants:
            plant_name = plant.getName()
            
            # Setting a random spread range based on the map size
            random_start = np.random.choice(range(map_size)) # Start at a random column
            random_size = np.random.choice(range(map_size)) # Pick a random size of the spread
            
            if random_start + random_size > map_size:
                random_end = (random_start + random_size) - map_size
            else:
                random_end = random_start + random_size
                
            # Add plant's spread to dict as a tuple
            plant_spreads[plant_name] = (random_start, random_end)
            
        return plant_spreads