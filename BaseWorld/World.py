"""
World
"""

import random

from .HexManager import *
from .Continent import *
from .TectonicPlate import *
from .BiomeManager import *
from .PlantManager import *
from .CreatureManager import *
from .Dominion import *


class World:
    def __init__(self, all_races, all_biome_dicts, all_flora_dicts, all_fauna_dicts,
                 map_width, map_height):
        self.all_races = all_races
        
        self.oBiomeManager = BiomeManager(all_biome_dicts)
        self.all_biomes = []
        
        self.oHexManager = HexManager()
        self.continents = [] # List of Continent objects
        
        self.oPlantManager = PlantManager(all_flora_dicts)
        self.oCreatureManager = CreatureManager(all_fauna_dicts)

        self.plates = []
        
        self.num_rows = 30
        self.num_columns = 60
        self.world_hexes = self.oHexManager.createWorldHexGrid(self.num_rows, self.num_columns)
        
        self.directions = ["NE", "E", "SE", "SW", "W", "NW"]
        
        self.landmark_hexes = []
        self.dominions = []

    
    def createContinent(self, size):
        continent_index = len(self.continents)
        
        oContinent = Continent(self.oHexManager.createContinent(size, continent_index), 
                               continent_index)
        self.continents.append(oContinent)

    def createPlate(self, size, plate_type, plate_direction):
        plate_index = len(self.plates)
        
        oTectonicPlate = TectonicPlate(self.oHexManager.createPlate(size, plate_type, plate_index),
                                       plate_type, plate_index, plate_direction)
        self.plates.append(oTectonicPlate)
        
        actual_plate_size = oTectonicPlate.getSize()
        
        return actual_plate_size
    
    def establishCoast(self):
        # Makes sure all the land tiles are correctly labeled as coast
        for world_hex in self.world_hexes: 
            self.oHexManager.checkIfLake(world_hex)
            self.oHexManager.checkIfCoast(world_hex)
            self.oHexManager.checkIfShallows(world_hex)
        
    def identifyPlateBoundaries(self):
        # Plates transfer movement to hexes
        for plate in self.plates:
            plate.transferMovement()
            plate.transferType()
        # Identifies the plate boundaries present for each hex
        for world_hex in self.world_hexes:
            if self.oHexManager.checkIfPlateBoundary(world_hex):
                self.oHexManager.setPlateBoundaryType(world_hex)
        # Smoothing out rift valleys
        self.oHexManager.finishRiftValleys()

    def addElevationFlavor(self):
        for world_hex in self.world_hexes:
            chance = np.random.randint(1,101)
            if chance <= 5:
                if world_hex.getIsValley():
                    continue # No change to valleys
                if world_hex.getIsLand() or world_hex.getIsLake():
                    if world_hex.getIsMountainous():
                        self.oHexManager.boostElevation(world_hex,2000)
                    else:
                        self.oHexManager.setElevation(world_hex,"mountains")
                        chance = np.random.randint(1,101)
                        if chance <= 20:
                            world_hex.setIsVolcanic()
                else:
                    world_hex.setIsShallows()
                    chance = np.random.randint(1,101)
                    if chance <= 20:
                        world_hex.setIsVolcanic()
            elif chance > 5 and chance <= 10:
                if world_hex.getIsValley():
                    continue # No change to valleys
                if world_hex.getIsLand() or world_hex.getIsLake():
                    if world_hex.getIsHighland():
                        self.oHexManager.boostElevation(world_hex, 2000)
                    else:
                        self.oHexManager.setElevation(world_hex, "highlands")
            elif chance > 10 and chance <= 20:
                if world_hex.getIsHighland() or world_hex.getIsHilly():
                    continue # No change to higher elevation hexes
                else:
                    if world_hex.getIsLand() or world_hex.getIsLake():
                        self.oHexManager.setElevation(world_hex, "valley")
            # Now add extra hills (running here so that highland hexes might also be hilly)
            chance = np.random.randint(1,101)
            if chance <= 10:
                if world_hex.getIsValley():
                    continue # No change to valleys
                elif world_hex.getIsMountainous():
                    self.oHexManager.boostElevation(world_hex, 1000)
                else:
                    if world_hex.getIsLand() or world_hex.getIsLake():
                        self.oHexManager.setElevation(world_hex, "hills")
                        
    def finishValleys(self):
        for world_hex in self.world_hexes:
            if world_hex.getIsValley() and not world_hex.getIsRiftValley():
                self.oHexManager.finishValley(world_hex)
                        
    def identifyCoastType(self):
        continent_sizes = {} # A dict of {continent index: continent size}
        for continent in self.continents:
            index = continent.getContinentIndex()
            size = continent.getSize()
            continent_sizes[index] = size
        for world_hex in self.world_hexes:
            self.oHexManager.findCoastType(world_hex, continent_sizes)
        self.oHexManager.setAuxiliaryCoastTypes()
                
    def addBiomes(self):   
        # Start by setting prevailing winds, as those will be relevant for biome setting.
        self.oHexManager.setPrevailingWinds(trade_wind_limits=[0,29],
                                            westerlies_limits=[31,60],
                                            easterlies_limits=[61,90])
        
        biome_spreads = self.oBiomeManager.getBiomeSpreads() 
        # Returns a dict of {biome name: {coast type: (minimum latitude, maximum latitude)}}
        biome_applicabilities = self.oBiomeManager.getBiomeApplicabilities()
        # Returns a dict of {biome name: [list of places the biome can exist]}
        
        for biome in biome_spreads:
            biome_name = biome
            biome_spread = biome_spreads[biome] # A dict of {coast type: (minimum latitude, maximum latitude)}
            biome_applicability = biome_applicabilities[biome_name]
            self.oHexManager.applyBiome(biome_name, biome_spread, biome_applicability)
        
        self.oHexManager.finalizeBiomes()
    
    def addWetlands(self):
        # Creates random wetlands that are not assigned a type
        for world_hex in self.world_hexes:
            if not world_hex.getIsLand():
                continue # Hex is already water
            if "icecap" in world_hex.getBiome():
                continue # No surface water exists
            chance_for_biome = np.random.randint(1,101)
            if chance_for_biome <= 6:
                world_hex.setWetland()
                    
    def addRivers(self):
        for world_hex in self.world_hexes:
                        
            world_hex_elevation = world_hex.getElevation()
            
            if "icecap" in world_hex.getBiome():
                continue
            
            if world_hex.getIsRiver() and not world_hex.getIsHeadwaters():
                continue
            
            # Try to start a river if hex hex is a a mountain, highland, or 
            # hilly area with an elevation of at least 4,000 feet
                        
            if (world_hex.getIsHighland() 
                or world_hex.getIsMountainous()) and world_hex_elevation >= 3000:
                                
                for direction in self.directions:
                    neighbor = self.oHexManager.getNeighbor(world_hex, direction)
                    if not neighbor:
                        continue
                    if "desert" in neighbor.getBiome():
                        chance = np.random.randint(1,101)
                        if chance <= 90:
                            continue
                    neighbor_elevation = neighbor.getElevation()
                    if neighbor_elevation < world_hex.getElevation():
                        #self.showMap("rivers")
                        #input("Press any key to start building a river")
                        self.oHexManager.createRiver(world_hex, neighbor, 
                                                     direction, headwaters=True)
                        new_river_hex = neighbor
                        while new_river_hex:
                            newer_river_hex = self.oHexManager.buildRiver(new_river_hex)
                            new_river_hex = newer_river_hex
                
                
                #self.showMap("rivers")
                #input("Press any key to start building a river")
                """
                windward_direction = world_hex.getPrevailingWind()
                windward_neighbor = self.oHexManager.getNeighbor(world_hex, 
                                                                 windward_direction)
                
                windward_neighbor_elevation = windward_neighbor.getElevation()
                
                # Start a river on the windward side if that hex is lower elevation
                if windward_neighbor_elevation < world_hex_elevation and "icecap" not in windward_neighbor.getBiome():
                    self.oHexManager.createRiver(world_hex, windward_neighbor, 
                                                 windward_direction, headwaters=True)
                    if "ocean" in windward_neighbor.getBiome():
                        windward_neighbor.setWetland("estuary")
                        continue # Prevents river pathing beyond the shore
                    new_river_hex = windward_neighbor
                    while new_river_hex:
                        newer_river_hex = self.oHexManager.buildRiver(new_river_hex)
                        new_river_hex = newer_river_hex
                else:
                    # Search for a viable river start options.
                    new_river_hex = self.oHexManager.buildRiver(world_hex,headwaters=True)
                    if new_river_hex:
                        while new_river_hex:
                            newer_river_hex = self.oHexManager.buildRiver(new_river_hex)
                            new_river_hex = newer_river_hex
                    else:
                        # Nowhere for a river to start
                        continue
                """
            elif world_hex.getIsLake():
                #self.showMap("rivers")
                #input("Press any key to start building a river")
                if not world_hex.getRiverOutflow():
                    # Search for a viable river start options.
                    new_river_hex = self.oHexManager.buildRiver(world_hex,headwaters=True)
                    if new_river_hex:
                        while new_river_hex:
                            newer_river_hex = self.oHexManager.buildRiver(new_river_hex)
                            new_river_hex = newer_river_hex
                    else:
                        # Nowhere for a river to start
                        continue
                else:
                    # Don't build out a river from a lake that already has an outflow
                    continue

    def classifyWetlands(self):
        for world_hex in self.world_hexes:
            wetland_options = ["vernal pool", "oasis", "bog", "fen", "marsh", 
                               "swamp", "lake", "endorheic basin"]
            if world_hex.getWetland():
                if world_hex.getWetland() == "unknown":
                    elevation = world_hex.getElevation()
                    is_river = world_hex.getIsRiver()
                    river_inflows = world_hex.getRiverInflows()
                    river_outflow = world_hex.getRiverOutflow()
                    biome = world_hex.getBiome()
                    
                    # Elevation filters
                    if elevation > 1000:
                        wetland_options.remove("oasis")
                        wetland_options.remove("swamp")
                        
                    # River filters
                    if is_river:
                        wetland_options.remove("vernal pool")
                        if "oasis" in wetland_options:
                            wetland_options.remove("oasis")
                        wetland_options.remove("bog")
                    else:
                        wetland_options.remove("marsh")
                        wetland_options.remove("lake")
                        if "swamp" in wetland_options:
                            wetland_options.remove("swamp")

                    
                    if river_inflows:
                        wetland_options.remove("fen")
                        
                    if len(river_inflows) < 2:
                        if "swamp" in wetland_options:
                            wetland_options.remove("swamp")
                        
                    if river_outflow:
                        wetland_options.remove("endorheic basin")
                    
                    else:
                        if "lake" in wetland_options:
                            wetland_options.remove("lake")
                        
                    # Biome filters
                    if "tropical forest" in biome:
                        if "vernal pool" in wetland_options:
                            wetland_options.remove("vernal pool")
                        if "oasis" in wetland_options:
                            wetland_options.remove("oasis")
                        if "bog" in wetland_options:
                            wetland_options.remove("bog")
                        if "fen" in wetland_options:
                            wetland_options.remove("fen")
                        if "marsh" in wetland_options:
                            wetland_options.remove("marsh")
                        
                    elif "tropical seasonal forest" in biome:
                        if "vernal pool" in wetland_options:
                            wetland_options.remove("vernal pool")
                        if "oasis" in wetland_options:
                            wetland_options.remove("oasis")
                        if "bog" in wetland_options:
                            wetland_options.remove("bog")
                        if "fen" in wetland_options:
                            wetland_options.remove("fen")
                        if "marsh" in wetland_options:
                            wetland_options.remove("marsh")
                        
                    elif "subtropical plains" in biome:
                        if "vernal pool" in wetland_options:
                            wetland_options.remove("vernal pool")
                        if "oasis" in wetland_options:
                            wetland_options.remove("oasis")
                        if "bog" in wetland_options:
                            wetland_options.remove("bog")
                        if "fen" in wetland_options:
                            wetland_options.remove("fen")
                        if "swamp" in wetland_options:
                            wetland_options.remove("swamp")
                        
                    elif "tropical plains" in biome:
                        if "vernal pool" in wetland_options:
                            wetland_options.remove("vernal pool")
                        if "oasis" in wetland_options:
                            wetland_options.remove("oasis")
                        if "bog" in wetland_options:
                            wetland_options.remove("bog")
                        if "fen" in wetland_options:
                            wetland_options.remove("fen")
                        if "swamp" in wetland_options:
                            wetland_options.remove("swamp")
                            
                    elif "tropical desert" in biome:
                        if "bog" in wetland_options:
                            wetland_options.remove("bog")
                        if "fen" in wetland_options:
                            wetland_options.remove("fen")
                        if "marsh" in wetland_options:
                            wetland_options.remove("marsh")
                        if "swamp" in wetland_options:
                            wetland_options.remove("swamp")
                        
                    elif "chaparral" in biome:
                        if "oasis" in wetland_options:
                            wetland_options.remove("oasis")
                        if "bog" in wetland_options:
                            wetland_options.remove("bog")
                        if "fen" in wetland_options:
                            wetland_options.remove("fen")
                        if "marsh" in wetland_options:
                            wetland_options.remove("marsh")
                        if "swamp" in wetland_options:
                            wetland_options.remove("swamp")
                        
                    elif "temperate desert" in biome:
                        if "bog" in wetland_options:
                            wetland_options.remove("bog")
                        if "fen" in wetland_options:
                            wetland_options.remove("fen")
                        if "marsh" in wetland_options:
                            wetland_options.remove("marsh")
                        if "swamp" in wetland_options:
                            wetland_options.remove("swamp")
                        
                    elif "temperate plains" in biome:
                        if "oasis" in wetland_options:
                            wetland_options.remove("oasis")
                        if "bog" in wetland_options:
                            wetland_options.remove("bog")
                        if "swamp" in wetland_options:
                            wetland_options.remove("swamp")
                        
                    elif "temperate seasonal forest" in biome:
                        if "vernal pool" in wetland_options:
                            wetland_options.remove("vernal pool")
                        if "oasis" in wetland_options:
                            wetland_options.remove("oasis")
                        if "marsh" in wetland_options:
                            wetland_options.remove("marsh")
                        
                    elif "temperate forest" in biome:
                        if "vernal pool" in wetland_options:
                            wetland_options.remove("vernal pool")
                        if "oasis" in wetland_options:
                            wetland_options.remove("oasis")
                        if "marsh" in wetland_options:
                            wetland_options.remove("marsh")
                        
                    elif "laurentian" in biome:
                        if "vernal pool" in wetland_options:
                            wetland_options.remove("vernal pool")
                        if "oasis" in wetland_options:
                            wetland_options.remove("oasis")
                        if "marsh" in wetland_options:
                            wetland_options.remove("marsh")
                        if "swamp" in wetland_options:
                            wetland_options.remove("swamp")
                        
                    elif "taiga" in biome:
                        if "vernal pool" in wetland_options:
                            wetland_options.remove("vernal pool")
                        if "oasis" in wetland_options:
                            wetland_options.remove("oasis")
                        if "marsh" in wetland_options:
                            wetland_options.remove("marsh")
                        if "swamp" in wetland_options:
                            wetland_options.remove("swamp")
                        
                    elif "tundra" in biome:
                        if "oasis" in wetland_options:
                            wetland_options.remove("oasis")
                        if "bog" in wetland_options:
                            wetland_options.remove("bog")
                        if "marsh" in wetland_options:
                            wetland_options.remove("marsh")
                        if "swamp" in wetland_options:
                            wetland_options.remove("swamp")
                            
                    if len(wetland_options) == 0:
                        print("No possible wetland :(")
                        print("Elevation =", elevation)
                        print("River status =", is_river)
                        print("River inflows =", river_inflows)
                        print("River outflow =", river_outflow)
                        print("Biome =", biome)
                    else:
                        wetland_type = np.random.choice(wetland_options)
                        world_hex.setWetland(wetland_type)

    def addResourceSpreads(self):
        # Creates a dict of {plant name: (starting x, ending x)}
        plant_spreads = self.oPlantManager.assignSpreads(self.num_columns)
        creature_spreads = self.oCreatureManager.assignSpreads(self.num_columns)
        
        for plant in plant_spreads:
            plant_name = plant
            plant_spread = plant_spreads[plant]
            self.oHexManager.setResourceSpread(plant_name, plant_spread)
            
        for creature in creature_spreads:
            creature_name = creature
            creature_spread = creature_spreads[creature]
            self.oHexManager.setResourceSpread(creature_name, creature_spread)

    def addLandmarks(self):
        # Assigns landmark locations across the world map
        
        for world_hex in self.world_hexes:
            if not world_hex.getIsLand():
                if world_hex.getIsShallows():
                    landmark_chance = 15
                else:
                    landmark_chance = 1
           
            else:
                world_hex_biome = world_hex.getBiome()
                
                if world_hex_biome == "icecap":
                    landmark_chance = 1
                elif world_hex.getWetland() == "estuary":
                    if "temperate" in world_hex_biome or "chaparral" in world_hex_biome:
                        landmark_chance = 35
                    elif "tropical" in world_hex_biome or "subtropical" in world_hex_biome:
                        landmark_chance = 30
                    else:
                        landmark_chance = 25
                elif world_hex.getIsCoast():
                    if "temperate" in world_hex_biome or "chaparral" in world_hex_biome:
                        landmark_chance = 25
                    elif "tropical" in world_hex_biome or "subtropical" in world_hex_biome:
                        landmark_chance = 20
                    else:
                        landmark_chance = 15
                else:
                    if "temperate" in world_hex_biome:
                        landmark_chance = 20
                    elif "tropical" in world_hex_biome:
                        landmark_chance = 15
                    else:
                        landmark_chance = 10
                
                if world_hex.getIsRiver():
                    landmark_chance += 5
                
                if (
                        "desert" in world_hex_biome or 
                        "forest" in world_hex_biome or 
                        world_hex.getIsMountainous() or
                        "bog" in world_hex.getWetland() or
                        "fen" in world_hex.getWetland() or
                        "marsh" in world_hex.getWetland() or
                        "swamp" in world_hex.getWetland()
                        ):
                    landmark_chance -= 5
                    
                if world_hex.getIsRiver():
                    landmark_chance += 5
            
            # Generate random number 1-100 to determine if a landmark will be placed.
            landmark_roll = np.random.randint(1,101)
            
            if landmark_roll <= landmark_chance:
                # Determine what type of landmark is there
                landmark_type_roll = np.random.randint(1,8)
                if landmark_type_roll == 1:
                    landmark_type = "city"
                elif landmark_type_roll == 2:
                    landmark_type = "military fortress"
                elif landmark_type_roll == 3:
                    landmark_type = "religious site"
                elif landmark_type_roll == 4:
                    landmark_type = "center of learning"
                elif landmark_type_roll == 5:
                    landmark_type = "monster lair"
                elif landmark_type_roll == 6:
                    landmark_type = "natural wonder"
                else:
                    landmark_type = "ruin"
                
                world_hex.setLandmark(landmark_type)

                self.landmark_hexes.append(world_hex)
    
    def addDominions(self):
        
        # Go through all landmark locations and start a dominion at every civilized landmark
        
        dominion_index = 0
        
        for landmark_hex in self.landmark_hexes:
            landmark_type = landmark_hex.getLandmark()
            if (
                    "city" in landmark_type or
                    "fortress" in landmark_type or
                    "site" in landmark_type or
                    "center" in landmark_type
                    ):
                # If it's a civilized landmark, start a dominion there (unless it's
                # already been claimed by another dominion).
                # Determine whether the dominion will be an empire, great kingdom,
                # or good kingdom.
                
                if landmark_hex.getDominionIndex():
                    continue # Skip landmark if it's already in a dominion
                
                dominion_type_roll = np.random.randint(1, 101)
                if dominion_type_roll <= 17:
                    dominion_type = "empire"
                    # Determine size
                    dominion_size = np.random.randint(11, 21)
                elif dominion_type_roll <= 50:
                    dominion_type = "great kingdom"
                    # Determine size
                    dominion_size = np.random.randint(3, 11)
                else:
                    dominion_type = "good kingdom"
                    # Determine size
                    dominion_size = np.random.randint(1,3)
                    
                # Start the dominion as the landmark hex or encircling the landmark hex
                
                new_dominion_hexes = [landmark_hex]
                dominion_landmarks = 1
                
                if dominion_size >= 7:
                    neighbor_hexes = self.oHexManager.getNeighbors(landmark_hex)
                    
                    for neighbor in neighbor_hexes:
                        
                        if not neighbor:
                            continue
                        
                        if neighbor.getLandmark():
                            if dominion_type == "good kingdom":
                                continue # Can't accept another landmark
                            elif dominion_type == "great kingdom" and dominion_landmarks >= 2:
                                continue # Can't accept more landmarks
                        
                        if (
                                not neighbor.getIsLand() and 
                                not neighbor.getIsShallows() and
                                landmark_hex.getIsLand()):
                            continue # Can't accept a deep ocean tile unless the landmark
                                    # hex is on a deep ocean tile
                                    
                        if neighbor.getDominionIndex():
                            coin_flip = np.random.randint(0,2)
                            if coin_flip == 0:
                                continue # 50/50 chance of expanding to a claimed tile
                                    
                        # Only viable additions will make it to this part of the code
                        new_dominion_hexes.append(neighbor)
                        if neighbor.getLandmark():
                            dominion_landmarks += 1
                    
                # Build out the dominion until it reaches the correct size
                                
                was_expansion = True
                
                while (len(new_dominion_hexes) < dominion_size) and was_expansion:
                    
                    was_expansion = False
                    
                    # Shuffle the list of dominion hexes
                    random.shuffle(new_dominion_hexes)
                                        
                    for world_hex in new_dominion_hexes:
                        
                        if len(new_dominion_hexes) >= dominion_size:
                            break
                    
                        hex_neighbors = self.oHexManager.getNeighbors(world_hex)
                        perimeter = False
                        
                        for neighbor in hex_neighbors:
                            
                            if not neighbor:
                                continue
                            
                            if not neighbor in new_dominion_hexes:
                                # The hex is a perimeter hex
                                perimeter = True
                                break
                        
                        if perimeter == True:
                            expansion_options = []
                            best_expansion_value = -1000
                            
                            # Check how viable each neighbor is for dominion expansion
                            for neighbor in hex_neighbors:
                                
                                if not neighbor:
                                    continue
                                
                                if neighbor in new_dominion_hexes:
                                    continue
                                
                                expansion_value = 0
                                
                                if neighbor.getLandmark():
                                    if dominion_type == "good kingdom":
                                        continue # Can't accept another landmark
                                    elif (dominion_type == "great kingdom" and 
                                          dominion_landmarks >= 2):
                                        continue # Can't accept more landmarks
                                
                                if (
                                        not neighbor.getIsLand() and 
                                        not neighbor.getIsShallows() and
                                        landmark_hex.getIsLand()
                                        ):
                                    continue # Can't accept a deep ocean tile unless the 
                                            # landmark hex is on a deep ocean tile
                                            
                                if (
                                        (neighbor.getIsHilly() or
                                        neighbor.getIsHighland() or
                                        neighbor.getIsMountainous()) and
                                        (not landmark_hex.getIsHilly() and
                                         not landmark_hex.getIsHighland() and
                                         not landmark_hex.getIsMountainous())
                                        ):
                                    expansion_value -= 30
                                    
                                if neighbor.getBiome() == world_hex.getBiome():
                                    expansion_value += 40
                                    
                                if neighbor.getIsCoast():
                                    expansion_value += 40
                                    
                                if (
                                        ("desert" in neighbor.getBiome() or
                                        "taiga" in neighbor.getBiome() or
                                        "tundra" in neighbor.getBiome() or
                                        "forst" in neighbor.getBiome()) and
                                        neighbor.getBiome() != world_hex.getBiome()
                                        ):
                                    expansion_value -= 20
                                    
                                if ("icecap" in neighbor.getBiome() and 
                                    neighbor.getBiome() != world_hex.getBiome()):
                                    expansion_value -= 100
                                    
                                if neighbor.getDominionIndex():
                                    expansion_value -= 40
                                    
                                if expansion_value > best_expansion_value:
                                    expansion_options = [neighbor]
                                    best_expansion_value = expansion_value
                                    
                                elif expansion_value == best_expansion_value:
                                    expansion_options.append(neighbor)
                            
                            # After all neighbors have been screened...
                            
                            if len(expansion_options) == 1:
                                new_dominion_hexes.append(expansion_options[0])
                                was_expansion = True
                                if expansion_options[0].getLandmark():
                                    dominion_landmarks += 1
                                
                            elif len(expansion_options) > 1:
                                new_hex = np.random.choice(expansion_options)
                                new_dominion_hexes.append(new_hex)
                                was_expansion = True
                                if new_hex.getLandmark():
                                    dominion_landmarks += 1
                                
                if len(new_dominion_hexes) < dominion_size:
                    # If there's nowhere to expand but the dominion hasn't reached its
                    # full size yet, adjust its type if necessary.
                    
                    if 3 <= len(new_dominion_hexes) <= 10:
                        dominion_type = "great kingdom"
                        
                    elif len(new_dominion_hexes) <= 2:
                        dominion_type = "good kingdom"
                
                new_dominion = Dominion(dominion_index, dominion_type, new_dominion_hexes)
                for world_hex in new_dominion_hexes:
                    world_hex.setDominionIndex(dominion_index)
                    
                self.dominions.append(new_dominion)
                
                dominion_index += 1
                
        print(len(self.dominions))        

    def showMap(self, view):
        self.oHexManager.drawWorldHexGrid(view)
