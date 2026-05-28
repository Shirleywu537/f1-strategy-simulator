import random


class Weather:

    def __init__(self):

        self.condition = "Dry"

    def update_weather(self):

        chance = random.random()

        # 10% chance to rain
        if chance < 0.10:
            self.condition = "Rain"

        # 10% chance to dry up
        elif chance < 0.20:
            self.condition = "Dry"

    def get_grip_multiplier(self):

        if self.condition == "Rain":
            return 1.08

        return 1.0