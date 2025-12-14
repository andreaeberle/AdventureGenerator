"""
Creature Manager Class
"""

import numpy as np
from .Creature import *

class CreatureManager:
    
    def __init__(self, all_creature_dicts):
        
        self.all_creatures = [] # List of all Creature objects
        
        # Converting creature dicts to Creature objects
        for creature in all_creature_dicts:
            oCreature = Creature(creature)
            self.all_creatures.append(oCreature)
            
    def assignSpreads(self, map_size):
        creature_spreads = {}
        for creature in self.all_creatures:
            creature_name = creature.getName()
            
            # Setting a random spread range based on the map size
            random_start = np.random.choice(range(map_size)) # Start at a random column
            random_size = np.random.choice(range(map_size)) # Pick a random size of the spread
            
            if random_start + random_size > map_size:
                random_end = (random_start + random_size) - map_size
            else:
                random_end = random_start + random_size
                
            # Add creature's spread to dict as a tuple
            creature_spreads[creature_name] = (random_start, random_end)
            
        return creature_spreads