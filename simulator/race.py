import random

from simulator.weather import Weather
from simulator.tire import create_tire


class Race:

    def __init__(self, track, drivers, strategies, total_laps, weather=None, verbose=True):
        self.track = track
        self.drivers = drivers
        self.strategies = strategies
        self.total_laps = total_laps
        self.verbose = verbose
        self.weather = weather or Weather()
        self.safety_car_active = False
        self.safety_car_laps_remaining = 0

    # -------------------------
    # PIT STOPS
    # -------------------------

    def process_pit_stop(self, driver, lap):
        strategy = self.strategies.get(driver.name)
        if strategy is None:
            return
        if lap not in strategy.pit_laps:
            return
        pit_index = strategy.pit_laps.index(lap) + 1

        if pit_index >= len(strategy.tire_plan):
            return

        next_compound = strategy.tire_plan[pit_index]

        new_tire = create_tire(next_compound)

        driver.pit_stop(new_tire, self.track.pit_stop_time)

        if self.verbose:
            print(f"{driver.name} PIT → "f"{next_compound}")

    # -------------------------
    # SAFETY CAR
    # -------------------------

    def update_safety_car(self):
        if self.safety_car_active:
            self.safety_car_laps_remaining -= 1
            if self.safety_car_laps_remaining <= 0:
                self.safety_car_active = False
                if self.verbose:
                    print("\nSAFETY CAR ENDED\n")
            return

        chance = random.random()

        if chance < self.track.safety_car_probability:
            self.safety_car_active = True
            self.safety_car_laps_remaining = 2

            if self.verbose:
                print("\nSAFETY CAR DEPLOYED\n")

    # -------------------------
    # OVERTAKING
    # -------------------------

    def process_overtakes(self):
        if self.safety_car_active:
            return
        for i in range(len(self.drivers) - 1):
            front = self.drivers[i]
            back = self.drivers[i + 1]

            gap = back.total_time - front.total_time
 
            if gap > 1.2: continue

            front_lap = front.lap_times[-1]

            back_lap = back.lap_times[-1]

            pace_delta = front_lap - back_lap

            prob = 0.35 * back.overtaking / max(0.1, front.defending)
            prob *= max(0.0, pace_delta)

            if random.random() < prob:
                self.drivers[i], self.drivers[i + 1] = back, front

                if self.verbose:
                    print(f"{back.name}"f" passes "f"{front.name}")

    # -------------------------
    # STANDINGS
    # -------------------------

    def update_standings(self):
        self.drivers.sort(key=lambda d: d.total_time)

        if self.safety_car_active:
            leader_time = self.drivers[0].total_time

            for driver in self.drivers[1:]:
                gap = driver.total_time - leader_time

                compressed_gap = gap * 0.85

                driver.total_time = leader_time + compressed_gap

    # -------------------------
    # SINGLE LAP
    # -------------------------

    def simulate_lap(self, lap):
        self.weather.update_weather()
        self.update_safety_car()
        weather_multiplier = self.weather.get_grip_multiplier()

        if self.safety_car_active:
            weather_multiplier *= 1.15

        if self.verbose:
            print(f"\n===== LAP {lap} =====")

            print(f"Weather: "f"{self.weather.condition}")

        leader = self.drivers[0]
        pit_multiplier = 1.0

        if self.safety_car_active:
            pit_multiplier = 0.55

        for d in self.drivers:
            d.pit_multiplier = pit_multiplier

        for driver in self.drivers:
            self.process_pit_stop(driver, lap)

            is_behind_car = (driver != leader)

            lap_time = driver.drive_lap(
                self.track.base_lap_time,
                weather_multiplier,
                is_raining=(self.weather.condition == "Rain"),
                safety_car=self.safety_car_active
            )

            if is_behind_car:
                lap_time += 0.12
                driver.total_time += 0.12

            if self.verbose:
                print(
                    f"{driver.name:12}"
                    f" "
                    f"{lap_time:.2f}s "
                    f"| "
                    f"{driver.tire.compound}"
                )

        self.update_standings()
        self.process_overtakes()
        self.update_standings()
        self.record_positions()

    # -------------------------
    # POSITION HISTORY
    # -------------------------

    def record_positions(self):
        for position, driver in enumerate(self.drivers, start=1):

            driver.position_history.append(position)
        driver.current_position = position

    # -------------------------
    # RACE LOOP
    # -------------------------

    def run(self):
        if self.verbose:
            print(f"\n=== "f"{self.track.name}"f" ===\n")

        for lap in range(1, self.total_laps + 1):
            self.simulate_lap(lap)

        self.update_standings()
        return self.drivers

    # -------------------------
    # RESULTS
    # -------------------------

    def get_results(self):
        self.update_standings()
        results = []
        for position, driver in enumerate(self.drivers,start=1):

            results.append({
                "position":
                    position,
                "driver":
                    driver.name,
                "total_time":
                    driver.total_time,
                "avg_lap":
                    sum(driver.lap_times)
                    / len(driver.lap_times)
            })

        return results