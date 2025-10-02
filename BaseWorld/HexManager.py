# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 20:50:34 2025

@author: ame94
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from collections import Counter

from .WorldHex import *

import numpy as np


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
        
        self.longest_border = ()
        self.biggest_continents = []
    
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
                        
                else:
                    color = "royalblue" # Start with all water tiles being blue
                    if hex_tile.getIsShallows():
                        color = "lightsteelblue"
                    if hex_tile.getIsLake():
                        color = "cornflowerblue"
                    if hex_tile.getIsSeaTrench():
                        color = "midnightblue"

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
                        
                        
            """
                # Delete after plate boundary relationship code has been settled.
                if hex_tile.getPlateBoundaries():
                    if len(hex_tile.getPlateBoundaries()) > 1:
                        if "convergent" in hex_tile.getPlateBoundaries():
                            if "transform" in hex_tile.getPlateBoundaries():
                                if "divergent" in hex_tile.getPlateBoundaries():
                                    color = "black"
                                else:
                                    color = "orange"
                            elif "divergent" in hex_tile.getPlateBoundaries():
                                color = "purple"
                        else:
                            color = "green"
                            
                    else:
                        if "convergent" in hex_tile.getPlateBoundaries():
                            color = "red"
                        elif "transform" in hex_tile.getPlateBoundaries():
                            color = "yellow"
                        elif "divergent" in hex_tile.getPlateBoundaries():
                            color = "blue"
                        else:
                            print("Not sure what's happening...")
                            print(hex_tile.getPlateBoundaries())
                            color = "deeppink"
                            
            if view == "debugging":
                movement_colors = {"NE": "mediumslateblue", "E": "blue", "SE": "aquamarine",
                                   "SW": "olive", "W": "red", "NW": "mediumvioletred"}
                title = "Debugging Plates"
                if hex_tile.getPlateMovement():
                    direction = hex_tile.getPlateMovement()
                    color = movement_colors[direction]
                else:
                    color = "black"
    """        
    
    
