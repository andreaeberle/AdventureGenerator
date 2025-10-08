# -*- coding: utf-8 -*-
"""
Created on Sat Jun 28 23:59:29 2025

@author: ame94
"""

class WorldHex:
    
    def __init__(self, hex_position): # Each World Hex is created with a position [x, y].
        self.hex_position = hex_position
        self.is_land = False # All world hexes begin as ocean tiles
        self.is_coast = False # Land hexes only
        self.is_shallows = False # Ocean hexes only
        self.continent_index = None
        self.plate_index = ""
        self.plate_type = ""
        self.plate_movement = ""
        self.plate_boundaries = [] # A list to hold all plate boundary relationships the hex has.
                                    # The list entries will be tuples: (boundary_type, hex_side).
        self.is_volcanic = False
        self.is_mountainous = False
        self.is_highland = False
        self.is_rift_valley = False
        self.is_sea_trench = False
        self.is_valley = False
        self.is_lake = False
        self.is_hilly = False
        self.elevation = 0
        self.major_river = () # Empty tuple for river's start and end points in the hex
    
    def getHexPosition(self):
        return self.hex_position # Returns [x,y] position as a list
    
    """
    def getColor(self):
        return self.color
    """
    
    def getIsLand(self):
        return self.is_land
    
    def getIsCoast(self):
        return self.is_coast
    
    def getIsShallows(self):
        return self.is_shallows
    
    def getContinentIndex(self):
        return self.continent_index
    
    def getPlateIndex(self):
        return self.plate_index
    
    def getPlateMovement(self):
        return self.plate_movement
    
    def getPlateType(self):
        return self.plate_type
    
    def getPlateBoundaries(self):
        return self.plate_boundaries
    
    def getIsVolcanic(self):
        return self.is_volcanic
    
    def getIsMountainous(self):
        return self.is_mountainous
    
    def getIsHighland(self):
        return self.is_highland
    
    def getIsRiver(self):
        if self.major_river:
            return True
        else:
            return False
        
    def getIsValley(self):
        return self.is_valley
    
    def getIsRiftValley(self):
        return self.is_rift_valley
    
    def getIsSeaTrench(self):
        return self.is_sea_trench
    
    def getIsLake(self):
        return self.is_lake
    
    def getIsHilly(self):
        return self.is_hilly
    
    def getElevation(self):
        return self.elevation
    
    def setIsVolcanic(self):
        self.is_volcanic = True
    
    def setIsCoast(self, status): # status will be either True if coast or False if not coast
        self.is_coast = status
        
    def setIsShallows(self):
        self.is_shallows = True
        
    def setIsLake(self):
        self.is_lake = True
        
    def setIsHilly(self):
        self.is_hilly = True
        
    def setElevation(self, elevation):
        self.elevation = elevation
    
    def makeLand(self, continent_index):
        self.is_land = True
        self.continent_index = continent_index

    def addToPlate(self, plate_index):
        self.plate_index = plate_index
        
    def setPlateMovement(self, direction):
        self.plate_movement = direction
        
    def setPlateType(self, plate_type):
        self.plate_type = plate_type
        
    def setPlateBoundary(self, boundary_type):
        self.plate_boundaries.append(boundary_type)
        unique_boundaries = list(set(self.plate_boundaries)) # Removes duplicate boundary entries
        self.plate_boundaries = unique_boundaries

    def makeMountainous(self):
        self.is_mountainous = True
    
    def makeHighland(self):
        self.is_highland = True
        
    def makeRiftValley(self):
        self.is_rift_valley = True
        self.is_valley = True
        
    def makeValley(self):
        self.is_valley = True
        
    def makeSeaTrench(self):
        self.is_sea_trench = True
        
    def addRiver(self, starting_side, ending_side):
        self.major_river = (starting_side, ending_side)
        
    def makeValley(self):
        self.is_valley = True
