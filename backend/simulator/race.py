from simulator.weather import Weather
from simulator.tire import create_tire
import random

class Race:

    def __init__(
        self,
        track,
        drivers,
        strategies,
        total_laps,
        verbose=True
    ):

        self.track = track
        self.drivers = drivers
        self.strategies = strategies
        self.total_laps = total_laps
        self.verbose = verbose
        self.weather = Weather()
        self.safety_car_active = False
        self.safety_car_laps_remaining = 0

    def process_pit_stop(self, driver, lap):

        strategy = self.strategies[driver.name]

        if lap in strategy.pit_laps:

            pit_index = (
                strategy.pit_laps.index(lap) + 1
            )

            next_compound = (
                strategy.tire_plan[pit_index]
            )

            new_tire = create_tire(next_compound)

            driver.pit_stop(
                new_tire,
                self.track.pit_stop_time
            )

            if self.verbose:
                print(
                f"{driver.name} pits for "
                f"{new_tire.compound} tires "
                f"(+{self.track.pit_stop_time}s)"
            )

    def process_overtakes(self):

        if self.safety_car_active:
            return

        for i in range(len(self.drivers) - 1):

            front_driver = self.drivers[i]
            behind_driver = self.drivers[i + 1]

            gap = (
                behind_driver.total_time
                - front_driver.total_time
            )

            if gap < 1.0:

                last_front_lap = (
                    front_driver.lap_times[-1]
                )

                last_behind_lap = (
                    behind_driver.lap_times[-1]
                )

                pace_advantage = (
                    last_front_lap
                    - last_behind_lap
                )

                if pace_advantage > 0.5:

                    self.drivers[i], self.drivers[i + 1] = (
                        self.drivers[i + 1],
                        self.drivers[i]
                    )

                    if self.verbose:
                        print(
                        f"OVERTAKE: "
                        f"{behind_driver.name} passes "
                        f"{front_driver.name}"
                    )

    def update_standings(self):

        self.drivers.sort(
            key=lambda d: d.total_time
        )

        if self.safety_car_active:

            leader_time = self.drivers[0].total_time

            for driver in self.drivers[1:]:

                gap = (
                    driver.total_time
                    - leader_time
                )

                compressed_gap = gap * 0.85

                driver.total_time = (
                    leader_time
                    + compressed_gap
                )


    def print_standings(self, lap):

        if not self.verbose:
            return

        print(f"\n--- Standings After Lap {lap} ---")

        for position, driver in enumerate(
            self.drivers,
            start=1
        ):

            driver.position = position

            driver.position_history.append(
                position
            )

            print(
                f"{position}. "
                f"{driver.name:12} "
                f"{driver.total_time:.2f}s"
            )

    def update_safety_car(self):
        if self.safety_car_active:

            self.safety_car_laps_remaining -= 1

            if self.safety_car_laps_remaining <= 0:

                self.safety_car_active = False

                if self.verbose:
                    print("\nSAFETY CAR ENDED\n")

            return

        chance = random.random()

        # 5% chance
        if chance < 0.05:

            self.safety_car_active = True

            self.safety_car_laps_remaining = 2

            if self.verbose:
                print("\nSAFETY CAR DEPLOYED\n")


    def simulate_lap(self, lap):

        self.weather.update_weather()

        self.update_safety_car()

        if self.verbose:
            print(f"\n========== LAP {lap} ==========\n")

        if self.verbose:
            print(
                f"Weather: "
                f"{self.weather.condition}"
            )

        if self.safety_car_active and self.verbose:
            print("SAFETY CAR ACTIVE")

        safety_car_multiplier = 1.0

        if self.safety_car_active:
            safety_car_multiplier = 1.15

        for driver in self.drivers:

            self.process_pit_stop(driver, lap)

            lap_time = driver.drive_lap(
                self.track.base_lap_time,
                self.weather.get_grip_multiplier() * safety_car_multiplier
            )

            
            if self.verbose:
                print(
                    f"{driver.name:12} | "
                    f"Lap Time: {lap_time:.2f}s | "
                    f"Tire: {driver.tire.compound:6} | "
                    f"Wear: {driver.tire.wear:.2f} | "
                    f"Total: {driver.total_time:.2f}s"
            )

        self.update_standings()
        
        self.process_overtakes()
        
        self.update_standings()

        self.print_standings(lap)


    def run(self):

        if self.verbose:
            print(
                f"\n=== "
                f"{self.track.name} Race Simulation "
                f"===\n"
            )

        for lap in range(
            1,
            self.total_laps + 1
        ):

            self.simulate_lap(lap)

        if self.verbose:
            print("\n========== FINAL RESULTS ==========\n")

            for position, driver in enumerate(
                self.drivers,
                start=1
            ):

                print(
                    f"{position}. "
                    f"{driver.name:12} "
                    f"{driver.total_time:.2f}s"
                )