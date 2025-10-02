# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 17:45:22 2025

@author: ame94
"""

class TectonicPlate:
    
    def __init__(self, hex_list, plate_type, plate_index, plate_direction):
        self.hex_list = hex_list
        self.plate_type = plate_type
        self.plate_index = plate_index
        self.plate_direction = plate_direction
        
    def getSize(self):
        return len(self.hex_list)
    
    def setType(self):
        if self.plate_type == "minor":
            if len(self.hex_list) < 20:
                self.plate_type = "micro"
        return self.plate_type
    
    def transferMovement(self):
        for world_hex in self.hex_list:
            world_hex.setPlateMovement(self.plate_direction)
    
    def transferType(self):
        self.setType()
        for world_hex in self.hex_list:
            world_hex.setPlateType(self.plate_type)