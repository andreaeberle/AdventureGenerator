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
    