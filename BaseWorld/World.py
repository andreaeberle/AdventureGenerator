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
        
        self.world_hexes = self.oHexManager.createWorldHexGrid(30, 60)
    
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
    
    def establishCoast(self):
        # Makes sure all the land tiles are correctly labeled as coast
        for world_hex in self.world_hexes: 
            self.oHexManager.checkIfLake(world_hex)
            self.oHexManager.checkIfCoast(world_hex)
            self.oHexManager.checkIfShallows(world_hex)
        
    def identifyPlateBoundaries(self):
        # Plates transfer movement to hexes
        for plate in self.plates:
            plate.transferMovement()
            plate.transferType()
        # Identifies the plate boundaries present for each hex
        for world_hex in self.world_hexes:
            if self.oHexManager.checkIfPlateBoundary(world_hex):
                self.oHexManager.setPlateBoundaryType(world_hex)
                is_divergent = False
                for plate_boundary in world_hex.getPlateBoundaries():
                    if "convergent" in plate_boundary:
                        if world_hex.getIsLand():
                            world_hex.makeMountainous()
                        else:
                            world_hex.setIsShallows()
                    elif "divergent" in plate_boundary:
                        is_divergent = True
                if is_divergent and len(world_hex.getPlateBoundaries()) == 1:
                    if world_hex.getIsLand():
                        world_hex.makeRiftValley()
                    else:
                        world_hex.makeSeaTrench()
                    
    def showMap(self, view):
        self.oHexManager.drawWorldHexGrid(view)
