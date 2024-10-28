
# Six Degrees of Separation in Non-Reciprocal Networks

This repository contains the code and instructions to replicate an experiment testing the "Six Degrees of Separation" theory in non-reciprocal networks, using Twitter data from the Stanford Large Network Dataset Collection (SNAP) and analytical tools such as Gephi and Python.

## Table of Contents

- [Six Degrees of Separation in Non-Reciprocal Networks](#six-degrees-of-separation-in-non-reciprocal-networks)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Requirements](#requirements)
  - [Dataset](#dataset)
  - [Setup](#setup)
  - [Data Preparation](#data-preparation)
  - [Analysis Steps](#analysis-steps)
  - [Results and Visualization](#results-and-visualization)
  - [References](#references)

---

## Overview

This project investigates the degrees of separation in a non-reciprocal social network (Twitter) to determine if the Six Degrees of Separation theory holds. The methodology involves:
- Data processing and preparation
- Network analysis to determine path lengths, clustering, and modularity
- Centrality analysis to identify influential nodes
- Visualization of community structures and network properties

## Requirements

To replicate this experiment, ensure you have the following installed:

- **Python 3.x**
- **Gephi** (for visualization and modularity analysis)
- Python Libraries:
  - `networkx`
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `tqdm`

## Dataset

The dataset used is the **Twitter Social Network** from the [SNAP dataset collection](https://snap.stanford.edu/data/ego-Twitter.html).

1. **Download the dataset**:
   - Go to the [SNAP ego-Twitter page](https://snap.stanford.edu/data/ego-Twitter.html).
   - Download the dataset files (`edges.csv` and `nodes.csv`) and save them to a local directory named `data/`.

2. **File Structure**:
   - Ensure the dataset files are in a directory called `data/` in the root of this repository for consistency with the analysis script.

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *(Ensure that `requirements.txt` includes the necessary Python libraries: `networkx`, `pandas`, `numpy`, `matplotlib`, `tqdm`.)*

3. **Install Gephi**:
   - Download Gephi from [https://gephi.org](https://gephi.org).
   - Follow the installation instructions for your operating system.

## Data Preparation

Since the SNAP dataset files are provided in a compatible CSV format, no additional data preparation script is necessary. Ensure the following structure:

- `data/edges.csv` – Contains edges representing connections between Twitter users.
- `data/nodes.csv` – Contains nodes representing Twitter users with attributes such as modularity class.

## Analysis Steps

1. **Run the Analysis Script**:
   - The main analysis script `network_analysis.py` performs all necessary computations, including:
     - Identifying within-cluster and cross-cluster edges
     - Calculating cluster density
     - Computing degree and eigenvector centrality for influential node identification
     - Estimating average path length and network diameter
   - Execute the script:
   ```bash
   python network_analysis.py
   ```

2. **Script Details**:
   - The script will:
     - Load and process the dataset to compute within-cluster and cross-cluster edges, displaying the cluster density.
     - Calculate degree and eigenvector centrality, ranking the top 10 nodes by degree with their centrality scores.
     - Use parallel processing to estimate the average path length.
     - Use a sample of nodes to approximate the network diameter through breadth-first search (BFS).

3. **Key Parameters**:
   - `SAMPLE_SIZE_AVG_PATH_LENGTH`: Defines the sample size for average path length calculations (default: 100,000).
   - `SAMPLE_SIZE_DIAMETER`: Defines the sample size for estimating the diameter through BFS (default: 10).

## Results and Visualization

1. **Interpret Results**:
   - The script outputs key metrics:
     - Total edges and breakdown of within-cluster and cross-cluster edges.
     - Top 10 connected users by degree with their eigenvector centrality scores.
     - Approximate average path length and network diameter.
   
2. **Visualization**:
   - Use Gephi to visualize community structures by modularity class and analyze clustering. Load the `nodes.csv` and `edges.csv` files in Gephi, apply the **ForceAtlas2** layout for initial visualization, and use the modularity feature to display clusters.

## References

- SNAP. (n.d.). *ego-Twitter Social Network.* Stanford Large Network Dataset Collection. Available at: https://snap.stanford.edu/data/ego-Twitter.html
- Bastian, M., Heymann, S., & Jacomy, M. (2009). Gephi: An Open Source Software for Exploring and Manipulating Networks. *International AAAI Conference on Weblogs and Social Media.*

---
