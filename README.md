# Monitoring Bacterial Movement and Populations

## Description
This project uses simulated outputs from a bacterial tracking experiment. It monitors how different bacterial species move (motility) and reproduce (proliferation) under diverse conditions, such as nutrient availability or stress factors.


## Research Questions
- What are the average counts of each bacterial strain and their statistical uncertainties?
- Is there any asymmetry between the normal and the mutant strain?
- Is there any asymmetry as a function of their momentum?

---

## Input Data Format
Each experiment file consists of:
- **Header:** Contains the `event ID` and total `number of bacteria tracked`
- **Data Rows:** Each record contains
    - 3D momentum vectors (`px`, `py`, `pz` in 10⁻²⁰ kg·m/s)
    - Integer ID representing the bacterial strain or genetic variant

---

## Installation & Environment Setup

### Prerequisites
- Python 3.9+
- Git

### Setup Instructions
1. Clone the repository and navigate to the project root:
```bash
git clone https://github.com/Aleksandra8880/python1.git
cd python1
```

## Usage
To run the analysis script:
```bash
python main.py
```

---

## Main Results

This analysis evaluates the full dataset across subsamples using the subsampling technique to determine the mean number of bacteria per event along with their statistical uncertainties.

### Bacterial Counts per Event

| Bacterial ID | Bacterial Strain | Average Count per Event | Statistical Uncertainty ($\pm$) |
| :---: | :--- | :---: | :---: |
| `211` | *E. coli* (wild type) | 19.964042 | 0.031091 |
| `-211` | *E. coli* (mutant) | 19.931722 | 0.030228 |
| `321` | *B. subtilis* (wild type) | 2.510976 | 0.004516 |
| `-321` | *B. subtilis* (mutant) | 2.505281 | 0.005228 |
| `2212` | *P. aeruginosa* (wild type) | 1.208914 | 0.001818 |
| `-2212` | *P. aeruginosa* (antibiotic-resistant mutant) | 1.185024 | 0.002295 |
| `3122` | *S. pneumoniae* (wild type) | 0.276800 | 0.001021 |
| `-3122` | *S. pneumoniae* (capsule-deficient mutant) | 0.271894 | 0.000935 |
| `3312` | *M. tuberculosis* (wild type) | 0.039470 | 0.000269 |
| `-3312` | *M. tuberculosis* (drug-resistant mutant) | 0.039029 | 0.000381 |
| `3334` | *S. enterica* (wild type) | 0.001188 | 0.000040 |
| `-3334` | *S. enterica* (mutant) | 0.001152 | 0.000048 |

---

### Wild Type vs. Mutant Comparison & Asymmetry

To assess asymmetry without assuming independence between strains, the difference ($\Delta = \langle\text{WT}\rangle - \langle\text{Mutant}\rangle$) was computed within each subsample batch, and the statistical uncertainty was determined from the spread (sample standard deviation) of these differences across all subsamples.

* **Statistically Significant Difference (Asymmetry detected):**
  * *E. coli*
  * *B. subtilis*
  * *P. aeruginosa*
  * *S. pneumoniae*

* **No Significant Difference (Compatible with zero):**
  * *M. tuberculosis*
  * *S. enterica*

