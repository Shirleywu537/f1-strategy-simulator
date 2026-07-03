import random


class Driver:

    def __init__(self, name, race_pace, consistency, tire, qualifying_pace=0.0, tire_management=1.0, 
            wet_skill=1.0, overtaking=1.0, defending=1.0):
        self.name = name
        self.race_pace = race_pace
        self.qualifying_pace = qualifying_pace
        self.consistency = consistency
        self.tire_management = tire_management
        self.wet_skill = wet_skill
        self.overtaking = overtaking
        self.defending = defending
        self.tire = tire
        self.total_time = 0.0
        self.lap_times = []
        self.position_history = []
        self.wear_history = []
        self.current_position = None
        self.finished = True
        self.fuel_load = 1.0

    # -------------------------
    # MAIN LAP SIMULATION
    # -------------------------

    def drive_lap(self, base_lap_time, weather_multiplier=1.0, is_raining=False, safety_car=False):
        lap_time = base_lap_time

        # -------------------------
        # Driver Pace
        # -------------------------

        lap_time -= self.race_pace

        # -------------------------
        # Tire Pace
        # -------------------------

        lap_time -= self.tire.pace_bonus

        # -------------------------
        # Tire Wear
        # -------------------------

        lap_time += self.tire.get_wear_penalty()

        # -------------------------
        # Dirty air
        # -------------------------
        if self.current_position is not None:
            lap_time += 0.10

        # -------------------------
        # Rain Adjustment
        # -------------------------

        if is_raining:
            lap_time /= self.wet_skill
            self.tire.wear += 0.3

        # -------------------------
        # Weather
        # -------------------------

        lap_time *= weather_multiplier

        # -------------------------
        # Safety Car
        # -------------------------

        if safety_car: lap_time *= 1.15

        # -------------------------
        # Randomness
        # -------------------------

        lap_time += random.gauss(0, self.consistency)

        # -------------------------
        # Update Race State
        # -------------------------

        self.total_time += lap_time
        self.lap_times.append(lap_time)
        self.tire.wear += self.tire.degradation_rate * self.tire_management
        self.wear_history.append(self.tire.wear)

        # -------------------------
        # Fuel effect
        # -------------------------

        fuel_penalty = self.fuel_load * 1.5
        lap_time += fuel_penalty
        self.fuel_load -= 1 / 60
        self.fuel_load = max(self.fuel_load, 0.3)
        return lap_time

    # -------------------------
    # PIT STOP
    # -------------------------

    def pit_stop(self, new_tire, pit_time_loss):
        self.tire = new_tire
        multiplier = 1.0

        if hasattr(self, "pit_multiplier"): multiplier = self.pit_multiplier
        self.total_time += pit_time_loss * multiplier

    # -------------------------
    # DNF
    # -------------------------

    def retire(self):
        self.finished = False
        self.total_time = float("inf")

    # -------------------------
    # STATS
    # -------------------------

    @property
    def average_lap(self):
        if not self.lap_times:
            return None
        return sum(self.lap_times) / len(self.lap_times)

    @property
    def best_lap(self):
        if not self.lap_times:
            return None
        return min(self.lap_times)

    @property
    def worst_lap(self):
        if not self.lap_times:
            return None
        return max(self.lap_times)

    # -------------------------
    # STRING
    # -------------------------

    def __repr__(self):
        return f"Driver("f"{self.name}, "f"time={self.total_time:.2f}"f")"