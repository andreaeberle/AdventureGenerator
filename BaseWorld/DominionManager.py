# -*- coding: utf-8 -*-
"""
DominionManager class

"""

import numpy as np

from .Dominion import *

class DominionManager:
    
    def __init__(self):
        
        self.dominions = {} # A dict of {dominion_index: dominion}
        
    def createDominion(self, dominion_index, dominion_type, new_dominion_hexes, 
                       capital_hex, capital_type):
            
        # Setting age
        age_options = ["fledgling", "growing", "stable", "declining", "collapsing"]
        age = np.random.choice(age_options)
        
        # Setting system of government
        government_options = ["monarchy", "oligarchy", "republic"]
        government = np.random.choice(government_options)
            
        # Setting degree of secular vs. religious government
        secularity_options = ["religious", "religion-influenced", "secular"]
        secularity = np.random.choice(secularity_options)
        
        # Setting economic system
        economy_options = ["command", "market", "mixed"]
        economy = np.random.choice(economy_options)
        
        # Setting approach to education
        education_access_options = ["exclusive", "widely accessible"]
        education_access = np.random.choice(education_access_options)
        education_requirement_options = ["optional", "compulsory"]
        education_requirement = np.random.choice(education_requirement_options)
        
        # Setting law and order
        punishment_options = ["banishment", "branding/tattoos", 
                              "community service/indentured servitude", 
                              "corporal punishment", "excommunication/outlawing", 
                              "execution", "fines", "incarceration", "mutilation", 
                              "public humiliation", 
                              "brainwashing/psychological reprogramming"]
        punishments = np.random.choice(punishment_options, size=4, replace=False)
        
        # Setting discrimination levels
        discrimination_levels = {}
        discrimination_areas = ["race", "national origin", "religion", "magic ability", 
                                "age", "class", "disability", "gender", "sexual orientation", 
                                "marital/family status"]
        
        for area in discrimination_areas:
            discrimination_level = round(np.random.uniform(0,10))
            discrimination_levels[area] = discrimination_level
        
        # Setting diplomacy style
        diplomacy_options = ["aggressive", "collaborative", "neutral", "isolationist"]
        diplomacy_style = np.random.choice(diplomacy_options)
        
        # Setting assimilation style
        assimilation_options = ["oppressive", "incentivizing", "neutral", "restricted"]
        assimilation_style = np.random.choice(assimilation_options)
        
        # Setting tax types
        tax_options = ["money", "natural resources", "products", "people"]
        tax_types = np.random.choice(tax_options, size=2, replace=False)
        
        
        new_dominion = Dominion(dominion_index, dominion_type, new_dominion_hexes,
                                capital_hex, capital_type, age, government, secularity, 
                                economy, education_access, education_requirement, 
                                punishments, discrimination_levels, diplomacy_style, 
                                assimilation_style, tax_types)
        
        self.dominions[dominion_index] = new_dominion
        
    def getDominionDetail(self, dominion_index=""):
        
        if not dominion_index:
            dominions = list(self.dominions.values())
            dominion = np.random.choice(dominions)
        
        dominion_detail = dominion.getDetail()
        
        return dominion_detail
    
    def getDiplomacyStyles(self, indexes):
        
        dominion_indexes = []
        if isinstance(indexes, int):
            dominion_indexes.append(indexes)
        else:
            dominion_indexes.extend(indexes)
        
        diplomacy_styles = []
        
        for dominion_index in dominion_indexes:
            dominion = self.dominions[dominion_index]
            dominion_diplomacy_style = dominion.getDiplomacyStyle()
            diplomacy_styles.append(dominion_diplomacy_style)
            
        return diplomacy_styles
    
    def getAges(self, indexes):
        
        dominion_indexes = []
        if isinstance(indexes, int):
            dominion_indexes.append(indexes)
        else:
            dominion_indexes.extend(indexes)   
            
        ages = []
        
        for dominion_index in dominion_indexes:
            dominion = self.dominions[dominion_index]
            dominion_age = dominion.getAge()
            ages.append(dominion_age)
            
        return ages
    
    def getAssimilationStyles(self, indexes):
        
        dominion_indexes = []
        if isinstance(indexes, int):
            dominion_indexes.append(indexes)
        else:
            dominion_indexes.extend(indexes)
        
        assimilation_styles = []
        
        for dominion_index in dominion_indexes:
            dominion = self.dominions[dominion_index]
            dominion_assimilation = dominion.getAssimilationStyle()
            assimilation_styles.append(dominion_assimilation)
            
        return assimilation_styles
    
    def getReligiousTolerances(self, indexes):
        
        dominion_indexes = []
        if isinstance(indexes, int):
            dominion_indexes.append(indexes)
        else:
            dominion_indexes.extend(indexes)
        
        religious_tolerances = []
        
        for dominion_index in dominion_indexes:
            dominion = self.dominions[dominion_index]
            dominion_religious_tolerance = dominion.getReligiousTolerance()
            religious_tolerances.append(dominion_religious_tolerance)
            
        return religious_tolerances
    
    def setWar(self, dominion_indexes):
        
        print(f"The dominions at war are {dominion_indexes}")
        
        for dominion_index in dominion_indexes:
            other_dominion_indexes = dominion_indexes.copy()
            other_dominion_indexes.remove(dominion_index)
            dominion = self.dominions[dominion_index]
            dominion.setWar(other_dominion_indexes)
                        
            print(f"Dominion {dominion_index} is at war with Dominion(s) {other_dominion_indexes}.")

    def setRevolt(self, dominion_index, world_hex):
        
        print(f"Dominion {dominion_index} is experiencing a revolt.")
        
        dominion = self.dominions[dominion_index]
        dominion.setRevolt(world_hex)
