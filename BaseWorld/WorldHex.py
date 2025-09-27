# -*- coding: utf-8 -*-
"""
Created on Sat Jun 28 23:59:29 2025

@author: ame94
"""

class WorldHex:
    
    def __init__(self, hex_position): # Each World Hex is created with a position [x, y].
        self.hex_position = hex_position
        self.is_land = False # All world hexes begin as ocean tiles
        self.is_coast = False
        self.continent_index = None
        self.plate_index = ""
        #print("plate index is ", self.plate_index)
    
    def getHexPosition(self):
        return self.hex_position # Returns [x,y] position as a list
    
    """
    def getColor(self):
        return self.color
    """
    
    def getIsLand(self):
        return self.is_land
    
    def getContinentIndex(self):
        return self.continent_index
    
    def getPlateIndex(self):
        return self.plate_index
    
    def setIsCoast(self, status): # status will be either True if coast or False if not coast
        self.is_coast = status
    
    def makeLand(self, continent_index):
        self.is_land = True
        self.continent_index = continent_index

    def addToPlate(self, plate_index):
        self.plate_index = plate_index

