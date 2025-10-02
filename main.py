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
    print("5) Quit")
    
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
        choice = "quit"
    else:
        print("Not a valid input. Please enter one of the numbers provided below:")