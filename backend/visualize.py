import matplotlib.pyplot as plt

def plot_lap_times(drivers):

    plt.figure(figsize=(10, 6))

    for driver in drivers:

        laps = range(1, len(driver.lap_times) + 1)

        plt.plot(
            laps,
            driver.lap_times,
            label=driver.name
        )

    plt.xlabel("Lap")
    plt.ylabel("Lap Time (s)")
    plt.title("Lap Times by Driver")

    plt.legend()

    plt.grid(True)

    plt.show()

def plot_positions(drivers):

    plt.figure(figsize=(10, 6))

    for driver in drivers:

        laps = range(
            1,
            len(driver.position_history) + 1
        )

        plt.plot(
            laps,
            driver.position_history,
            marker='o',
            label=driver.name
        )

    plt.xlabel("Lap")
    plt.ylabel("Race Position")

    plt.title("Position Changes During Race")

    # Reverse Y-axis because P1 should be at top
    plt.gca().invert_yaxis()

    plt.legend()

    plt.grid(True)

    plt.show()


def plot_tire_wear(drivers):

    plt.figure(figsize=(10, 6))

    for driver in drivers:

        laps = range(
            1,
            len(driver.wear_history) + 1
        )

        plt.plot(
            laps,
            driver.wear_history,
            label=driver.name
        )

    plt.xlabel("Lap")
    plt.ylabel("Tire Wear")

    plt.title("Tire Wear Over Race")

    plt.legend()

    plt.grid(True)

    plt.show()