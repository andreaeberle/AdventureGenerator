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
        
        self.prevailing_wind = ""
        self.biome_options = []
        self.biome = ""
        self.coast_type = ""
        
        self.wetland = ""
        self.is_headwaters = False
        self.river_outflow = ""
        self.river_inflows = []
        
        self.possible_resources = []
        
        self.landmark = ""
        self.civ_type = "wilds"
        self.dominion_indexes = []
        self.conflicts = []
    
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
        if self.is_headwaters:
            return True
        if self.river_outflow:
            return True
        if self.river_inflows and self.getIsLand():
            return True
        
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
    
    def getCoastType(self):
        return self.coast_type
    
    def getPrevailingWind(self):
        return self.prevailing_wind
    
    def getBiomeOptions(self):
        return self.biome_options
    
    def getBiome(self):
        return self.biome
    
    def getWetland(self):
        return self.wetland
    
    def getRiverInflows(self):
        return self.river_inflows
    
    def getRiverOutflow(self):
        return self.river_outflow
    
    def getIsHeadwaters(self):
        return self.is_headwaters
    
    def getPossibleResources(self):
        return self.possible_resources
    
    def getLandmark(self):
        return self.landmark
    
    def getCivType(self):
        return self.civ_type
    
    def getDominionIndexes(self):
        return self.dominion_indexes
    
    def getConflicts(self):
        return self.conflicts
    
    def getConflictTypes(self):
        conflict_types = []
        if self.conflicts:
            for conflict in self.conflicts:
                conflict_type = conflict[0]
                if not conflict_type in conflict_types:
                    conflict_types.append(conflict_type)
        return conflict_types
    
    def setIsVolcanic(self):
        self.is_volcanic = True
    
    def setIsCoast(self, status): # status will be either True if coast or False if not coast
        self.is_coast = status
        
    def setIsShallows(self):
        self.is_shallows = True
        
    def setIsLake(self):
        self.is_lake = True
        self.wetland = "lake"
        
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
        
    def setCoastType(self, coast_type):
        self.coast_type = coast_type
        
    def setPrevailingWind(self, direction):
        self.prevailing_wind = direction
        
    def addBiomeOption(self, biome_name):
        self.biome_options.append(biome_name)
        
    def setBiome(self, biome_name):
        self.biome = biome_name

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
        
    def setWetland(self, wetland_type="unknown"):
        self.wetland = wetland_type
        
    def setIsHeadwaters(self):
        self.is_headwaters = True
        self.is_river = True
        
    def setRiverOutflow(self, direction):
        self.river_outflow = direction
        self.is_river = True
        
    def setRiverInflow(self, direction):
        self.river_inflows.append(direction)
        self.is_river = True
        
    def assignResource(self, resource_name):
        self.possible_resources.append(resource_name)
        
    def setLandmark(self, landmark_type):
        self.landmark = landmark_type
        
    def setCivType(self, civ_type):
        self.civ_type = civ_type
        
    def setDominionIndex(self, dominion_index):
        self.dominion_indexes.append(dominion_index)
        
    def addConflict(self, conflict, stage, monster_index=""):
        conflict_and_stage = [conflict, stage]
        if monster_index:
            conflict_and_stage.append(monster_index)
        self.conflicts.append(conflict_and_stage)
