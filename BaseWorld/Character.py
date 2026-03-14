"""
Character Class
"""

import numpy as np
from .Race import *

class Character:
    
    def __init__(self, race, gender, height, weight, appearance = None, 
                  personality = None, abilities = None, skills = None, 
                  home = None):
        
        self.race = race
        self.gender = gender
        self.height = height
        self.weight = weight
        self.personality = personality
        
    def getHeight(self):
        return self.height
    
    def getHeightFtIn(self):
        height_feet = int(np.floor(self.height))
        height_inches = round(12 * (self.height - height_feet))
        if height_inches == 12:
            height_feet += 1
            height_inches = 0
        height_str = str(height_feet) + "'" + str(height_inches) + "\""
        return height_str
    
    def printCharacter(self):
        print("+++ Appearance +++")
        print("Race:", self.race)
        print("Gender:", self.gender)
        print("Height:", self.getHeightFtIn())
        print("Weight:", self.weight)
        
        print("+++ Personality +++")
        for trait in self.personality:
            print(trait + ": " + str(self.personality[trait]))
