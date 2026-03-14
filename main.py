"""
Created on Wed Jun 18 13:42:53 2025

@author: ame94
"""
from BaseWorld.GameMaster import *

oGameMaster = GameMaster()
oGameMaster.startNewWorld() 
#oGameMaster.startAdventure() # Muting until I can straighten out world building mechanics

# A loop that allows user to switch between map views
choice = "continue"
while choice != "quit":
    print("Map Views:")
    print("1) Land Masses")
    print("2) Continents")
    print("3) Plate Tectonics")
    print("4) Geographic Features")
    print("5) Topography")
    print("6) Biomes")
    print("7) Rivers/Wetlands")
    print("8) Debugging Resources")
    print("9) Landmarks")
    print("10) Dominions")
    print("11) Conflicts")
    print("12) Describe a Random Hex")
    print("13) Quit")
    
    choice = input("What would you like to view? Enter number: ")
    if choice == "1":
        oGameMaster.showMap("land")
    elif choice == "2":
        oGameMaster.showMap("continents")
    elif choice == "3":
        oGameMaster.showMap("plates")
    elif choice == "4":
        oGameMaster.showMap("geography")
    elif choice == "5":
        oGameMaster.showMap("topography")
    elif choice == "6":
        oGameMaster.showMap("biomes")
    elif choice == "7":
        oGameMaster.showMap("rivers")
    elif choice == "8":
        oGameMaster.showMap("debug resources")
    elif choice == "9":
        oGameMaster.showMap("landmarks")
    elif choice == "10":
        oGameMaster.showMap("dominions")
    elif choice == "11":
        oGameMaster.showMap("conflicts")
    elif choice == "12":
        oGameMaster.showMap("random hex")
    elif choice == "13":
        choice = "quit"
    else:
        print("Not a valid input. Please enter one of the numbers provided below:")