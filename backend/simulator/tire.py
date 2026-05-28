class Tire:
    def __init__(self, compound, pace_bonus, degradation_rate):
        self.compound = compound
        self.pace_bonus = pace_bonus
        self.degradation_rate = degradation_rate
        self.wear = 0

    def degrade(self):
        self.wear += self.degradation_rate

    def get_wear_penalty(self):
        return self.wear * 0.05
    
def create_tire(compound):

    if compound == "Soft":
        return Tire(
            compound="Soft",
            pace_bonus=1.2,
            degradation_rate=1.5
        )

    elif compound == "Medium":
        return Tire(
            compound="Medium",
            pace_bonus=0.6,
            degradation_rate=1.0
        )

    elif compound == "Hard":
        return Tire(
            compound="Hard",
            pace_bonus=0.0,
            degradation_rate=0.7
        )

    else:
        raise ValueError("Invalid tire compound")