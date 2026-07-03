from dataclasses import dataclass


@dataclass
class TireCompound:
    name: str
    pace_bonus: float
    degradation_rate: float


SOFT = TireCompound("Soft", 1.2, 1.5)
MEDIUM = TireCompound("Medium", 0.6, 1.0)
HARD = TireCompound("Hard", 0.0, 0.7)


class Tire:

    def __init__(self, compound):
        self.compound = compound
        self.pace_bonus = compound.pace_bonus
        self.degradation_rate = compound.degradation_rate
        self.wear = 0

    def degrade(self):
        self.wear += self.degradation_rate

    def get_wear_penalty(self):
        w = self.wear
        if w < 20:
            return 0.02 * w
        elif w < 50:
            return 0.4 + (w-20)*0.05
        else:
            return 1.9 + (w-50)**1.3 * 0.04


def create_tire(name):
    if name == "Soft":
        return Tire(SOFT)
    if name == "Medium":
        return Tire(MEDIUM)
    if name == "Hard":
        return Tire(HARD)
    raise ValueError(f"Unknown tire compound: {name}")