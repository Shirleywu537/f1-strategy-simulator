import random


class Weather:

    def __init__(self, rain_probability=0.05, grip_multiplier=1.08):
        self.condition = "Dry"
        self.rain_probability = rain_probability
        self.grip_multiplier = grip_multiplier

    def update_weather(self):
        chance = random.random()
        if self.condition == "Dry":
            if chance < self.rain_probability:
                self.condition = "Rain"
        else:
            if chance < 0.15:
                self.condition = "Dry"

    def get_grip_multiplier(self):
        if self.condition == "Rain":
            return self.grip_multiplier
        return 1.0