import random

from simulator.tire import create_tire
from simulator.driver import Driver
from simulator.track import Track
from simulator.strategy import Strategy
from simulator.race import Race
from monte_carlo import run_monte_carlo

from visualize import (
    plot_lap_times,
    plot_positions,
    plot_tire_wear
)


def main():

    # Create track
    silverstone = Track(
        name="Silverstone",
        base_lap_time=90.0,
        pit_stop_time=22
    )

    # Create drivers
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

    # Create strategies
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
        total_laps=10
    )

    # Run race simulation
    race.run()

    # Visualization
    plot_lap_times(drivers)

    plot_positions(drivers)

    plot_tire_wear(drivers)

    run_monte_carlo(num_simulations=1000)


if __name__ == "__main__":

    random.seed(42)

    main()