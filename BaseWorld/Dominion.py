"""
Dominion class
"""

class Dominion:
    
    def __init__(self, dominion_index, dominion_type, hex_list, capital_hex, 
                 capital_type, age, government, secularity, economy, education_access, 
                 education_requirement, punishments, discrimination_levels, 
                 diplomacy_style, assimilation_style, tax_types):

        self.index = dominion_index        
        self.type = dominion_type
        self.hexes = hex_list
        self.capital_hex = capital_hex
        self.capital_type = capital_type
        self.age = age

        self.government = government
        self.secularity = secularity
        self.economy = economy
        
        self.education_access = education_access
        self.education_requirement = education_requirement
        
        self.demographics = {}
        
        self.religions = []
        
        self.punishments = punishments
        
        self.discrimination_levels = discrimination_levels
        
        self.diplomacy_style = diplomacy_style
        self.assimilation_style = assimilation_style
        self.tax_types = tax_types
        
        self.war_opponents = []
        self.revolts = [] # List of world hexes in active revolt
        
    def getDetail(self):
        
        detail = f"""
        Dominion {self.index} is a {self.age} {self.type}. Its capital is a {self.capital_type}.
        The dominion is ruled by a {self.secularity} {self.government} and operates a 
        {self.economy} economy. Education in the dominion is {self.education_requirement} 
        and {self.education_access}. The rule of law is maintained by threat of the 
        following punishments: 
        {self.punishments}.
        
        The dominion discriminates in the following areas to the listed degree:
        {self.discrimination_levels}
        
        The dominion takes a(n) {self.diplomacy_style} approach to diplomacy and has
        been {self.assimilation_style} in its assimilation across recently conquered areas.
        The dominion extracts taxes from its citizens in the form of 
        {self.tax_types[0]} and {self.tax_types[1]}.
        """
        
        return detail
    
    def getDiplomacyStyle(self):
        return self.diplomacy_style
    
    def getAssimilationStyle(self):
        return self.assimilation_style
    
    def getReligiousTolerance(self):
        religious_discrimination = self.discrimination_levels["religion"]
        if religious_discrimination <= 2:
            religious_tolerance = "tolerant"
        elif religious_discrimination <= 5:
            religious_tolerance = "somewhat tolerant"
        elif religious_discrimination <= 8:
            religious_tolerance = "somewhat intolerant"
        else:
            religious_tolerance = "strictly intolerant"
        return religious_tolerance
    
    def getAge(self):
        return self.age
    
    def setWar(self, enemy_indexes):
        for enemy_index in enemy_indexes:
            if enemy_index not in self.war_opponents:
                self.war_opponents.append(enemy_index)

    def setRevolt(self, world_hex):
        self.revolts.append(world_hex)