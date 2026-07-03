import random
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from simulator.tire import create_tire
from simulator.driver import Driver
from simulator.track import Track
from simulator.strategy import Strategy
from simulator.race import Race

from optimizer.monte_carlo import run_monte_carlo
from optimizer.strategy_optimizer import StrategyOptimizer

from visualize import plot_lap_times, plot_positions, plot_tire_wear

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="F1 Strategy Simulator",
    layout="wide"
)

st.title("🏁 F1 Strategy Simulator")

# =====================================
# SIDEBAR
# =====================================

page = st.sidebar.radio(
    "Navigation",
    [
        "Race Simulator",
        "Monte Carlo",
        "Strategy Optimizer"
    ]
)

seed = st.sidebar.number_input("Random Seed", value=42)

random.seed(seed)

# =====================================
# SHARED OBJECTS
# =====================================

def build_track():
    return Track(
        name="Silverstone",
        base_lap_time=90.0,
        pit_stop_time=22,
        safety_car_probability=0.10
    )


def build_drivers():
    return [
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


# =====================================
# PAGE 1
# =====================================

if page == "Race Simulator":
    st.header("🏎️ Race Simulation")
    num_laps = st.slider("Total Laps", 5, 60, 20)
    run_race = st.button("▶ Run Race")

    if run_race:
        track = build_track()
        drivers = build_drivers()
        strategies = {

            "Verstappen":
                Strategy(
                    [10],
                    ["Soft", "Medium"]
                ),

            "Leclerc":
                Strategy(
                    [8],
                    ["Medium", "Hard"]
                ),

            "Norris":
                Strategy(
                    [12],
                    ["Soft", "Hard"]
                )
        }

        race = Race(
            track=track,
            drivers=drivers,
            strategies=strategies,
            total_laps=num_laps,
            verbose=False
        )

        progress = st.progress(0)
        status = st.empty()
        for lap in range(1, num_laps + 1):
            race.simulate_lap(lap)
            progress.progress(lap / num_laps)
            leader = race.drivers[0]
            status.write(f"Lap {lap}/{num_laps} | "f"Leader: {leader.name}")

        st.success("Race Finished")
        results = pd.DataFrame([
            {
                "Driver": d.name,
                "Total Time": round(d.total_time, 2)
            }
            for d in race.drivers
        ])

        st.subheader("🏆 Final Standings")
        st.dataframe(results, use_container_width=True)

        # -----------------
        # Charts
        # -----------------

        st.subheader("📊 Race Analysis")
        fig1 = plot_lap_times(drivers)
        st.pyplot(fig1)
        fig2 = plot_positions(drivers)

        st.pyplot(fig2)
        fig3 = plot_tire_wear(drivers)
        st.pyplot(fig3)


# =====================================
# PAGE 2
# =====================================

elif page == "Monte Carlo":
    st.header("📈 Monte Carlo Analysis")
    sims = st.slider("Simulations", 100, 5000, 1000, step=100)

    if st.button("Run Monte Carlo"):
        with st.spinner("Running simulations..."):
            results = run_monte_carlo(sims)
        df = pd.DataFrame(results)
        if df.empty:
            st.error("Monte Carlo returned no results. Check run_monte_carlo().")
            st.stop()

        # =========================
        # TABLE
        # =========================
        st.subheader("📋 Raw Results")
        st.dataframe(df, use_container_width=True)

        # =========================
        # SUMMARY METRICS
        # =========================
        st.subheader("📊 Summary")

        metric_col = "avg_time" if "avg_time" in df.columns else df.columns[1]
        best = df.loc[df[metric_col].idxmin()]
        col1, col2, col3 = st.columns(3)

        col1.metric("Best Strategy", best["strategy"])
        col2.metric("Best Avg Position", f"{best['avg_position']:.2f}")
        col3.metric("Win Rate", f"{best.get('win_rate', 0):.2%}")

        # =========================
        # BAR CHART: average time
        # =========================
        st.subheader("⏱️ Average Race Time by Strategy")

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(df["strategy"], df["avg_position"])
        ax.set_ylabel("Avg Position")
        ax.set_xlabel("Strategy")

        st.pyplot(fig)

        # =========================
        # OPTIONAL: win rate plot
        # =========================
        if "win_rate" in df.columns:

            st.subheader("🏆 Win Rate")

            fig2, ax2 = plt.subplots(figsize=(8, 4))
            ax2.bar(df["strategy"], df["win_rate"])
            ax2.set_ylabel("Win Probability")

            st.pyplot(fig2)


# =====================================
# PAGE 3
# =====================================

elif page == "Strategy Optimizer":

    st.header("🧠 Strategy Optimizer")

    pit_start = st.slider("Earliest Pit Lap", 2, 20, 5)

    pit_end = st.slider("Latest Pit Lap", 5, 40, 20)

    simulations = st.slider("MC Simulations", 50, 1000, 200)

    if st.button("Find Best Strategy"):

        track = build_track()
        opponents = build_drivers()[1:]
        optimizer = StrategyOptimizer(
            track=track,

            driver_template={
                "name": "Verstappen",
                "race_pace": 1.00,
                "consistency": 0.05,
                "tire_management": 0.98,
                "wet_skill": 1.08,
                "overtaking": 1.10,
                "defending": 1.10
            },

            opponents=opponents,
            total_laps=25,
            simulations=simulations
        )

        result = (
            optimizer.optimize_one_stop(
                first_compound="Soft",
                second_compound="Medium",
                start_lap=pit_start,
                end_lap=pit_end
            )
        )

        st.success(
            f"Best Pit Lap: "
            f"{result['best_pit_lap']}"
        )

        st.metric(
            "Expected Race Time",
            f"{result['best_time']:.2f}s"
        )

        history = pd.DataFrame(result["all_results"])
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(history["pit_lap"], history["expected_time"])

        ax.set_xlabel("Pit Lap")
        ax.set_ylabel("Expected Race Time")
        ax.set_title("Strategy Search")
        st.pyplot(fig)