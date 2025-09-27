"""
Character Class
"""

import numpy as np
from .Race import *

class Character:
    
    def __init__(self, race, height, weight, home = None, appearance = None, 
                  personality = None, abilities = None, skills = None):
        
        self.race = race
        self.height = height
        self.weight = weight
        
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
        print(self.race)
        print(self.getHeightFtIn())
        print(self.weight)
