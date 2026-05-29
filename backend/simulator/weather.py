import random

class Weather:

    def __init__(self):

        self.condition = "Dry"

    def update_weather(self):

        chance = random.random()

        if self.condition == "Dry":

            if chance < 0.05:
                self.condition = "Rain"

        else:

            if chance < 0.15:
                self.condition = "Dry"

    def get_grip_multiplier(self):

        if self.condition == "Rain":
            return 1.08

        return 1.0