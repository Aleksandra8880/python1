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
- **Data Rows:** Each record contains:
  - 3D momentum vectors (`px`, `py`, `pz` in $10^{-20}\ \text{kg}\cdot\text{m}/\text{s}$)
  - Integer ID representing the bacterial strain or genetic variant

---

## Main Results

This analysis evaluates the full dataset across subsamples (`output-Set1.txt` to `output-Set10.txt`) using the subsampling technique to determine the mean number of bacteria per event along with their statistical uncertainties.

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

To assess asymmetry without assuming independence between strains, the difference ($\Delta = \langle\text{WT}\rangle - \langle\text{Mutant}\rangle$) was computed within each subsample batch, and the statistical uncertainty was determined from the spread across all subsamples.

| Bacterial Species | Mean Asymmetry ($\langle\text{WT}\rangle - \langle\text{Mutant}\rangle$) | Uncertainty | Statistical Significance |
| :--- | :---: | :---: | :---: |
| ***E. coli*** | 0.032320 | ± 0.004210 | Significant ($> 7\sigma$) |
| ***B. subtilis*** | 0.005695 | ± 0.001150 | Significant ($> 4\sigma$) |
| ***P. aeruginosa*** | 0.023890 | ± 0.001920 | Significant ($> 12\sigma$) |
| ***S. pneumoniae*** | 0.004907 | ± 0.000850 | Significant ($> 5\sigma$) |
| ***M. tuberculosis*** | 0.000440 | ± 0.000490 | Not Significant ($< 1\sigma$) |
| ***S. enterica*** | 0.000035 | ± 0.000062 | Not Significant ($< 1\sigma$) |

#### Overall Abundance Asymmetry Plot
![Abundance Asymmetry](wt_mutant_differences.png)

---

### Momentum-Dependent Asymmetry

The differential asymmetry as a function of momentum magnitude ($p = \sqrt{p_x^2 + p_y^2 + p_z^2}$) was evaluated in uniform bins between $0$ and $60 \times 10^{-20}\ \text{kg}\cdot\text{m}/\text{s}$.

#### *E. coli* Momentum Distribution
![E. coli Momentum Asymmetry](E_coli_momentum_asymmetry.png)

#### *B. subtilis* Momentum Distribution
![B. subtilis Momentum Asymmetry](B_subtilis_momentum_asymmetry.png)

#### *P. aeruginosa* Momentum Distribution
![P. aeruginosa Momentum Asymmetry](P_aeruginosa_momentum_asymmetry.png)

#### *S. pneumoniae* Momentum Distribution
![S. pneumoniae Momentum Asymmetry](S_pneumoniae_momentum_asymmetry.png)

#### *M. tuberculosis* Momentum Distribution
![M. tuberculosis Momentum Asymmetry](M_tuberculosis_momentum_asymmetry.png)

#### *S. enterica* Momentum Distribution
![S. enterica Momentum Asymmetry](S_enterica_momentum_asymmetry.png)

---

## Conclusions & Answers to Research Questions

1. **What are the average counts and uncertainties?**  
   - The average counts per event vary across strains, ranging from $\sim 20$ counts/event for *E. coli* down to $\sim 0.001$ counts/event for *S. enterica*, with statistical uncertainties calculated from the subsample spread.

2. **Is there any asymmetry between normal and mutant strains?**  
   - **Yes.** A distinct, statistically significant positive asymmetry is observed in *E. coli*, *B. subtilis*, *P. aeruginosa*, and *S. pneumoniae*, where the wild type significantly outnumbers the mutant strain.  
   - Conversely, *M. tuberculosis* and *S. enterica* are compatible with zero asymmetry within their statistical uncertainty.

3. **Is there any asymmetry as a function of momentum?**  
   - **Yes.** The observed abundance asymmetry is strongly concentrated in the low-momentum region ($p \lesssim 15 \times 10^{-20}\ \text{kg}\cdot\text{m}/\text{s}$). As momentum increases, the counts decrease and the absolute difference approaches zero.
