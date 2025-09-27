# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 19:09:36 2025

@author: ame94
"""

import json

fname = r"C:\Users\ame94\.spyder-py3\Adventure Generator\WorldPrimera\Races\elf_config.json"

with open(fname,'r') as file:
    data = json.load(file)
print(data["elf"])

fname = r"C:\Users\ame94\.spyder-py3\Adventure Generator\WorldPrimera\Races\human_config.json"

with open(fname,'r') as file:
    data = json.load(file)
print(data["human"])