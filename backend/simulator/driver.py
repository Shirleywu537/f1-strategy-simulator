import random

class Driver:
    def __init__(self, name, skill, tire, consistency):
        self.name = name
        self.skill = skill
        self.tire = tire
        self.consistency = consistency
        self.total_time = 0
        self.lap_times = []
        self.position_history = []
        self.wear_history = []

    def drive_lap(self, base_lap_time, grip_multiplier=1.0):
        lap_time = base_lap_time * grip_multiplier - self.tire.pace_bonus - self.skill + self.tire.get_wear_penalty() + random.uniform(-self.consistency, self.consistency)
        self.total_time += lap_time
        self.lap_times.append(lap_time)
        self.tire.degrade()
        self.wear_history.append(self.tire.wear)

        return lap_time
    
    def pit_stop(self, new_tire, pit_time_loss):
        self.tire = new_tire
        self.total_time += pit_time_loss
