"""
World
"""

from .HexManager import *
from .Continent import *
from .TectonicPlate import *

class World:
    def __init__(self, all_races, map_width, map_height):
        self.all_races = all_races
        self.oHexManager = HexManager()
        self.continents = [] # List of Continent objects

        self.plates = []
        
        self.oHexManager.createWorldHexGrid(30, 60)
    
    def createContinent(self, size):
        continent_index = len(self.continents)
        
        oContinent = Continent(self.oHexManager.createContinent(size, continent_index), 
                               continent_index)
        self.continents.append(oContinent)

    def createPlate(self, size, plate_type, plate_direction):
        plate_index = len(self.plates)
        
        oTectonicPlate = TectonicPlate(self.oHexManager.createPlate(size, plate_type, plate_index),
                                       plate_type, plate_index, plate_direction)
        self.plates.append(oTectonicPlate)
        
        actual_plate_size = oTectonicPlate.getSize()
        
        return actual_plate_size

    def showMap(self, view):
        self.oHexManager.drawWorldHexGrid(view)
