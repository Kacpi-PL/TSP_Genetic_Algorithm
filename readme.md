# Traveling Salesman Problem Solver: Genetic Algorithm

An interactive web application built with Python and Streamlit that solves the Traveling Salesman Problem (TSP) using an evolutionary approach. The project visualizes the optimization process in real-time and allows for dynamic adjustment of genetic algorithm parameters.

![TSP Solver Showcase](assets/showcase.gif) 


## Overview

This project implements a Genetic Algorithm from scratch to find near-optimal solutions for NP-hard routing problems. It features a fully interactive Streamlit dashboard that tracks the distance convergence and plots the best route on a 2D coordinate plane generation by generation. 

The application is configured to parse and solve standard TSPLIB datasets, with built-in support for **Berlin52** and **ATT48**.

## Features

* **Real-time Visualization:** Dynamic Matplotlib charts displaying the route evolution and distance convergence against the known global optimum.
* **Parameter Tuning:** Instant adjustment of Population Size, Generations, Elite Size, and Mutation/Crossover Probabilities via the UI.
* **Data Export:** Download detailed run metrics, execution time, and the final route configuration as a JSON report for further analysis.

## Implemented Operators

* **Selection:** Tournament Selection, Roulette Wheel Selection, Rank Selection
* **Crossover:** Ordered Crossover (OX), Partially Mapped Crossover (PMX), Edge Recombination Crossover (ERX)
* **Mutation:** Swap Mutation, Inverse Mutation, Scramble Mutation

## Experimental Insights

During the development and testing of this algorithm, several performance benchmarks were observed:
* **Crossover Efficiency:** While Edge Recombination Crossover (ERX) is theoretically superior at preserving edge adjacency, Ordered Crossover (OX) consistently yielded faster execution times and competitive convergence rates due to lower computational overhead.
* **Selection Pressure:** Roulette Wheel selection frequently led to premature convergence (getting stuck in local optima) and performed poorly compared to Tournament Selection, which maintained a much healthier genetic diversity across generations.
* **Mutation Impact:** Inverse mutation proved to be highly effective for the TSP compared to standard point-swapping, significantly improving the algorithm's ability to escape local minima.

## Project Structure
```text
├── data/
│   ├── att48.tsp
│   ├── berlin52.tsp
├── assets/
│   ├──showcase.gif
├── app.py                 # Streamlit UI and main entry point
├── genetic_algorithm.py   # Core GA logic and evolutionary loop
├── operators.py           # Selection, crossover, and mutation functions
├── tsp_problem.py         # TSPLIB95 data parser and distance matrix calculator
├── utils.py               # Helper functions (population initialization, fitness)
├── visualization.py       # Matplotlib drawing and plotting functions
├── requirements.txt
└── README.md
```

## Installation & Usage

1. Clone the repository:
```bash
   git clone https://github.com/kacpipl2006/TSP_With_Genetic_Algorithm.git
   cd TSP_With_Genetic_Algorithm
```

2. Install the required dependencies:
   
```bash
   pip install -r requirements.txt
```

3. Run the Streamlit application:
```bash
   streamlit run app.py
   
```