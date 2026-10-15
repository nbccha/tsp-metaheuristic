# TSP Metaheuristic: SA, Tabu Search, and VNS

Aplikasi optimasi **Traveling Salesman Problem (TSP)** berbasis Streamlit untuk membangun, mengoptimalkan, dan membandingkan rute menggunakan tiga algoritma metaheuristik: **Simulated Annealing (SA), Tabu Search (TS), dan Variable Neighborhood Search (VNS)**.

Project ini mendukung input data fleksibel, visualisasi rute, analisis konvergensi, perbandingan kualitas solusi, serta eksperimen multi-run untuk mengevaluasi performa algoritma berdasarkan data aktual.

## Key Features

- **Flexible Input:** input manual, klik kanvas X–Y, generate koordinat acak, upload Excel/CSV, dan dataset contoh.
- **Distance Metrics:** Euclidean dan Manhattan.
- **Initial Solution:** Nearest Neighbor (NN), Nearest Insertion (NI), Cheapest Insertion (CI), Farthest Insertion (FI), Arbitrary Insertion (AI), dan rute manual.
- **Local Search:** 2-opt dengan strategi First Improvement atau Best Improvement.
- **Simulated Annealing:** optimasi berbasis probabilitas penerimaan Metropolis dan penurunan suhu.
- **Tabu Search:** pencarian neighborhood dengan tabu list FIFO dan aspiration criterion.
- **Variable Neighborhood Search:** eksplorasi bergantian menggunakan Swap, Insertion, dan 2-opt, dilengkapi shaking serta opsi local search.
- **Performance Comparison:** perbandingan best distance, runtime, jumlah iterasi, dan struktur rute SA, TS, serta VNS.
- **Convergence & Analysis:** grafik konvergensi, iteration log, analisis improvement, pembaruan solusi terbaik, dan kesamaan edge.
- **Multi-run & Export:** statistik eksperimen berulang serta ekspor rute, log, distance matrix, dan grafik ke CSV/PNG.

## Project Structure

```text
TSP-Metaheuristic/
├── app/
│   └── app.py              # Streamlit interface and workflow
├── src/
│   └── tsp_core.py         # Distance functions and algorithms
├── data/
│   └── data1.xlsx          # Example dataset
├── docs/                   # Project documentation
├── .streamlit/
│   └── config.toml         # Application theme
├── requirements.txt
└── README.md
```

**Core implementation**

- `app/app.py`: input management, algorithm configuration, execution, visualization, comparison, and analysis.
- `src/tsp_core.py`: distance calculation, construction heuristics, local search, SA, TS, ILS, and VNS.
- `data/data1.xlsx`: example dataset using sheet `Sheet7`, containing Case I (25 cities), Case II (40 cities), and Case III (68 cities).

## Tech Stack

Python · Streamlit · NumPy · Pandas · Matplotlib · Plotly · openpyxl

## Installation

Python must be installed before running the application.

**1. Open a terminal in the project directory**

```powershell
cd "path\to\TSP-Metaheuristic"
```

**2. Create and activate a virtual environment**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Skip the first command if the virtual environment already exists.

**3. Install dependencies**

```powershell
python -m pip install -r requirements.txt
```

**4. Run the application**

```powershell
python -m streamlit run app/app.py
```

Open the local URL displayed in the terminal, usually `http://localhost:8501`.

## Optimization Methods

### 1. Simulated Annealing (SA)

SA explores the solution space by accepting improving solutions and occasionally accepting worse solutions to reduce the risk of becoming trapped in a local optimum.

Acceptance probability:

```text
P(accept) = 1, if ΔE ≤ 0
P(accept) = exp(-ΔE / T), if ΔE > 0
```

Temperature cooling:

```text
T_next = α × T
```

Main parameters: initial temperature, cooling rate (alpha), minimum temperature, iterations per temperature, maximum iterations, and neighborhood operator.

### 2. Tabu Search (TS)

TS explores neighboring routes while using a bounded FIFO tabu list to discourage cycling between previously visited moves. The aspiration criterion allows a tabu move when it improves the best solution found so far.

Main parameters: maximum iterations, tabu size, neighborhood size, neighborhood operator, and aspiration criterion.

### 3. Variable Neighborhood Search (VNS)

VNS systematically changes neighborhood structures to explore different regions of the solution space.

Supported neighborhoods:

- **Swap:** exchange the positions of two cities.
- **Insertion:** move a city to another position in the route.
- **2-opt:** reverse a segment of the route.

The search applies shaking, optionally performs 2-opt local search, evaluates the candidate, and returns to the first neighborhood when an improvement is found. Otherwise, it advances to the next neighborhood.

Main parameters: maximum iterations, `k_max`, selected neighborhoods, shaking method, local search option, and random seed.

### Additional Methods

- **Construction heuristics:** generate an initial feasible route.
- **2-opt Local Search:** improve the initial route and optionally polish an optimized route.
- **Iterated Local Search (ILS):** optional optimization using 2-opt and double-bridge perturbation.
- **Multi-run:** repeat SA, TS, and VNS with controlled seeds to assess solution quality and consistency.

## Workflow

1. **Input Data:** select a data source and prepare city coordinates.
2. **Configure Optimization:** choose the distance metric, initial solution, local search, algorithm parameters, random seed, and optional multi-run.
3. **Review Optimization Summary:** verify the configuration before execution.
4. **Run Optimization:** execute SA, TS, and VNS, with optional ILS.
5. **Evaluate Results:** inspect the summary, routes, algorithm comparison, convergence, iteration logs, and analysis.
6. **Export Results:** save supported route visualizations and experiment data.

## Results & Evaluation

The application provides the following result views:

| View | Purpose |
|---|---|
| Summary | Initial distance, best distance, improvement, runtime, and iterations |
| Routes | Visualization of initial and optimized routes |
| Comparison | Pairwise route-edge overlap and distance differences |
| Convergence | Best-distance history from actual algorithm execution |
| Detail & Log | Route details, iteration logs, and distance matrix |
| Analysis | Six information cards covering solution quality, runtime, convergence, and route structure |
| Competition | Compare a user-created route with algorithm results |
| Tabu Explorer | Inspect Tabu Search history for datasets of up to 12 cities |
| Multi-run | Evaluate repeated-run statistics when enabled |

Supported exports include route images, comparison images, convergence plots (PNG), route details (CSV), iteration logs (CSV), and distance matrices (CSV).

## Implementation Notes

- A route is a **closed tour**: the return to the starting city is included in the total distance.
- Each city must be visited exactly once.
- The application supports up to 200 cities.
- Euclidean distance uses straight-line coordinate distance; Manhattan distance uses the sum of absolute coordinate differences.
- SA, TS, and VNS use the same input data, distance metric, and starting solution within a comparison run.
- Random seeds support reproducible algorithmic experiments when data and parameters are unchanged. Runtime may vary between executions.
- Best distance, improvement, iteration history, convergence, runtime, and edge overlap are derived from the executed algorithms, not hardcoded results.
- No algorithm is guaranteed to outperform the others for every dataset or configuration.

## Troubleshooting

**Streamlit command not found**

```powershell
python -m streamlit run app/app.py
```

**Missing dependencies**

```powershell
python -m pip install -r requirements.txt
```

**Example dataset not found**

Verify that `data/data1.xlsx` exists and contains the expected `Sheet7` worksheet.

**Configuration changed after optimization**

Run **RUN OPTIMIZATION** again to refresh results for the current data and parameters.

---

This project is intended for learning and experimentation in combinatorial optimization, with an emphasis on solution quality, convergence behavior, runtime, and reproducibility across SA, TS, and VNS.