import random

from simulator.tire import create_tire
from simulator.driver import Driver
from simulator.track import Track
from simulator.strategy import Strategy
from simulator.race import Race


def run_monte_carlo(num_simulations=100):

    # Store statistics
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

        # Create track
        silverstone = Track(
            name="Silverstone",
            base_lap_time=90.0,
            pit_stop_time=22
        )

        # Create fresh drivers every simulation
        drivers = [

            Driver(
                name="Verstappen",
                skill=1.0,
                tire=create_tire("Soft"),
                consistency=0.08
            ),

            Driver(
                name="Leclerc",
                skill=0.9,
                tire=create_tire("Medium"),
                consistency=0.15
            ),

            Driver(
                name="Norris",
                skill=0.85,
                tire=create_tire("Soft"),
                consistency=0.12
            )
        ]

        # Strategies
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

        # Create race
        race = Race(
            track=silverstone,
            drivers=drivers,
            strategies=strategies,
            total_laps=10,
            verbose=False
        )

        # Disable race printing
        run_silent_race(race)

        # Final standings
        drivers.sort(key=lambda d: d.total_time)

        # Record results
        for position, driver in enumerate(
            drivers,
            start=1
        ):

            results[driver.name][
                "total_position"
            ] += position

            if position == 1:
                results[driver.name]["wins"] += 1

    # Print statistics
    print("\n========== MONTE CARLO RESULTS ==========\n")

    for driver_name, stats in results.items():

        win_rate = (
            stats["wins"] / num_simulations
        ) * 100

        avg_finish = (
            stats["total_position"]
            / num_simulations
        )

        print(f"{driver_name}")
        print(f"Win Rate: {win_rate:.2f}%")
        print(f"Average Finish: {avg_finish:.2f}")
        print()


def run_silent_race(race):

    for lap in range(1, race.total_laps + 1):

        for driver in race.drivers:

            race.process_pit_stop(driver, lap)

            driver.drive_lap(
                race.track.base_lap_time
            )

        race.update_standings()

        race.process_overtakes()