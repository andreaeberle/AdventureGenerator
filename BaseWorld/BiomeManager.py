"""
Biome Manager Class
"""

from .Biome import *

class BiomeManager:
    
    def __init__(self, all_biome_dicts):
        
        self.all_biomes = [] # List of all Biome objects
        
        # Converting biome dicts to biome objects
        for biome in all_biome_dicts:
            oBiome = Biome(biome)
            self.all_biomes.append(oBiome)
    
    def getBiomeSpreads(self):
        biome_spreads = {}
        for biome in self.all_biomes:
            biome_name = biome.getName()
            biome_spread = biome.getBiomeSpread()
            biome_spreads[biome_name] = biome_spread
        return biome_spreads
    
    def getBiomeApplicabilities(self):
        biome_applicabilities = {}
        for biome in self.all_biomes:
            biome_name = biome.getName()
            biome_applicability = biome.getBiomeApplicability()
            biome_applicabilities[biome_name] = biome_applicability
        return biome_applicabilities
        