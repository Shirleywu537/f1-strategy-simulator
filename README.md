# F1 Strategy Simulator

A Python-based Formula 1 race strategy simulator that models realistic race dynamics using probabilistic simulation and Monte Carlo methods. The simulator evaluates pit stop strategies under varying weather conditions, tire degradation, overtaking opportunities, and safety car deployments to estimate race outcomes.

---

# Motivation

Formula 1 races are often won or lost through strategy rather than outright pace. Teams must constantly balance tire degradation, pit stop timing, weather conditions, safety cars, and overtaking opportunities under uncertainty.

I built this project to explore how probabilistic simulation and optimization techniques can be used to model these strategic decisions. Rather than replaying historical races, the simulator provides a flexible framework for experimenting with different race strategies and understanding the trade-offs behind them.

The project also served as an opportunity to practice object-oriented software design, Monte Carlo simulation, data visualization, and interactive application development in Python.

---

# Tech Stack

| Category | Technologies |

|----------|--------------|

| Language | Python 3.11+ |

| Numerical Computing | NumPy |

| Data Processing | Pandas |

| Visualization | Matplotlib |

| Web Interface | Streamlit |

| Development | Git, GitHub |

| Programming Paradigm | Object-Oriented Programming (OOP) |

---

## Features

- Full race simulation
- Tire degradation model
- Pit stop strategy optimization
- Dynamic weather simulation
- Safety Car probability model
- Overtaking simulation
- Monte Carlo race analysis
- Interactive Streamlit dashboard
- Strategy comparison and visualization

---

## Simulation Components

### Tire Model

Each tire compound has unique characteristics including:

- Initial grip
- Performance degradation
- Wear rate
- Recommended stint length

Supported compounds:

- Soft
- Medium
- Hard

Tire performance decreases over each lap, affecting lap time and strategy decisions.

---

### Driver Model

Each driver maintains:

- Current tire
- Tire age
- Lap times
- Position
- Pit stop history
- Retirement status

Drivers can:

- Complete laps
- Pit for new tires
- Retire from the race
- Overtake competitors

---

### Track Model

Tracks define race-specific parameters such as:

- Number of laps
- Pit lane time loss
- Overtaking difficulty
- Safety Car probability
- Base lap time

Different tracks naturally produce different strategic outcomes.

---

### Weather System

Weather evolves throughout the race and influences:

- Tire performance
- Grip levels
- Pit strategy
- Lap times

Possible conditions include:

- Sunny
- Cloudy
- Light Rain
- Heavy Rain

---

### Race Engine

The race simulator performs a lap-by-lap simulation that models:

- Tire degradation
- Driver pace
- Pit stop execution
- Safety Car deployment
- Overtaking attempts
- Position updates
- Race retirement events

The engine keeps track of the full race state until the checkered flag.

---

## Monte Carlo Simulation

To account for randomness in racing, the simulator performs hundreds or thousands of independent race simulations.

Random variables include:

- Weather evolution
- Safety Cars
- Driver performance variation
- Overtake success
- Pit timing interactions

This produces probability distributions instead of a single deterministic outcome.

Example outputs include:

- Average finishing position
- Win probability
- Podium probability
- Expected race time
- Strategy success rate

---

## Project Structure

```
f1-strategy-simulator/
│
├── models/
│   ├── driver.py
│   ├── tire.py
│   ├── track.py
│   └── weather.py
│
├── simulator/
│   ├── race.py
│   └── strategy.py
│
├── optimizer/
│   ├── monte_carlo.py
│   └── strategy_optimizer.py
│
├── visualization/
│   └── plots.py
│
├── app.py
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Shirleywu537/f1-strategy-simulator.git

cd f1-strategy-simulator
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Simulator

Run the Streamlit application:

```bash
streamlit run app.py
```

The dashboard allows users to:

- Select tire strategies
- Configure race parameters
- Adjust weather conditions
- Run Monte Carlo simulations
- Compare strategy outcomes
- Visualize race statistics

---

## Example Strategy Comparison

| Strategy | Avg Finish | Avg Race Time | Pit Stops |
|-----------|-----------:|--------------:|----------:|
| Medium → Hard | 3.8 | 1:31:42 | 1 |
| Soft → Medium → Hard | 2.9 | 1:31:18 | 2 |
| Hard → Medium | 5.1 | 1:32:10 | 1 |

*(Example results for illustration.)*

---

## Technologies

- Python
- NumPy
- Pandas
- Matplotlib
- Streamlit

---

## Future Improvements

- FIA regulation constraints
- DRS modeling
- Fuel load simulation
- Driver skill ratings
- Track-specific degradation models
- Historical race calibration
- Bayesian parameter estimation
- Reinforcement learning strategy optimization
- Live telemetry integration
- Multi-driver/team simulation

---

## Learning Objectives

This project demonstrates:

- Object-oriented software design
- Simulation modeling
- Probabilistic programming
- Monte Carlo methods
- Data visualization
- Interactive dashboard development
- Strategy optimization under uncertainty

---

## License

This project is intended for educational and portfolio purposes.