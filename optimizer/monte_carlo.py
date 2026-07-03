import random

from simulator import race
from simulator.tire import create_tire
from simulator.driver import Driver
from simulator.track import Track
from simulator.strategy import Strategy
from simulator.race import Race


def run_monte_carlo(num_simulations=100):

    results = {

        "Verstappen": {
            "wins": 0,
            "total_position": 0
        },

        "Leclerc": {
            "wins": 0,
            "total_position": 0
        },

        "Norris": {
            "wins": 0,
            "total_position": 0
        }
    }

    for sim in range(num_simulations):

        silverstone = Track(
            name="Silverstone",
            base_lap_time=90.0,
            pit_stop_time=22
        )

        drivers = [

            Driver(
                name="Verstappen",
                race_pace=1.00,
                consistency=0.05,
                tire=create_tire("Soft"),
                tire_management=0.98,
                wet_skill=1.08,
                overtaking=1.10,
                defending=1.10
            ),

            Driver(
                name="Leclerc",
                race_pace=0.92,
                consistency=0.12,
                tire=create_tire("Medium"),
                tire_management=1.02,
                wet_skill=0.98,
                overtaking=1.02,
                defending=0.98
            ),

            Driver(
                name="Norris",
                race_pace=0.90,
                consistency=0.10,
                tire=create_tire("Soft"),
                tire_management=1.00,
                wet_skill=1.02,
                overtaking=1.00,
                defending=1.00
            )
        ]

        strategies = {

            "Verstappen": Strategy(
                pit_laps=[5],
                tire_plan=["Soft", "Medium"]
            ),

            "Leclerc": Strategy(
                pit_laps=[4],
                tire_plan=["Medium", "Hard"]
            ),

            "Norris": Strategy(
                pit_laps=[6],
                tire_plan=["Soft", "Hard"]
            )
        }

        race = Race(
            track=silverstone,
            drivers=drivers,
            strategies=strategies,
            total_laps=10,
            verbose=False
        )

        for lap in range(1, race.total_laps + 1):
            race.simulate_lap(lap)

        race.update_standings()
        drivers = race.drivers

        for position, driver in enumerate(drivers, start=1):
            results[driver.name]["total_position"] += position

            if position == 1:
                results[driver.name]["wins"] += 1

    print("\n========== MONTE CARLO RESULTS ==========\n")

    for driver_name, stats in results.items():

        win_rate = (stats["wins"] / num_simulations) * 100

        avg_finish = stats["total_position"] / num_simulations

        print(f"{driver_name}")
        print(f"Win Rate: {win_rate:.2f}%")
        print(f"Average Finish: {avg_finish:.2f}")
        print()

        return [
            {
                "strategy": name,
                "wins": stats["wins"],
                "avg_position": stats["total_position"] / num_simulations
            }
            for name, stats in results.items()
        ]


def run_silent_race(race):

    for lap in range(1, race.total_laps + 1):
        for driver in race.drivers:
            race.process_pit_stop(driver, lap)
            driver.drive_lap(
                race.track.base_lap_time
            )

        race.update_standings()
        race.process_overtakes()