# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 12:23:56 2025

@author: ame94
"""

class Continent:
    
    def __init__(self, hex_list, continent_index):
        self.hex_list = hex_list
        self.continent_index = continent_index
        
    def getSize(self):
        return len(self.hex_list)