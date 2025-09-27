# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 22:33:21 2025

@author: ame94
"""

import numpy as np

continent_number = np.random.randint(3,8)

loop = continent_number

available_landmass = 522

minimum_size = 30

continent_sizes = []

remaining_continents = continent_number

for continent in range(continent_number):
    maximum_size = available_landmass - (minimum_size * (remaining_continents-1))
    continent_size = np.random.randint(minimum_size, maximum_size+1)
    continent_sizes.append(continent_size)
    remaining_continents -= 1
    available_landmass -= continent_size

last_continent = available_landmass







"""
# Generating continents based on the golden ratio

continent_number = np.random.randint(3,5)

loop = continent_number

x = 0

previous_num = 1

multiplier_list = []

while loop > 0:

    x += previous_num

    multiplier_list.append(x)

    previous_num = x

    loop -= 1

total_multipliers = 0

for number in multiplier_list:
    total_multipliers += number
    
x = math.floor(522/total_multipliers)

continent_sizes = []

for number in multiplier_list:
    continent_size = number * x
    continent_sizes.append(continent_size)
"""