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
        # Smoothing out rift valleys
        self.oHexManager.finishRiftValleys()

    def addElevationFlavor(self):
        for world_hex in self.world_hexes:
            chance = np.random.randint(1,101)
            if chance <= 5:
                if world_hex.getIsValley():
                    continue # No change to valleys
                if world_hex.getIsLand() or world_hex.getIsLake():
                    if world_hex.getIsMountainous():
                        self.oHexManager.boostElevation(world_hex,2000)
                    else:
                        self.oHexManager.setElevation(world_hex,"mountains")
                        chance = np.random.randint(1,101)
                        if chance <= 20:
                            world_hex.setIsVolcanic()
                else:
                    world_hex.setIsShallows()
                    chance = np.random.randint(1,101)
                    if chance <= 20:
                        world_hex.setIsVolcanic()
            elif chance > 5 and chance <= 10:
                if world_hex.getIsValley():
                    continue # No change to valleys
                if world_hex.getIsLand() or world_hex.getIsLake():
                    if world_hex.getIsHighland():
                        self.oHexManager.boostElevation(world_hex, 2000)
                    else:
                        self.oHexManager.setElevation(world_hex, "highlands")
            elif chance > 10 and chance <= 20:
                if world_hex.getIsHighland() or world_hex.getIsHilly():
                    continue # No change to higher elevation hexes
                else:
                    if world_hex.getIsLand() or world_hex.getIsLake():
                        self.oHexManager.setElevation(world_hex, "valley")
            # Now add extra hills (running here so that highland hexes might also be hilly)
            chance = np.random.randint(1,101)
            if chance <= 10:
                if world_hex.getIsValley():
                    continue # No change to valleys
                elif world_hex.getIsMountainous():
                    self.oHexManager.boostElevation(world_hex, 1000)
                else:
                    if world_hex.getIsLand() or world_hex.getIsLake():
                        self.oHexManager.setElevation(world_hex, "hills")
                        
    def finishValleys(self):
        for world_hex in self.world_hexes:
            if world_hex.getIsValley() and not world_hex.getIsRiftValley():
                self.oHexManager.finishValley(world_hex)
                        
                    
    def showMap(self, view):
        self.oHexManager.drawWorldHexGrid(view)
