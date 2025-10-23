"""
Biome Class
"""

class Biome:
    
    def __init__(self, biome_dict):
        
        self.keys = list(biome_dict.keys())
        
        self.name = self.keys[0] # Setting biome name
        
        self.biome_dict = biome_dict[self.name] # Pulling out biome dict
        
        #self.is_land_biome = self.biome_dict["is_land_biome"]
        
        self.biome_spread = self.biome_dict["latitude_spread"] # Pulling out latitude dict
        
        #self.hex_applicability = self.biome_dict["hex_applicability"] # Pulling out hex applicability dict
        
        #self.latitude_min = self.latitude_spread["latitude_min"]
        #self.latitude_max = self.latitude_spread["latitude_max"]
        
        self.biome_applicability = []
        for key in self.biome_spread:
            self.biome_applicability.append(key)
        # Creates a list of all hex types that the biome applies to [ocean, inland, west coast
        # east coast, and/or east coast monsoon]
        
        
            
         
        #self.in_inland = self.hex_applicability["in_inland"]
        #if self.in_inland:
        #    self.biome_applicability.append("inland")
        #self.in_west_coast = self.hex_applicability["in_west_coast"]
        #if self.in_west_coast:
        #    self.biome_applicability.append("west coast")
        #self.in_east_coast = self.hex_applicability["in_east_coast"]
        #if self.in_east_coast:
        #    self.biome_applicability.append("east coast")
        #self.in_east_coast_monsoon = self.hex_applicability["in_east_coast_monsoon"]
        #if self.in_east_coast_monsoon:
        #    self.biome_applicability.append("east coast monsoon")
        
        #if not self.biome_applicability:
        #    self.biome_applicability.append("ocean")
        
    def getName(self):
        return self.name
    
    def getBiomeApplicability(self):
        return self.biome_applicability
        
    def getBiomeSpread(self):
        return self.biome_spread # Returns a dict of {coast type: (latitude min, latitude max)}