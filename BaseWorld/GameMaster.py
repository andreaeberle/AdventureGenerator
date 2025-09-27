"""
Game Master class.
"""

import os
import json
from .WorldManager import *
from .CharacterManager import *

class GameMaster:
    
    def __init__(self):
        
        self.master_folder_path = "/Users/ame94/.spyder-py3/AdventureGenerator"
        
    def startNewWorld(self):
        
        # Identify loadable worlds and select one.
        root, dirs, files = os.walk(self.master_folder_path).__next__()

        for folder in dirs:
            if folder == "BaseWorld" or folder == "__pycache__":
                dirs.remove(folder)
        
        self.world_choice = dirs[0] # For now, this is hard coded.
        
        self.all_race_dicts = self.readWorldData("Races")
        
        # Initialize all Managers
        self.oWorldManager = WorldManager(self.all_race_dicts)
        self.oCharacterManager = CharacterManager(self.all_race_dicts)
        
        self.oWorldManager.createWorld() 
        
    def readWorldData(self, category): # Read data from .json files for a given worldbuiling category
        
        all_options = []
        
        module_dir = os.path.abspath("/Users/ame94/.spyder-py3/AdventureGenerator/" +
                                     self.world_choice + "/" + category) # Establish path to relevant folder.
                
        root, dirs, files = os.walk(module_dir).__next__() # Split out all race .json files in folder.
        
        for file in files: # Transfer each .json file into a dictionary and append to all_options list
            fname = os.path.join(root,file)
            with open(fname,'r') as file:
                data = json.load(file)
            all_options.append(data)
        
        return all_options
    
    def showMap(self, view):
        self.oWorldManager.showMap(view)            
    
    def startAdventure(self):
        
        # Start by creating a main character.
        self.oCharacterManager.createCharacter()
        
            