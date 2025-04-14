# Benchmarking Dispatching Algorithms Using Real Scenarios in Elevator Monte Carlo Simulation

This project was developed by Gastón Amengual and Ezequiel L. Castaño in college in 2021 as part of our academic work. It benchmarks the performance of different elevator dispatching algorithms under realistic building scenarios using a discrete-event Monte Carlo simulation. The simulation focuses on time-based performance metrics that impact user satisfaction, such as wait time and system time.

## 🧠 Core Concepts
* Dispatching Algorithms: Logic used by elevators to decide which floor to go to next. Four strategies were tested:
	* FIFO – First-In, First-Out
	* IFOF – Inside-First, Outside-Following
	* LOOK – Directional sweep without preference
	* LOOK-M – Modified LOOK, prioritizes inside calls first

* Scenarios: Realistic high- and low-demand settings:
	* Morning Rush
	* Lunchtime
	* Evening Rush
	* Residential Building
	* Full Business Day (composed scenario)

* Metrics:
	* Queue Time – Time waiting on a floor
	* Elevator Time – Time spent riding the elevator
	* System Time – Total time from arrival to destination

## ⚙️ Methodology

* Single elevator in a 6-floor building

* Gamma-distributed arrival times

* Fixed elevator speed and door times

* Capacity limit enforced

* Users may abandon the queue after a threshold

Each algorithm was tested across all scenarios, with 200 simulation runs per combination. Results were recorded and compared to assess overall performance.

## 📈 Results

* LOOK and LOOK-M consistently outperformed FIFO and IFOF in system time.

* LOOK-M performed better in low-demand settings (like Residential).

* IFOF had the best elevator time in high-demand Evening Rush but came at the cost of higher queue times.

* FIFO was the worst performer overall, especially in high-demand scenarios.

* Demand level critically influenced the optimal algorithm choice.

## 🔧 Tech Stack

* Python (Numpy, Pandas)

* Matplotlib for data visualization
