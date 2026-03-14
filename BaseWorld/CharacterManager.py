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
            
        # Creating personality traits list
        self.personality_traits = ["adaptation", 
                                       "alturism",
                                       "ambition",
                                       "compliance",
                                       "compromise",
                                       "confidence",
                                       "emotional perception",
                                       "empathy",
                                       "expression",
                                       "general outlook",
                                       "honesty",
                                       "introvert/extrovert",
                                       "initiative",
                                       "loyalty",
                                       "openness of mind",
                                       "patience",
                                       "self assurance",
                                       "sense of humor",
                                       "spontaneity",
                                       "steadiness",
                                       "sociability",
                                       "social care",
                                       "trust"]
        
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
        gender = race.setGender()
        trans_roll = np.random.randint(1,101)
        if trans_roll == 100:
            gender = "trans " + gender
        
        # Generationg personality
        personality = {}
        personality_trait_range = 100
        
        coin_flip = np.random.randint(0,2)
        if coin_flip == 0:
            dominant_energy = "left"
        elif coin_flip == 1:
            dominant_energy = "right"
        else:
            print("something weird happened")
        print(dominant_energy)
        
        for trait in self.personality_traits:
            trait_value = round(np.random.uniform(0, personality_trait_range))
            
            # Check if trait value is consistent with dominant energy
            if dominant_energy == "left" and trait_value > 50:
                chance_to_flip = np.random.randint(0,2)
                if chance_to_flip == 1:
                    final_trait_value = 100 - trait_value
                else:
                    final_trait_value = trait_value
            elif dominant_energy == "right" and trait_value < 50:
                chance_to_flip = np.random.randint(0,2)
                if chance_to_flip == 1:
                    final_trait_value = 100 - trait_value
                else:
                    final_trait_value = trait_value
            else:
                final_trait_value = trait_value
            
            personality[trait] = final_trait_value
                    
        oCharacter = Character(race_name, gender, height, weight, personality=personality)
        self.all_characters.append(oCharacter)
        oCharacter.printCharacter()
        
        