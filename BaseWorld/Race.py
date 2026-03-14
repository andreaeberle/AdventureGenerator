# -*- coding: utf-8 -*-
"""
Race class
"""

"""
Ideas: 
    - Make weight more dependent on height.
    - Select an actual skin tone color from a color wheel.
    - Add sub-races.
    - Generate a hybrid race -- some traits from one race and some from another.
"""

import numpy as np


"""
The base for all races to be built out from.
"""
class Race():
    
    def __init__(self, race_dict):
        
        self.keys = list(race_dict.keys())
        
        self.name = self.keys[0] # Setting race name
        
        self.race_dict = race_dict[self.name] # Pulling out race dict
        
        self.appearance = self.race_dict["appearance"] # Pulling out appearance dict
        
        self.height_min = self.appearance["height_min"]
        self.height_max = self.appearance["height_max"]
        self.weight_ratio_min = self.appearance["weight_ratio_min"]
        self.weight_ratio_max = self.appearance["weight_ratio_max"]
        self.gender_options = self.appearance["gender"] # Pulling out gender dict

        
        #self.ability_modifiers = self.race_dict["ability_modifiers"] # Pulling out ability modifier dict
    
    def getRaceName(self):
        return self.name
        
    def setHeight(self):
        height = np.random.uniform(self.height_min, self.height_max)
        return height
    
    def setWeightRatio(self):
        weight_ratio = np.random.uniform(self.weight_ratio_min, self.weight_ratio_max)
        return weight_ratio
    
    def setGender(self):
        gender_value = np.random.randint(1,101)
        for gender_option in self.gender_options:
            gender_range = self.gender_options[gender_option] # Pulls out list of [min, max] range
            if gender_value >= gender_range[0] and gender_value <= gender_range[1]:
                gender = gender_option
        return gender
    
