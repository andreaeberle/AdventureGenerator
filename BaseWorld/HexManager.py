# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 20:50:34 2025

@author: ame94
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from collections import Counter

import matplotlib.colors as mcolors

from .WorldHex import *

import numpy as np
import math


class HexManager:

    def __init__(self):
        self.world_hexes = {} # A dict of World Hex objects. Key is (x,y) tuple, value is Hex object
        
        self.directions = ["NE", "E", "SE", "SW", "W", "NW"]
        self.east_directions = ["NE", "E", "SE"]
        self.west_directions = ["SW", "W", "NW"]
        
        self.continent_colors = ["red", "cyan", "yellow", "lightgreen", "purple", "pink", 
                                 "forestgreen"]
        self.plate_colors = ["white", "firebrick", "maroon", "darkorange", "peru", "saddlebrown",
                             "goldenrod", "lightcoral", "orangered", "rosybrown", "indianred", 
                             "brown", "burlywood", "rosybrown"]
        
        css4_colors = list(mcolors.CSS4_COLORS.keys())
        self.dominion_colors = css4_colors[:100]
        
        self.longest_border = ()
        self.biggest_continents = []
                
        self.ocean_hexes = []
        self.inland_hexes = []
        self.west_coast_hexes = []
        self.west_coast_2_hexes = []
        self.west_coast_3_hexes = []
        self.east_coast_hexes = []
        self.east_coast_monsoon_hexes = []
        
        self.coast_groups = {}
    
    def drawHex(self, ax, x, y, color):
      delta = 1/np.sqrt(3)
      center_x = (2*x - y%2) * delta
      center_y = y
      radius = delta*2/np.sqrt(3)
      num_sides = 6
    
      angles = np.linspace(0, 2 * np.pi, num_sides, endpoint=False)
      vertices_x = center_x + radius * np.sin(angles)
      vertices_y = center_y + radius * np.cos(angles)
      vertices = np.column_stack([vertices_x, vertices_y])
    
      hexagon = Polygon(vertices, closed=True, edgecolor='black', facecolor=color)
      ax.add_patch(hexagon)
    
    def createWorldHexGrid(self, num_rows, num_columns):
        self.num_rows = num_rows
        self.num_columns = num_columns
        
        self.equator_y = num_rows/2
        self.degree_multiplier = num_rows/180 # The real world extends 90 degrees north and south
        
        world_hex_objects = []
        for x in range(num_columns):
            for y in range(num_rows):
                new_hex = WorldHex([x,y])
                world_hex_objects.append(new_hex)
                self.world_hexes[(x,y)] = new_hex
        return world_hex_objects
                
    def drawWorldHexGrid(self, view):
        
        fig, ax = plt.subplots()
        
        self.world_hexes_keys = list(self.world_hexes.keys())
        
        for key in self.world_hexes_keys:
            x,y = key
            hex_tile = self.world_hexes[key]
            
            # Determine hex color bsed on the view selected
            if view == "land":
                title = "World Map"
                if hex_tile.getIsLand():
                    color = "darkgoldenrod"
                else:
                    color = "royalblue"
            
            if view == "continents":
                title = "World Map: Continents"
                if hex_tile.getIsLand():
                    color = self.continent_colors[hex_tile.getContinentIndex()]
                else:
                    color = "royalblue"                
            
            if view == "plates":
                title = "World Map: Tectonic Plates"
                if type(hex_tile.getPlateIndex()) is not str:
                    color = self.plate_colors[hex_tile.getPlateIndex()]
                else:
                    color = "black"
            
            if view == "geography":
                title = "World Map: Geographic Features"
                if hex_tile.getIsLand():
                    color = "darkgoldenrod" # Start with all land being brown
                    # The ordering below will allow map to overwrite for the display of the feature
                    # we would most like to have displayed on the map. If a tile is both a valley
                    # and a river, the river will be highlighted. If a tile is both a river and
                    # mountainous, the mountains will be highlighted.
                    if hex_tile.getIsCoast():
                        color = "navajowhite"
                    if hex_tile.getIsValley():
                        color = "goldenrod"
                    if hex_tile.getIsRiftValley():
                        color = "black"
                    if hex_tile.getIsRiver():
                        color = "aqua"
                    if hex_tile.getIsMountainous():
                        color = "saddlebrown"   
                    if hex_tile.getIsVolcanic():
                        color = "crimson"
                        
                else:
                    color = "royalblue" # Start with all water tiles being blue
                    if hex_tile.getIsShallows():
                        color = "lightsteelblue"
                    if hex_tile.getIsLake():
                        color = "deepskyblue"
                    if hex_tile.getIsSeaTrench():
                        color = "midnightblue"
                    if hex_tile.getIsVolcanic():
                        color = "firebrick"
                        
            if view == "topography":
                title = "World Map: Topography"
                hex_elevation = hex_tile.getElevation()
                
                if hex_tile.getIsLand() or hex_tile.getIsLake():
                    if hex_elevation < 0:
                        color = "rosybrown"
                    elif hex_elevation >= 0 and hex_elevation < 250:
                        color = "papayawhip"
                    elif hex_elevation >= 250 and hex_elevation < 500:
                        color = "navajowhite"
                    elif hex_elevation >= 500 and hex_elevation < 1000:
                        color = "burlywood"
                    elif hex_elevation >= 1000 and hex_elevation < 2000:
                        color = "goldenrod"
                    elif hex_elevation >=2000 and hex_elevation < 3000:
                        color = "darkgoldenrod"
                    elif hex_elevation >= 3000 and hex_elevation < 4000:
                        color = "sienna"
                    elif hex_elevation >= 4000 and hex_elevation < 6000:
                        color = "saddlebrown"
                    elif hex_elevation >= 6000 and hex_elevation < 10000:
                        color = "darkred"
                    elif hex_elevation >=10000 and hex_elevation < 15000:
                        color = "maroon"
                    elif hex_elevation >= 15000:
                        color = "black"
                    else:
                        color = "yellow"
                        print("Someone's elevation is funky.")
                        
                else:
                    color = "royalblue" # Start with all water tiles being blue
                    if hex_tile.getIsShallows():
                        color = "lightsteelblue"
                    if hex_tile.getIsSeaTrench():
                        color = "midnightblue"                

            if view == "biomes":
                title = "World Map: Biomes"
                
                hex_biome = hex_tile.getBiome()
                if hex_biome == "tropical ocean":
                    if hex_tile.getIsShallows():
                        color = "lightskyblue"
                    else:
                        color = "blue"
                elif hex_biome == "temperate ocean":
                    if hex_tile.getIsShallows():
                        color = "cornflowerblue"
                    else:
                        color = "royalblue"
                elif hex_biome == "arctic ocean":
                    if hex_tile.getIsShallows():
                        color = "steelblue"
                    else:
                        color = "darkblue"
                elif hex_biome == "icecap":
                    color = "white"
                elif hex_biome == "tundra":
                    color = "thistle"
                elif hex_biome == "taiga":
                    color = "lightsteelblue"
                elif hex_biome == "tropical forest":
                    color = "darkgreen"
                elif hex_biome == "temperate forest":
                    color = "darkslategrey"
                elif hex_biome == "temperate seasonal forest":
                    color = "darkolivegreen"
                elif hex_biome == "tropical seasonal forest":
                    color = "green"
                elif hex_biome == "chaparral":
                    color = "darkorange"
                elif hex_biome == "temperate plains":
                    color = "darkseagreen"
                elif hex_biome == "subtropical plains":
                    color = "gold"
                elif hex_biome == "tropical desert":
                    color = "firebrick"
                elif hex_biome == "tropical plains":
                    color = "yellow"
                elif hex_biome == "laurentian":
                    color = "teal"
                elif hex_biome == "temperate desert":
                    color = "khaki"
                
                else:
                    color = "magenta"

            if view == "rivers":
                title = "World Map: Rivers/Wetlands"
                
                wetland_type = hex_tile.getWetland()
                
                if hex_tile.getIsLand():
                    color = "darkgoldenrod"
                else:
                    color = "royalblue"
                    
                if hex_tile.getIsRiver():
                    color = "cyan"
                    
                if hex_tile.getIsHeadwaters():
                    color = "paleturquoise"
                    
                if wetland_type == "vernal pool":
                    color = "darkkhaki"
                    
                if wetland_type == "oasis":
                    color = "yellowgreen"
                    
                if wetland_type == "bog":
                    color = "darkseagreen"

                if wetland_type == "fen":
                    color = "mediumseagreen"

                if wetland_type == "marsh":
                    color = "lightseagreen"
                    
                if wetland_type == "swamp":
                    color = "olivedrab"

                if wetland_type == "lake":
                    color = "deepskyblue"

                if wetland_type == "endorheic basin":
                    color = "olive"
                    
                if wetland_type == "estuary":
                    color = "darkcyan"
                    
                if wetland_type and not "estuary" in wetland_type:
                    print(wetland_type)

            if view == "debug resources":
                title = "World Map: Debugging Resources"
                if "corn" in hex_tile.getPossibleResources():
                    color = "yellow"
                    if "wolf" in hex_tile.getPossibleResources():
                        color = "orange"
                elif "wolf" in hex_tile.getPossibleResources():
                    color = "red"
                else:
                    color = "black"

            if view == "landmarks":
                title = "World Map: Landmarks"
                hex_landmark = hex_tile.getLandmark()

                if not hex_landmark:
                    if hex_tile.getIsLand():
                        color = "darkgoldenrod"
                    else:
                        color = "royalblue"
                elif hex_landmark == "city":
                    color = "yellow"
                elif hex_landmark == "military fortress":
                    color = "green"
                elif hex_landmark == "religious site":
                    color = "orange"
                elif hex_landmark == "center of learning":
                    color = "purple"
                elif hex_landmark == "monster lair":
                    color = "red"
                elif hex_landmark == "natural wonder":
                    color = "aqua"
                elif hex_landmark == "ruin":
                    color = "black"
                    
            if view == "dominions":
                title = "World Map: Dominions"        
                
                if not hex_tile.getDominionIndex():
                    if hex_tile.getIsLand():
                        color = "darkgoldenrod"
                    else:
                        color = "royalblue"
                
                else:
                    if len(hex_tile.getDominionIndex()) > 1:
                        color = "black"
                        print(hex_tile.getDominionIndex())
                    else:
                        color = self.dominion_colors[hex_tile.getDominionIndex()[0]]
                

            self.drawHex(ax, x, y, color)
        
        plt.title(title)
        plt.xlim(-2,70)
        plt.ylim(-2,31)
        plt.show()

    def createContinent(self, size, index):
        
        continent_perimeter = [] # List of WorldHex objects that are coast tiles
        continent_hexes = [] # Will gather all the hexes in the continent
        
        # Start by picking a random hex and turning it into a land tile
        clear_to_grow = False
        while clear_to_grow is False:
            starting_hex_x = np.random.randint(6, self.num_columns-5)
            starting_hex_y = np.random.randint(6, self.num_rows-5)
    
            starting_hex = self.world_hexes[(starting_hex_x, starting_hex_y)]
            
            if starting_hex.getIsLand():
                clear_to_grow = False
            
            else:
                starting_hex.makeLand(index)
                continent_hexes.append(starting_hex)
                continent_perimeter.append(starting_hex) # Adds starting hex to continent perimeter
                                
                # Create six arms from starting point
                if size < 50:
                    max_arm_size = 4
                else:
                    max_arm_size = 7
                
                for arm in range(6):
                    growing_hex = starting_hex # The first hex to grow out from will be the starting hex
                    length = np.random.randint(0,max_arm_size)
                    for tile in range(length):
                        growing_hex = self.getNeighbor(growing_hex, self.directions[arm])
                        if growing_hex:
                            if growing_hex.getIsLand():
                                break
                            else:
                                growing_hex.makeLand(index)
                            continent_hexes.append(starting_hex)
                            if self.checkIfCoast(growing_hex): # Adds new land tile to list if coast
                                continent_perimeter.append(growing_hex) 
                        else:
                            break
                clear_to_grow = True
                
        # Build out the continent based until it reaches its destined size
        while len(continent_hexes) < size:
            if not continent_perimeter: # Checks to see if list is empty
                break
            growing_hex = np.random.choice(continent_perimeter) # Selects a random coast tile
            if not self.checkIfCoast(growing_hex): 
                # If selected tile is no longer a coast tile, removes it from the list
                continent_perimeter.remove(growing_hex)
            else:
                ocean_neighbors = []
                neighbors = self.getNeighbors(growing_hex)
                for neighbor in neighbors: # Removes all land tiles from ocean neighbors list
                    if neighbor and not neighbor.getIsLand():
                        ocean_neighbors.append(neighbor)
                for neighbor in ocean_neighbors:
                    # Remove ocean tiles that are too close to the map edge
                    neighbor_x = neighbor.getHexPosition()[0]
                    if neighbor_x < 2 or neighbor_x > self.num_columns-3:
                        ocean_neighbors.remove(neighbor)
                # If there isn't anywhere to grow from the selected tile, it's skipped and removed
                # from the perimeter list
                if not ocean_neighbors:
                    continent_perimeter.remove(growing_hex)
                    continue # Return to the top of the while loop to select a new tile
                
                new_hex = np.random.choice(ocean_neighbors)

                new_hex_neighbors = self.getNeighbors(new_hex) # Get new hex's neighbors
                # Probability /100 new hex will become land if surrounded by ocean
                chance_of_land = 10
                for neighbor in new_hex_neighbors:
                    # Increases chance of becoming land if bordered by land
                    if not neighbor: # Prevents an error from reaching bottom or top of map
                        break
                    if neighbor.getIsLand(): 
                        chance_of_land += 15 
                land_roll = np.random.randint(0,101)
                if land_roll <= chance_of_land:
                    new_hex.makeLand(index)
                    continent_hexes.append(new_hex)
                    if self.checkIfCoast(new_hex): # Add new tile to perimeter if coast tile
                        continent_perimeter.append(new_hex)
        return continent_hexes
    
    def createPlate(self, size, plate_type, index):
                
        plate_perimeter = []
        plate_hexes = []
        
        if index == 0: # The first plate will always be the polar plate
            # Start with the bottom two rows of hexes in the polar plate
            for y in range(2):
                for x in range(self.num_columns):
                    new_hex = self.world_hexes[(x,y)]
                    new_hex.addToPlate(index)
                    plate_hexes.append(new_hex)
                    if y == 1:
                        plate_perimeter.append(new_hex)
        
        elif index == 1: # The second plate will be based on the longest contient border, if any
            
            continent_indexes = []
            self.continent_borders = []
            
            # Finding all the continent border relationships
            for key in self.world_hexes_keys:
                x,y = key
                hex_tile = self.world_hexes[key]
                
                if hex_tile.getIsLand(): # Ask every tile whether they're a land tile
                
                    hex_tile_continent = hex_tile.getContinentIndex()
                    
                    # Creates a list of all continent indexes as it goes through all land tiles.
                    continent_indexes.append(hex_tile_continent)
                    
                    hex_neighbors = self.getNeighbors(hex_tile) # If so, get their neighbors
                    # See if any neighbors are on a different continent
                    for neighbor in hex_neighbors: 
                        if not neighbor:
                            continue # Skips None entries at edges
                        neighbor_continent = neighbor.getContinentIndex()
                        if not neighbor_continent:
                            continue # Skips ocean tiles
                        if hex_tile_continent != neighbor_continent:
                            continent_border = []
                            continent_border.append(hex_tile_continent)
                            continent_border.append(neighbor_continent)
                            continent_border.sort()
                            border_tuple = tuple(continent_border)
                            self.continent_borders.append(border_tuple)
            
            if self.continent_borders:
                counted_list = Counter(self.continent_borders)
                self.longest_border = counted_list.most_common(1)[0][0]
                                
                for key in self.world_hexes_keys:
                    x,y = key
                    hex_tile = self.world_hexes[key]
                    
                    # Assign all tiles from one of continents with the longest border to the plate.
                    if hex_tile.getContinentIndex() == self.longest_border[0]:
                        if hex_tile.getPlateIndex() != "":
                            continue # Skips tiles in the continent that are already in a plate.
                        hex_tile.addToPlate(index)
                        plate_hexes.append(hex_tile)
                        
                        # Check if the tile is a perimeter.
                        hex_neighbors = self.getNeighbors(hex_tile)
                        for tile in hex_neighbors:
                            if tile and tile.getContinentIndex() != self.longest_border[0]:
                                plate_perimeter.append(hex_tile)
                
            else:
                counted_list = Counter(continent_indexes)
                self.biggest_continents = counted_list.most_common(2)
                
                for key in self.world_hexes_keys:
                    x,y = key
                    hex_tile = self.world_hexes[key]
                    
                    # Assign all tiles from the biggest continent to the plate.
                    if hex_tile.getContinentIndex() == self.biggest_continents[0][0]:
                        if hex_tile.getPlateIndex() != "":
                            continue # Skips tiles in the continent that are already in a plate.
                        hex_tile.addToPlate(index)
                        plate_hexes.append(hex_tile)
                
                        # Check if the tile is a perimeter.
                        hex_neighbors = self.getNeighbors(hex_tile)
                        for tile in hex_neighbors:
                            if tile and tile.getContinentIndex() != self.biggest_continents[0]:
                                plate_perimeter.append(hex_tile)
                            
        elif index == 2:
            if self.continent_borders:
                
                for key in self.world_hexes_keys:
                    x,y = key
                    hex_tile = self.world_hexes[key]
                    
                    # Assign all tiles from the other continent with the longest border to the plate.
                    if hex_tile.getContinentIndex() == self.longest_border[1]:
                        if hex_tile.getPlateIndex() != "":
                            continue # Skips tiles in the continent that are already in a plate.
                        hex_tile.addToPlate(index)
                        plate_hexes.append(hex_tile)
                        
                        # Check if the tile is a perimeter.
                        hex_neighbors = self.getNeighbors(hex_tile)
                        for tile in hex_neighbors:
                            if tile and tile.getContinentIndex() != self.longest_border[1]:
                                plate_perimeter.append(hex_tile)
                
            else:
                for key in self.world_hexes_keys:
                    x,y = key
                    hex_tile = self.world_hexes[key]
                    
                    # Assign all tiles from the biggest continent to the plate.
                    if hex_tile.getContinentIndex() == self.biggest_continents[1]:
                        if hex_tile.getPlateIndex() != "":
                            continue # Skips tiles in the continent that are already in a plate.
                        hex_tile.addToPlate(index)
                        plate_hexes.append(hex_tile)
                
                        # Check if the tile is a perimeter.
                        hex_neighbors = self.getNeighbors(hex_tile)
                        for tile in hex_neighbors:
                            if tile and tile.getContinentIndex() != self.biggest_continents[1]:
                                plate_perimeter.append(hex_tile)
            
        else:
            unclaimed_hexes = []
            
            for key in self.world_hexes_keys:
                x,y = key
                hex_tile = self.world_hexes[key]
            
                # Make a list of unclaimed hexes.
                if hex_tile.getPlateIndex() == "":
                    unclaimed_hexes.append(hex_tile)
            
            random_hex = np.random.choice(unclaimed_hexes)
            
            random_hex.addToPlate(index)
            plate_hexes.append(random_hex)
            plate_perimeter.append(random_hex)
                            
        # Continue building out the plate until it reaches its destined size
        while len(plate_hexes) < size and len(plate_perimeter) != 0:
            growing_hex = np.random.choice(plate_perimeter) # Selects a random tile from the plate
            
            # Checks if selected tile is on a plate boundary
            if not self.checkIfPlateBoundary(growing_hex):
                plate_perimeter.remove(growing_hex)
                continue # Returns to the top of the while loop to select another tile
                        
            # Check for viable directions to grow out plate
            growing_hex_neighbors = self.getNeighbors(growing_hex)
            plate_growth_options = []
            for tile in growing_hex_neighbors:
                if tile and tile.getPlateIndex() != growing_hex.getPlateIndex():
                    
                    if tile.getPlateIndex() != "":
                        continue
                    
                    if index ==1:
                        
                        if self.longest_border and tile.getContinentIndex() == self.longest_border[1]:
                            continue
                        # Specifically forbids tiles from the other continent in the longest
                        # border pair from being added to the second major plate.
                        
                        # If there are no continent borders...
                        elif self.biggest_continents and tile.getContinentIndex() == self.biggest_continents[1]: 
                            continue
                            # Specifically forbids tiles from the second largest continent from
                            # being added to the second major plate.
                    
                    plate_growth_options.append(tile)
                    
            if not plate_growth_options:
                plate_perimeter.remove(growing_hex)
                if len(plate_perimeter) != 0: # This means there are still more options.
                    continue # Returns to the top of the while loop to select another tile
                else:
                    break
            
            new_plate_hex = np.random.choice(plate_growth_options)
            
            new_hex_neighbors = self.getNeighbors(new_plate_hex)
            chance_of_growth = 5
            for neighbor in new_hex_neighbors:
                if not neighbor:
                    break
                elif neighbor.getPlateIndex() != "":
                    chance_of_growth += 5
            plate_roll = np.random.randint(0, 101)
            if plate_roll <= chance_of_growth:
                new_plate_hex.addToPlate(index)
                plate_hexes.append(new_plate_hex)
                if self.checkIfPlateBoundary(new_plate_hex):
                    plate_perimeter.append(new_plate_hex)
        
        # Once plate has been formed, check for holes
        for tile in plate_hexes: # Go through every tile in the plate.
            tile_neighbors = self.getNeighbors(tile)
            for neighbor in tile_neighbors:
                if not neighbor: 
                    continue # Prevents searching off the edge of the map.
                if neighbor.getPlateIndex() == "": # If a neighboring tile is not in a plate...
                    # ...get that neighbor's neighbors. It might be a hole.   
                    is_hole = True # Assume it's a hole until proven otherwise.
                    neighbor_buddies = self.getNeighbors(neighbor)
                    for buddy in neighbor_buddies:
                        if not buddy:
                            continue # Being at the edge of the map can still count as a hole
                        if buddy.getPlateIndex() == "":
                            is_hole = False # Not a hole if tile is next to another empty tile.
                    if is_hole:
                        plate_hexes.append(neighbor)
                        neighbor.addToPlate(index)
                    
        return plate_hexes
    
    def getNeighbor(self, world_hex, direction): # Pass a World Hex object and a direction string
        even_row_adjustment = (world_hex.getHexPosition()[1]+1)%2
        odd_row_adjustment = (world_hex.getHexPosition()[1])%2
        if direction == "NE":
            x = world_hex.getHexPosition()[0] + even_row_adjustment
            y = world_hex.getHexPosition()[1] + 1
            if y >= (self.num_rows):
                return None
            if x >= (self.num_columns):
                x = even_row_adjustment
            ne_neighbor = self.world_hexes[(x,y)]
            return ne_neighbor
        
        elif direction == "E":
            x = world_hex.getHexPosition()[0] + 1
            y = world_hex.getHexPosition()[1]
            if x >= (self.num_columns):
                x = 0
            east_neighbor = self.world_hexes[(x,y)]
            return east_neighbor
        
        elif direction == "SE":
            x = world_hex.getHexPosition()[0] + even_row_adjustment
            y = world_hex.getHexPosition()[1] - 1
            if y < 0:
                return None
            if x >= (self.num_columns):
                x = even_row_adjustment
            se_neighbor = self.world_hexes[(x,y)]
            return se_neighbor
        
        elif direction == "SW":
            x = world_hex.getHexPosition()[0] - odd_row_adjustment
            y = world_hex.getHexPosition()[1] - 1
            if y < 0:
                return None
            if x < 0:
                x = self.num_columns - 1
            sw_neighbor = self.world_hexes[(x,y)]
            return sw_neighbor
        
        elif direction == "W":
            x = world_hex.getHexPosition()[0] - 1
            y = world_hex.getHexPosition()[1]
            if x < 0:
                x = self.num_columns - 1
            west_neighbor = self.world_hexes[(x,y)]
            return west_neighbor
        
        elif direction == "NW":
            x = world_hex.getHexPosition()[0] - odd_row_adjustment
            y = world_hex.getHexPosition()[1] + 1
            if y >= (self.num_rows):
                return None
            if x < 0:
                x = self.num_columns - 1
            nw_neighbor = self.world_hexes[(x,y)]
            return nw_neighbor

    def getNeighbors(self, world_hex): # Returns a list of all neighboring World Hex objects
        neighbors = []
        for direction in self.directions:
            neighbors.append(self.getNeighbor(world_hex, direction))
        return neighbors
    
    def checkIfCoast(self, world_hex): # Checks if WorldHex object is touching an ocean tile
        neighbhors = self.getNeighbors(world_hex) # Returns list of all neighboring World Hex objects
        for neighbor in neighbhors:
            if not neighbor:
                continue
            if not neighbor.getIsLand():
                if neighbor.getIsLake():
                    continue
                else:
                    # Sets World Hex obj as coast if touching an ocean tile
                    world_hex.setIsCoast(True)
                    return True
        world_hex.setIsCoast(False) # If World Hex is not touching any ocean tiles, it's not coast
        return False
    
    def checkIfShallows(self, world_hex):
        if world_hex.getIsLand(): # A land tile cannot be shallows
            return False
        neighbhors = self.getNeighbors(world_hex)
        for neighbor in neighbhors:
            if not neighbor:
                continue
            elif neighbor.getIsLand(): # If any neighbor is a land hex, it's a shallows hex
                world_hex.setIsShallows()
    
    def checkIfLake(self, world_hex):
        if not world_hex.getIsLand():
            neighbors = self.getNeighbors(world_hex)
            for neighbor in neighbors:
                if not neighbor:
                    continue
                if not neighbor.getIsLand():
                    # Will end the method if the hex is not completely surrounded by land
                    return False 
            world_hex.setIsLake() # Makes it a lake hex if the ocean hex is completely 
                                    # surrounded by land.
    
    def checkIfPlateBoundary(self, world_hex): 
        # Checks if WorldHex object is touching a hex from a different tectonic plate
        neighbhors = self.getNeighbors(world_hex)
        for neighbor in neighbhors:
            if not neighbor:
                continue
            if neighbor.getPlateIndex() != world_hex.getPlateIndex():
                return True
        return False        
    
    def setPlateBoundaryType(self, world_hex):
        plate_hierarchy = ["micro", "minor", "major"]
        world_hex_direction = world_hex.getPlateMovement()
        
        for direction in self.directions:
            boundary_type = ""
            neighbor = self.getNeighbor(world_hex, direction)
            if not neighbor:
                continue # Prevents going off the top or bottom of map
            if world_hex.getPlateIndex() == neighbor.getPlateIndex():
                continue # Prevents comparing to neighbors on the same plate as the hex
            neighbor_direction = neighbor.getPlateMovement()
            
            # Establish which three directions would be moving away from the world hex
            direction_index = self.directions.index(direction)
            
            away_from_world_hex = []
            away_from_world_hex.append(direction)
            
            if direction_index + 1 > 5:
                new_index = direction_index - 5
                away_from_world_hex.append(self.directions[new_index])
            else:
                away_from_world_hex.append(self.directions[direction_index+1])
                
            if direction_index - 1 < 0:
                new_index = direction_index + 5
                away_from_world_hex.append(self.directions[new_index])
            else:
                away_from_world_hex.append(self.directions[direction_index-1])
            
            
            # If the hex's neighbor is moving away from the hex...
            if neighbor_direction in away_from_world_hex:

                # ...and the hex is moving directly towards the neighbor...
                if world_hex_direction == direction:
                    # then you need to check the plate size (i.e., speed).
                    world_hex_type = world_hex.getPlateType()
                    neighbor_type = neighbor.getPlateType()
                    # If the neighbor is moving faster than the hex...
                    if plate_hierarchy.index(world_hex_type) > plate_hierarchy.index(neighbor_type):
                        #... then it's divergent.
                        boundary_type = ("divergent", direction)
                            
                    # If both hexes are moving at the same speed...
                    elif plate_hierarchy.index(world_hex_type) == plate_hierarchy.index(neighbor_type):
                        #...it's transform.
                        boundary_type = ("transform", direction)
                    else:
                        #... otherwise, it's convergent.
                        boundary_type = ("convergent", direction)
                else: 
                    boundary_type = ("divergent", direction)
                        
            # Otherwise, if the hex's neighbor is moving towards it...
            else:
                # Determine relationships between where the hex's neighbor is 
                # and where the hex is moving.
                
                # The direction the neighbor is located in
                if direction in self.east_directions:
                    direction_index = self.east_directions.index(direction)
                else: 
                    direction_index = self.west_directions.index(direction)
                    
                # The direction the world hex is moving
                if world_hex_direction in self.east_directions:
                    world_hex_direction_index = self.east_directions.index(world_hex_direction)
                else: world_hex_direction_index = self.west_directions.index(world_hex_direction)
                
                # The direction the neighbor is moving
                if neighbor_direction in self.east_directions:
                    neighbor_direction_index = self.east_directions.index(neighbor_direction)
                else:
                    neighbor_direction_index = self.west_directions.index(neighbor_direction)
                    
                # If the hex is moving directly towards it's neighbor...
                if direction_index == world_hex_direction_index:
                    # ...it's convergent.
                    boundary_type = ("convergent", direction)
                    
                # If the hex is moving in the opposite direction that the neighbor is moving in...
                elif world_hex_direction_index == neighbor_direction_index:
                    # ...it's transform.
                    boundary_type = ("transform", direction)
                
                    # If the hex is moving away from its neighbor...
                elif world_hex_direction not in away_from_world_hex:
                    #...then you need to check the plate size (i.e., speed).
                    world_hex_type = world_hex.getPlateType()
                    neighbor_type = neighbor.getPlateType()
                    # If the hex is moving faster than its neighbor...
                    if plate_hierarchy.index(world_hex_type) < plate_hierarchy.index(neighbor_type):
                        #... then it's divergent.
                        boundary_type = ("divergent", direction)
                    # If hexes are moving at the same speed...
                    elif plate_hierarchy.index(world_hex_type) == plate_hierarchy.index(neighbor_type):
                        # ...it's transform.
                        boundary_type = ("transform", direction)
                    else:
                        #... otherwise, it's convergent.
                        boundary_type = ("convergent", direction)
                
                # Otherwise, it's converget.
                else:
                    boundary_type = ("convergent", direction)
                
            world_hex.setPlateBoundary(boundary_type)
            
            if "convergent" in boundary_type:
                if world_hex.getIsLand() or world_hex.getIsLake():
                    if not world_hex.getIsMountainous():
                        world_hex.makeMountainous()
                        world_hex.makeHighland()
                        self.setElevation(world_hex, "plate mountains")
                    if not neighbor.getIsLand() and not neighbor.getIsLake():
                        world_hex.setIsVolcanic()
                else:
                    if neighbor.getIsLand():
                        world_hex.makeSeaTrench()
                    else:
                        world_hex.setIsShallows()
                        
        for plate_boundary in world_hex.getPlateBoundaries():
            if "divergent" in plate_boundary:
                is_divergent = True
                if is_divergent and len(world_hex.getPlateBoundaries()) == 1:
                    if world_hex.getIsLand():
                        world_hex.makeRiftValley()
                        self.setElevation(world_hex, "valley")
                    else:
                        world_hex.setIsShallows()
                        world_hex.setIsVolcanic()
            
    def setElevation(self, world_hex, feature):
        if feature == "plate mountains":
            elevation = np.random.randint(4000,17001)
            world_hex.makeMountainous()
            world_hex.makeHighland()
        elif feature == "mountains":
            elevation = np.random.randint(2000,10001)
            world_hex.makeMountainous()
            world_hex.makeHighland()
        elif feature == "highlands":
            elevation = np.random.randint(1000,10001)
            world_hex.makeHighland()
        elif feature == "hills":
            elevation = np.random.randint(50,1000)
            world_hex.setIsHilly()
        elif feature == "valley":
            elevation_drop = np.random.randint(300, 1000)
            elevation = world_hex.getElevation() - elevation_drop
            if elevation < 0:
                elevation = 0
            world_hex.makeValley()
        world_hex.setElevation(elevation)
        # After the elevation has been set, smooth out the elevation across the surrounding tiles
        self.smoothElevation(world_hex)
        
    def smoothElevation(self,world_hex):
        changed_hexes = [world_hex,]
        while changed_hexes:
            changed_hex = changed_hexes.pop()
            neighbors = self.getNeighbors(changed_hex)
            for neighbor in neighbors:
                if not neighbor:
                    continue # Prevents checking off top or bottom of map
                if not neighbor.getIsLand() and not neighbor.getIsLake():
                    continue # No change to ocean tiles
                if changed_hex.getIsMountainous() or changed_hex.getIsHighland():
                    min_elevation = changed_hex.getElevation()/5
                else:
                    min_elevation = changed_hex.getElevation()/2
                    
                if neighbor.getElevation() >= min_elevation:
                    continue # No change to tile's elevation if it's already as high or higher 
                            # than the minimum elevation.
                else:
                    if neighbor.getIsValley():
                        continue # No change to tile's that are already valleys.
                    neighbor.setElevation(min_elevation)
                    if min_elevation >= 3000:
                        neighbor.makeHighland()
                    changed_hexes.append(neighbor)
                    
    def finishRiftValleys(self):
        rift_valley_hexes = []
        for key in self.world_hexes_keys:
            x,y = key
            world_hex = self.world_hexes[key]
            if world_hex.getIsRiftValley():
                rift_valley_hexes.append(world_hex)
        for world_hex in rift_valley_hexes:
                neighbors = self.getNeighbors(world_hex)
                found_new_valley = False
                for neighbor in neighbors:
                    if found_new_valley == True:
                        break
                    if not neighbor:
                        continue
                    if neighbor.getIsMountainous():
                        continue
                    if not neighbor.getIsLand() and not neighbor.getIsLake():
                        continue
                    neighbor_buddies = self.getNeighbors(neighbor)
                    for buddy in neighbor_buddies:
                        if not buddy:
                            continue
                        if buddy == world_hex:
                            continue
                        if buddy.getIsRiftValley():
                            neighbor.makeRiftValley()
                            self.setElevation(neighbor,"valley")
                            found_new_valley = True
                            break
                        
    def finishValley(self, world_hex):
        neighbhors = self.getNeighbors(world_hex)
        for neighbor in neighbhors:
            if not neighbor:
                continue
            if neighbor.getIsHighland() or neighbor.getIsHilly() or neighbor.getIsValley():
                continue
            if not neighbor.getIsLand() and not neighbor.getIsLake():
                continue
            else:
                chance = np.random.randint(1,101)
                if chance < 15:
                    self.setElevation(neighbor, "mountains")
                else:
                    self.setElevation(neighbor, "hills")
                        
    def boostElevation(self, world_hex, elevation_boost):
        new_elevation = world_hex.getElevation() + elevation_boost
        world_hex.setElevation(new_elevation)
        self.smoothElevation(world_hex)
                  
    def findCoastType(self, world_hex, continent_sizes):
        
        if not world_hex.getIsLand() and not world_hex.getIsLake():
            self.ocean_hexes.append(world_hex)
            return world_hex.setCoastType("ocean")
        
        
        if not world_hex.getIsCoast():
            self.inland_hexes.append(world_hex)
            return world_hex.setCoastType("inland")
        
        west_neighbors = []
        west_ocean_neighbors = []
        west_neighbors.append(self.getNeighbor(world_hex,"NW"))
        west_neighbors.append(self.getNeighbor(world_hex, "W"))
        west_neighbors.append(self.getNeighbor(world_hex, "SW"))
        for neighbor in west_neighbors:
            if not neighbor:
                continue
            if not neighbor.getIsLand():
                west_ocean_neighbors.append(neighbor)
                
        east_neighbors = []
        east_ocean_neighbors = []
        east_neighbors.append(self.getNeighbor(world_hex,"NE"))
        east_neighbors.append(self.getNeighbor(world_hex, "E"))
        east_neighbors.append(self.getNeighbor(world_hex, "SE"))
        for neighbor in east_neighbors:
            if not neighbor:
                continue
            if not neighbor.getIsLand():
                east_ocean_neighbors.append(neighbor)
        
        if west_ocean_neighbors and east_ocean_neighbors:
            coast_dominance = 0
            for neighbor in west_ocean_neighbors:
                coast_dominance -= 1
            for neighbor in east_ocean_neighbors:
                coast_dominance += 1
            if coast_dominance == 0:
                coin_flip = np.random.randint(2)
                if coin_flip == 0:
                    self.west_coast_hexes.append(world_hex)
                    return world_hex.setCoastType("west coast")
            elif coast_dominance < 0:
                self.west_coast_hexes.append(world_hex)
                return world_hex.setCoastType("west coast")
            
        elif west_ocean_neighbors:
            self.west_coast_hexes.append(world_hex)
            return world_hex.setCoastType("west coast")
        
        # Now we are just left with the east coast hexes. We need to figure out which are on
        # landmasses large enough to be east coast monsoon hexes.
        
        touching_continents = list(set(self.continent_borders))
        continent_index = world_hex.getContinentIndex()
        landmass_size = continent_sizes[continent_index]
        for relationship in touching_continents:
            if continent_index in relationship:
                for continent in relationship:
                    if continent_index == continent:
                        continue # Skips the hex's continent
                    else:
                        landmass_size += continent_sizes[continent]
        
        if landmass_size >= 80:
            self.east_coast_monsoon_hexes.append(world_hex)
            return world_hex.setCoastType("east coast monsoon")
        else:
            self.east_coast_hexes.append(world_hex)
            return world_hex.setCoastType("east coast")
        
    def setAuxiliaryCoastTypes(self):
        # This is run after all hexes have been assigned a coast type of ocean, inland,
        # west coast, east coast, or east coast monsoon.
        
        for world_hex in self.west_coast_hexes:
            east_neighbor = self.getNeighbor(world_hex, "E")
            if not east_neighbor:
                continue
            if east_neighbor.getCoastType() == "inland":
                # Puts hexes one column in from the west coast in the west coast 2 category
                # unless they're a coast or the ocean.
                east_neighbor.setCoastType("west coast 2")
                self.west_coast_2_hexes.append(east_neighbor)
                self.inland_hexes.remove(east_neighbor)
                # Go one step further for the next column inland.
                east_neighbor_neighbor = self.getNeighbor(east_neighbor, "E")
                if not east_neighbor_neighbor:
                    continue
                if east_neighbor_neighbor.getCoastType() == "inland":
                    # Puts hexes two columns in from the west coast in the west coast 3 category
                    # unless they're a coast or the ocean.
                    east_neighbor_neighbor.setCoastType("west coast 3")
                    self.west_coast_3_hexes.append(east_neighbor_neighbor)
                    self.inland_hexes.remove(east_neighbor_neighbor)
            
    def setPrevailingWinds(self, trade_wind_limits, westerlies_limits, easterlies_limits):
        for key in self.world_hexes_keys:
            x,y = key
            world_hex = self.world_hexes[key]
            
            # Check for Northeasterly Trade Winds applicability
            min_n_latitude = math.floor(self.equator_y + trade_wind_limits[0]*self.degree_multiplier)
            max_n_latitude = math.floor(self.equator_y + trade_wind_limits[1]*self.degree_multiplier)
            
            if y >= min_n_latitude and y <= max_n_latitude:
                world_hex.setPrevailingWind("NE")
                
            else:
                # Check for Southeasterly Trade Winds applicability
                min_s_latitude = math.floor(self.equator_y - trade_wind_limits[0]*self.degree_multiplier)
                max_s_latitude = math.floor(self.equator_y - trade_wind_limits[1]*self.degree_multiplier)
                
                if y <= min_s_latitude and y >= max_s_latitude:
                    world_hex.setPrevailingWind("SE")
                    
                else:
                    # Check for Westerlies applicability
                    min_n_latitude = math.floor(self.equator_y + westerlies_limits[0]*self.degree_multiplier)
                    max_n_latitude = math.floor(self.equator_y + westerlies_limits[1]*self.degree_multiplier)
                    min_s_latitude = math.floor(self.equator_y - westerlies_limits[0]*self.degree_multiplier)
                    max_s_latitude = math.floor(self.equator_y - westerlies_limits[1]*self.degree_multiplier)
                    
                    if (y >= min_n_latitude and y <= max_n_latitude) or (y <= min_s_latitude and 
                                                                     y >= max_s_latitude):
                        world_hex.setPrevailingWind("W")
                        
                    else:
                        # Check for Polar Easterliers applicability
                        min_n_latitude = math.floor(self.equator_y + easterlies_limits[0]*self.degree_multiplier)
                        max_n_latitude = math.floor(self.equator_y + easterlies_limits[1]*self.degree_multiplier)
                        min_s_latitude = math.floor(self.equator_y - easterlies_limits[0]*self.degree_multiplier)
                        max_s_latitude = math.floor(self.equator_y - easterlies_limits[1]*self.degree_multiplier)
                        
                        if (y >= min_n_latitude and y <= max_n_latitude) or (y <= min_s_latitude and 
                                                                          y >= max_s_latitude):
                            world_hex.setPrevailingWind("E")
                
    def applyBiome(self, biome_name, biome_spread, biome_applicability):
        
        if not self.coast_groups:
            self.coast_groups["ocean"] = self.ocean_hexes
            self.coast_groups["east coast"] = self.east_coast_hexes
            self.coast_groups["east coast monsoon"] = self.east_coast_monsoon_hexes
            self.coast_groups["west coast"] = self.west_coast_hexes
            self.coast_groups["west coast 2"] = self.west_coast_2_hexes
            self.coast_groups["west coast 3"] = self.west_coast_3_hexes
            self.coast_groups["inland"] = self.inland_hexes
                
        for coast_type in self.coast_groups:
            
            if coast_type in biome_applicability:
                latitude_range = biome_spread[coast_type]
                min_latitude = latitude_range["latitude_min"]
                max_latiude = latitude_range["latitude_max"]
                # Gives a tuple of (latitude min, latitue max)
                
                min_n_latitude = math.floor(self.equator_y + min_latitude*self.degree_multiplier)
                max_n_latitude = math.floor(self.equator_y + max_latiude*self.degree_multiplier)
                min_s_latitude = math.floor(self.equator_y - min_latitude*self.degree_multiplier)
                max_s_latitude = math.floor(self.equator_y - max_latiude*self.degree_multiplier)
                
                for world_hex in self.coast_groups[coast_type]:
                    x,y = world_hex.getHexPosition()
                
                    if (y >= min_n_latitude and y <= max_n_latitude) or (y <= min_s_latitude and 
                                                                     y >= max_s_latitude):
                        world_hex.addBiomeOption(biome_name)
                            
    def finalizeBiomes(self):
        # Finalizes all biomes, adjusts for rain shadow, and checks for forests
        # next to deserts
        
        # Fixing overlapping biomes. This is janky. Ideally, I'd find a more 
        # elegant solution
        for key in self.world_hexes_keys:
            x,y = key
            world_hex = self.world_hexes[key]
            
            biome_options = world_hex.getBiomeOptions()
            if len(biome_options) == 0:
                print(world_hex.getCoastType())
                print(x)
                print(y)
            elif len(biome_options) == 1:
                world_hex.setBiome(biome_options[0])
            elif len(biome_options) >= 2:
                if "tropical desert" in biome_options:
                    biome_options.remove("tropical desert")
                elif "taiga" in biome_options:
                    biome_options.remove("taiga")
                elif "subtropical plains" in biome_options:
                    biome_options.remove("subtropical plains")
                elif "temperate forest" in biome_options:
                    biome_options.remove("temperate forest")
                if len(biome_options) != 3:
                    world_hex.setBiome(biome_options[0])
            
        # Finalizing inland hexes
        for key in self.world_hexes_keys:
            x,y = key
            world_hex = self.world_hexes[key]
            
            biome_options = world_hex.getBiomeOptions()

            if len(biome_options) == 3:
                neighbors = self.getNeighbors(world_hex)
                for neighbor in neighbors:
                    if not neighbor:
                        continue
                    neighbor_biome = neighbor.getBiome()
                    if not neighbor_biome:
                        continue
                    if "desert" in neighbor_biome and "laurentian" in biome_options:
                        biome_options.remove("laurentian")
                    elif "forest" in neighbor_biome and "temperate desert" in biome_options:
                        biome_options.remove("temperate desert")
                if len(biome_options) == 1:
                    world_hex.setBiome(biome_options[0])
                else: 
                    final_biome = np.random.choice(biome_options)
                    world_hex.setBiome(final_biome)
            elif len(biome_options) > 3:
                print(biome_options)
                
        # Adjusting biomes for rain shadows
        for key in self.world_hexes_keys:
            x,y = key
            world_hex = self.world_hexes[key]
            
            if (world_hex.getIsMountainous() or 
                world_hex.getIsHighland()) and world_hex.getElevation()>=4000:
                wind_direction = world_hex.getPrevailingWind()
                direction_index = self.directions.index(wind_direction)
                
                if direction_index + 3 > 5:
                    leeward_index = direction_index - 3
                else:
                    leeward_index = direction_index + 3
                
                leeward_direction = self.directions[leeward_index]
                
                leeward_neighbor = self.getNeighbor(world_hex, leeward_direction)
                if not leeward_neighbor:
                    continue
                
                # Making the leeward neighbor's biome one step drier where possible
                leeward_biome = leeward_neighbor.getBiome()
                leeward_biome_components = leeward_biome.split()
                if "forest" in leeward_biome_components:
                    if "seasonal" in leeward_biome_components:
                        leeward_biome_components.remove("seasonal")
                    leeward_biome_components[1] = "plains"
                elif "plains" in leeward_biome_components:
                    leeward_biome_components[1] = "desert"
                elif "subtropical" in leeward_biome_components:
                    leeward_biome_components = ["tropical", "desert"]
                elif "taiga" in leeward_biome_components:
                    leeward_biome_components = ["temperate", "plains"]
                elif "laurentian" in leeward_biome_components:
                    leeward_biome_components = ["temperate", "plains"]
                elif "chaparral" in leeward_biome_components:
                    leeward_biome_components = ["temperate", "desert"]
                else:
                    continue # Can't make an ocean, desert, or tundra drier
                
                new_leeward_biome = " ".join(leeward_biome_components)
                leeward_neighbor.setBiome(new_leeward_biome)
                
        # Checking for forests next to deserts.
        for key in self.world_hexes_keys:
            x,y = key
            world_hex = self.world_hexes[key]
            
            biome = world_hex.getBiome()
            
            if "forest" in biome or "laurentian" in biome or "taiga" in biome:
                neighbors = self.getNeighbors(world_hex)
                for neighbor in neighbors:
                    if not neighbor:
                        continue
                    neighbor_biome = neighbor.getBiome()
                    # Convert any desert hexes next to a forest hex into plains hexes
                    if "desert" in neighbor_biome:
                        neighbor_biome_components = neighbor_biome.split()
                        neighbor_biome_components.remove("desert")
                        neighbor_biome_components.append("plains")
                        new_neighbor_biome = " ".join(neighbor_biome_components)
                        neighbor.setBiome(new_neighbor_biome)

    def createRiver(self, starting_hex, ending_hex, flow_direction, headwaters=False):
        
        if headwaters:
            starting_hex.setIsHeadwaters()
        
        starting_hex.setRiverOutflow(flow_direction)
        
        flow_index = self.directions.index(flow_direction)
        
        if flow_index + 3 > 5:
            flow_from_direction = self.directions[flow_index-3]
        else:
            flow_from_direction = self.directions[flow_index+3]
            
        ending_hex.setRiverInflow(flow_from_direction)
        
        if not ending_hex.getIsLand() and not ending_hex.getIsLake():
            ending_hex.setWetland("estuary")
        
    def buildRiver(self, world_hex, headwaters=False):
        # Continues building out a river until it hits another river, a wetland
        # with existing outflow, the ocean, or a valley with no lower elevation exit
        
        if not world_hex.getIsLand() and not world_hex.getIsLake():
            return False # Don't build out a river in the ocean
        
        if "icecap" in world_hex.getBiome():
            return False # Don't build out a river where water can't flow
        
        min_elevation = world_hex.getElevation()
        lowest_neighbors = {} # A dict of {neighbor_hex: direction_from_world_hex}
                
        for direction in self.directions:
            neighbor = self.getNeighbor(world_hex, direction)
            if not neighbor:
                continue
            if direction in world_hex.getRiverInflows():
                # Prevents the river from going back on itself
                continue
            if "icecap" in neighbor.getBiome():
                # Prevents rivers pathing where water can't flow
                continue
            if neighbor.getIsHeadwaters():
                # Prevents new rivers from pathing into where another river
                # begins at the same hex level
                continue
            neighbor_elevation = neighbor.getElevation()
            if neighbor_elevation < min_elevation:
                lowest_neighbors = {neighbor: direction,}
                min_elevation = neighbor_elevation
            elif neighbor_elevation == min_elevation:
                lowest_neighbors[neighbor] = direction
                
        # If there's a single neighboring hex of lowest elevation, the river flows there
        if len(lowest_neighbors) == 1:
            chosen_hex = next(iter(lowest_neighbors))
            direction = lowest_neighbors[chosen_hex]
            self.createRiver(world_hex, chosen_hex, direction, headwaters)
            
        # If there's a tie, check how verdant the lowest neighbors are...
        elif len(lowest_neighbors) > 1:
            forest_neighbors = []
            shrub_neighbors = []
            all_lowest_neighbors = list(lowest_neighbors.keys())
            
            for neighbor in lowest_neighbors:
                neighbor_biome = neighbor.getBiome()
                
                if "forest" in neighbor_biome or "laurentian" in neighbor_biome or "taiga" in neighbor_biome:
                    forest_neighbors.append(neighbor)
                    
                elif "plains" in neighbor_biome or "chaparral" in neighbor_biome:
                    shrub_neighbors.append(neighbor)
                    
            # Flow to one of the most verdant hexes, or pick randomly from
            # the lowest hexes.
            if forest_neighbors:
                chosen_hex = np.random.choice(forest_neighbors)
            elif shrub_neighbors:
                chosen_hex = np.random.choice(shrub_neighbors)
            else:
                chosen_hex = np.random.choice(all_lowest_neighbors)
                
            direction = lowest_neighbors[chosen_hex]
            
            self.createRiver(world_hex, chosen_hex, direction, headwaters)
                
        
        # If there are no surrounding hexes with a lower elevation, the river ends.
        # The river either goes underground or forms an endorheic basin.
        else:
            coin_flip = np.random.randint(2)
            if coin_flip == 1:
                #print("Ended in endorheic basin")
                world_hex.setWetland("endorheic basin")
            #print("River stopped")
            return False
        
        # If a new river has been created, check if it hit another river, a wetland
        #  the ocean, or a desert.
        
        if "desert" in chosen_hex.getBiome(): # Good chance the river ends
            chance = np.random.randint(1,101)
            if chance <=90:
                coin_flip = np.random.randint(2)
                if coin_flip == 1:
                    chosen_hex.setWetland("endorheic basin")
                    #print("Ended in endorheic basin")
                #print("River stopped")
                return False
            
        elif "ocean" in chosen_hex.getBiome():
            world_hex.setWetland("estuary")
            chosen_hex.setWetland("estuary")
            #print("River reached the ocean")
            return False # River ends.
            
        if len(chosen_hex.getRiverInflows()) > 1: 
            # There is a confluence. No need to generate new river pathing.
            #print("River formed a confluence")
            #print(chosen_hex.getRiverInflows())
            return False
        
        if chosen_hex.getWetland():
            wetland_type = chosen_hex.getWetland()
            #print("River hit a wetland!!!!!!!!!!!!!!!!!!!!")
            if wetland_type == "endorheic basin":
                #print("Ended in endorheic basin")
                return False # There will be no outflow
            else:
                if chosen_hex.getRiverOutflow():
                    #print("Ended in wetland that already has an outflow!!!!!!!!!!!!!!")
                    return False # The wetland already has an outflow. No need to continue.
        #print("river continues")
        return chosen_hex
        
        # self.directions = ["NE", "E", "SE", "SW", "W", "NW"]
        
    def setResourceSpread(self, resource_name, resource_spread):
        
        # resource_spread should be a tuple of (starting x, ending x)
        
        # Assign resource to first map column
        starting_x = resource_spread[0]
        ending_x = resource_spread[1]
        for y in range(self.num_rows):
            world_hex = self.world_hexes[(starting_x, y)]
            world_hex.assignResource(resource_name)
        
        x = starting_x
        
        # Assign resource across spread until reaching the last column
        while x != ending_x:
            x += 1
            
            # Handles going off edge of map
            if x > self.num_columns - 1:
                x = 0
                
            for y in range(self.num_rows):
                world_hex = self.world_hexes[(x, y)]
                world_hex.assignResource(resource_name)
                
        # Assign resource to last map column
        if starting_x != ending_x: # Skips this step if the resource only exists in one column
            for y in range(self.num_rows):
                world_hex = self.world_hexes[(ending_x, y)]
                world_hex.assignResource(resource_name)
