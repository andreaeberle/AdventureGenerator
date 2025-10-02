"""
World Manager Class. Initializes the world by transfering data from .json files.
"""

import numpy as np

from .World import *

class WorldManager:
    def __init__(self, all_race_dicts):
        self.all_race_dicts = all_race_dicts
        self.all_races = [] # List of all race names.
        
        self.world_height = 30
        self.world_width = 60
        self.directions = ["NE", "E", "SE", "SW", "W", "NW"]
        
    def createWorld(self):
        # Extract race names from list of dicts and fill all_races list.
        for race_dict in self.all_race_dicts:
            keys = list(race_dict.keys())
            name = keys[0]
            self.all_races.append(name)
        
        self.oWorld = World(self.all_races, self.world_height, self.world_width)
        
        # Determining the number and size of continents
        
        world_area = self.world_height * self.world_width
        
        continent_number = np.random.randint(3,8)

        available_landmass = np.floor(world_area * 0.29)

        min_cont_size = 30

        continent_sizes = []

        remaining_continents = continent_number

        for continent in range(continent_number):
            if remaining_continents == 1:
                continent_size = int(np.floor(available_landmass))
            else:
                max_cont_size = available_landmass - (min_cont_size * (remaining_continents-1))
                continent_size = np.random.randint(min_cont_size, max_cont_size+1)
            continent_sizes.append(continent_size)
            remaining_continents -= 1
            available_landmass -= continent_size
        
        for continent_size in continent_sizes:
            self.oWorld.createContinent(continent_size)
        
        self.oWorld.showMap("land")
        
        # Creating tectonic plates
        
        # Determining sizes of major plates

        total_major_mass = np.floor(world_area * 0.80)
        
        max_major_plate_size = np.floor(world_area * 0.30)
        min_major_plate_size = np.floor(world_area * 0.20)
        
        major_plate_sizes = [min_major_plate_size,]
        available_plate_mass = total_major_mass - min_major_plate_size
        
        while available_plate_mass > 2*min_major_plate_size:
            major_plate_size = np.random.randint(min_major_plate_size, max_major_plate_size+1)
            major_plate_sizes.append(major_plate_size)
            available_plate_mass -= major_plate_size
        
        last_major_plate = int(available_plate_mass)
        major_plate_sizes.append(last_major_plate)
                
        actual_plate_sizes = [] # A list for tracking plate sizes once they're actually created.
        
        # Create major plates
        for size in major_plate_sizes:
            plate_direction = np.random.choice(self.directions)
            actual_plate_size = self.oWorld.createPlate(size, "major", plate_direction)
            actual_plate_sizes.append(actual_plate_size)
        
        # Create minor plates
        
        claimed_plate_mass = 0
        
        # Figuring out how many hexes have been claimed by major plates.
        for size in actual_plate_sizes:
            claimed_plate_mass += size
        
        while claimed_plate_mass < world_area:
            # Try to make a minor plate as big as it can be.
            max_minor_size = world_area * 0.15
            plate_direction = np.random.choice(self.directions)
            actual_plate_size = self.oWorld.createPlate(max_minor_size, "minor", plate_direction)
            actual_plate_sizes.append(actual_plate_size)
            claimed_plate_mass += actual_plate_size
        
        # Establish global geographic features
        
        self.oWorld.establishCoast()
        
        self.oWorld.identifyPlateBoundaries()
                
    def showMap(self, view):
        self.oWorld.showMap(view)