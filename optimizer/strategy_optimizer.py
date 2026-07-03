import copy
import random

from simulator.race import Race
from simulator.strategy import Strategy
from simulator.driver import Driver
from simulator.tire import create_tire


class StrategyOptimizer:

    def __init__(self, track, driver_template, opponents, total_laps, simulations=100):
        self.track = track
        self.driver_template = driver_template
        self.opponents = opponents
        self.total_laps = total_laps
        self.simulations = simulations

    def build_driver(self):
        return Driver(
            name=self.driver_template["name"],
            skill=self.driver_template["skill"],
            consistency=self.driver_template["consistency"],
            tire=create_tire("Soft")
        )

    def build_opponents(self):
        return copy.deepcopy(self.opponents)

    def evaluate_strategy(self, pit_lap, first_compound="Soft", second_compound="Medium"):
        total_time = 0
        for _ in range(self.simulations):
            target_driver = Driver(
                name=self.driver_template["name"],
                race_pace=self.driver_template["race_pace"],
                consistency=self.driver_template["consistency"],
                tire=create_tire(first_compound),
                tire_management=self.driver_template["tire_management"],
                wet_skill=self.driver_template["wet_skill"],
                overtaking=self.driver_template["overtaking"],
                defending=self.driver_template["defending"]
            )

            drivers = [target_driver, *self.build_opponents()]

            strategies = {
                target_driver.name: Strategy(
                    pit_laps=[pit_lap],
                    tire_plan=[first_compound,second_compound]
                )
            }

            for opponent in self.opponents:
                strategies[opponent.name] = Strategy(pit_laps=[5], tire_plan=["Soft", "Medium"])

            race = Race(
                track=self.track,
                drivers=drivers,
                strategies=strategies,
                total_laps=self.total_laps,
                verbose=False
            )

            race.run()
            total_time += target_driver.total_time

        return total_time / self.simulations

    def optimize_one_stop(self, first_compound="Soft", second_compound="Medium", start_lap=2, end_lap=None):

        if end_lap is None:
            end_lap = self.total_laps - 2
        best_time = float("inf")
        best_pit_lap = None
        results = []

        for pit_lap in range(start_lap, end_lap + 1):

            expected_time = self.evaluate_strategy(pit_lap, first_compound, second_compound)
            results.append(
                {
                    "pit_lap": pit_lap,
                    "expected_time": expected_time
                }
            )

            print(
                f"Pit Lap {pit_lap}: "
                f"{expected_time:.2f}s"
            )

            if expected_time < best_time:
                best_time = expected_time
                best_pit_lap = pit_lap

        return {
            "best_pit_lap": best_pit_lap,
            "best_time": best_time,
            "all_results": results
        }