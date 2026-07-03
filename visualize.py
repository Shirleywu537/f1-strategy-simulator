import matplotlib.pyplot as plt


def plot_lap_times(drivers):
    fig, ax = plt.subplots(figsize=(10, 6))

    for driver in drivers:
        laps = range(1, len(driver.lap_times) + 1)
        ax.plot(laps, driver.lap_times, linewidth=2, label=driver.name)

    ax.set_title("Lap Time Evolution")
    ax.set_xlabel("Lap")
    ax.set_ylabel("Lap Time (s)")
    ax.grid(True)
    ax.legend()
    return fig


def plot_positions(drivers):
    fig, ax = plt.subplots(figsize=(10, 6))

    for driver in drivers:
        laps = range(1, len(driver.position_history) + 1)

        ax.plot(laps, driver.position_history, marker="o", label=driver.name)

    ax.set_title("Race Positions")
    ax.set_xlabel("Lap")
    ax.set_ylabel("Position")
    ax.invert_yaxis()
    ax.grid(True)
    ax.legend()

    return fig


def plot_tire_wear(drivers):

    fig, ax = plt.subplots(figsize=(10, 6))
    for driver in drivers:
        laps = range(1, len(driver.wear_history) + 1)
        ax.plot(laps, driver.wear_history, linewidth=2, label=driver.name)

    ax.set_title("Tire Wear Progression")
    ax.set_xlabel("Lap")
    ax.set_ylabel("Wear")
    ax.grid(True)
    ax.legend()

    return fig


def plot_gap_to_leader(drivers):

    fig, ax = plt.subplots(figsize=(10, 6))

    leader = min(drivers, key=lambda d: d.total_time)

    for driver in drivers:
        gap = driver.total_time - leader.total_time

        ax.bar(driver.name, gap)

    ax.set_title("Gap To Race Winner")
    ax.set_ylabel("Seconds Behind")
    return fig


def plot_average_lap_times(drivers):
    fig, ax = plt.subplots(figsize=(10, 6))
    names = []
    averages = []
    for driver in drivers:
        names.append(driver.name)
        averages.append(sum(driver.lap_times) / len(driver.lap_times))

    ax.bar(names, averages)
    ax.set_title("Average Lap Time")
    ax.set_ylabel("Seconds")

    return fig


def plot_tire_stints(drivers):

    fig, ax = plt.subplots(figsize=(12, 4))
    for idx, driver in enumerate(drivers):
        if not hasattr(driver, "tire_history"):
            continue

        start_lap = 1
        for compound, end_lap in (driver.tire_history):

            ax.barh(driver.name, end_lap - start_lap + 1, left=start_lap, alpha=0.8)
            ax.text(start_lap, idx, compound, fontsize=8)
            start_lap = end_lap + 1

    ax.set_title("Tire Strategy Timeline")
    ax.set_xlabel("Lap")

    return fig