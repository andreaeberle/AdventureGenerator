"""
Character Manager class.
"""

import numpy as np
from .Race import *
from .Character import *

class CharacterManager:

    def __init__(self, all_race_dicts):
        
        self.all_characters = [] # A list to contain all the world's characters.
        self.all_races = [] # List of all Race objects.
        
        # Converting race dicts to race objects
        for race in all_race_dicts:
            oRace = Race(race)
            self.all_races.append(oRace)
        
    def createCharacter(self, race_options = None, height = None, weight_ratio = None, home = None, appearance = None, 
                  personality = None, abilities = None, skills = None):
        
        if isinstance(race_options, Race):
            race = race_options
        elif isinstance(race_options, list):
            race = np.random.choice(race)
        else:
            race = np.random.choice(self.all_races)
        
        race_name = race.getRaceName()

        # Generating appearance
        height = race.setHeight()
        weight = round(height * race.setWeightRatio())
        
        oCharacter = Character(race_name, height, weight)
        self.all_characters.append(oCharacter)
        oCharacter.printCharacter()
        
        