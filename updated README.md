# Monitoring Bacterial Movement and Populations

> Analysis of simulated bacterial tracking data to investigate bacterial abundance and differences between normal and mutant strains.

---

## Contents

- [Introduction](#introduction)
- [Data](#data)
- [Research Questions](#research-questions)
- [Analysis Method](#analysis-method)
- [Results](#results)
- [Normal vs Mutant Comparison](#normal-vs-mutant-comparison)
- [Conclusion](#conclusion)
- [Next Steps](#next-steps)

---

## Introduction

This project focuses on monitoring bacterial movement and populations using simulated data from bacterial tracking experiments, where bacterial movement and proliferation under specific nutrient or stress conditions are modelled by the simulation.

The analysis compares different bacterial strains and genetic variants to investigate their abundance and determine whether there are differences between normal and mutant strains.

---

## Data

Each input file represents simulated output from bacterial tracking experiments. The header of each event contains an event ID and the number of bacterial cells in that event, while the following rows contain the three-dimensional momentum components `px`, `py` and `pz`, together with an integer ID identifying the bacterial strain or genetic variant.

For this analysis, a total of **5,000,000 events** were used, divided into **10 sub-samples of 500,000 events each**. Although `output-Set0.txt` was also present in the dataset folder, it contains only one event and therefore does not match the size of the other sub-samples, so it was not included in the final analysis or uncertainty calculation.

---

## Research Questions

The analysis aims to answer the following questions:

1. What are the average counts of each bacterial strain and their statistical uncertainties?
2. Is there an asymmetry between the normal and mutant bacterial strains? If so, how large is this asymmetry?
3. Is there an asymmetry between the normal and mutant bacterial strains as a function of their momentum?

---

## Analysis Method

### Average per event

The program analyses each dataset separately and counts the bacterial IDs included in the analysis. The average number of bacteria per event is then calculated by dividing the total count of each bacterial strain by the total number of events:

$$
\text{Average per event} =
\frac{\text{Total bacterial count}}{\text{Total number of events}}
$$

### Statistical uncertainty

To calculate the statistical uncertainty, the 5,000,000 events are split into 10 sub-samples of 500,000 events and the average number of bacteria per event is calculated separately for each one. The standard deviation of these 10 results is then used as the statistical uncertainty on the final average.

### Normal vs mutant comparison

To investigate whether there is an asymmetry between the normal and mutant strains, the difference between their average counts is calculated for each pair:

$$
\Delta = \text{Average}_{normal} - \text{Average}_{mutant}
$$

Rather than only comparing the two final averages, this difference is also calculated separately within each of the 10 sub-samples, allowing the standard deviation of these differences to be used as the statistical uncertainty on $\Delta$.

The size of each difference can then be compared with its statistical uncertainty using:

$$
\frac{|\Delta|}{\sigma_{\Delta}}
$$

This gives the number of statistical uncertainties by which the measured difference differs from zero and can therefore be used to judge whether the observed difference is likely to represent an asymmetry rather than a statistical fluctuation.

---

## Results

Across the **5,000,000 events**, a total of **221,204,606 selected bacteria** were identified and no invalid lines were found in the included sub-samples.

| Bacterial strain | ID | Average per event | Statistical uncertainty |
|---|---:|---:|---:|
| *E. coli* WT | `211` | 18.42534 | ± 0.02778 |
| *E. coli* mutant | `-211` | 18.39551 | ± 0.02693 |
| *B. subtilis* WT | `321` | 2.31745 | ± 0.00401 |
| *B. subtilis* mutant | `-321` | 2.31219 | ± 0.00478 |
| *P. aeruginosa* WT | `2212` | 1.11574 | ± 0.00165 |
| *P. aeruginosa* antibiotic-resistant | `-2212` | 1.09369 | ± 0.00209 |
| *S. pneumoniae* | `3122` | 0.255466 | ± 0.000963 |
| Capsule-deficient *S. pneumoniae* | `-3122` | 0.250938 | ± 0.000891 |
| *M. tuberculosis* | `3312` | 0.0364278 | ± 0.000254 |
| Drug-resistant *M. tuberculosis* | `-3312` | 0.0360208 | ± 0.000367 |
| *S. enterica* | `3334` | 0.0010964 | ± 0.0000384 |
| *Salmonella* mutant | `-3334` | 0.0010636 | ± 0.0000469 |

---

## Normal vs Mutant Comparison

Although the normal strain has a slightly higher average abundance than its corresponding mutant or resistant strain for all six pairs, the size of this difference needs to be considered relative to its statistical uncertainty before deciding whether it provides evidence for an asymmetry.

| Comparison | Difference per event (Δ) | Uncertainty (σ) | Δ / σ |
|---|---:|---:|---:|
| *E. coli* | 0.0298292 | ± 0.0041732 | **7.15** |
| *B. subtilis* | 0.0052562 | ± 0.0030416 | **1.73** |
| *P. aeruginosa* | 0.0220492 | ± 0.0021929 | **10.05** |
| *S. pneumoniae* | 0.0045280 | ± 0.0005383 | **8.41** |
| *M. tuberculosis* | 0.0004070 | ± 0.0004506 | **0.90** |
| *S. enterica* | 0.0000328 | ± 0.0000633 | **0.52** |

The largest differences relative to their uncertainties are found for ***P. aeruginosa***, ***S. pneumoniae*** and ***E. coli***, at approximately 10.05σ, 8.41σ and 7.15σ respectively. Since these differences are several times larger than their statistical uncertainties, they provide much stronger evidence for an asymmetry between the normal and mutant populations.

For ***B. subtilis***, the difference is only 1.73σ, while ***M. tuberculosis*** and ***S. enterica*** have differences of 0.90σ and 0.52σ respectively. In these cases, the measured differences are much smaller relative to their statistical uncertainties, so the results do not provide the same evidence for an asymmetry.

---

## Conclusion

The analysis shows that the normal bacterial strain has a higher average abundance than the corresponding mutant or resistant strain for all six pairs, although the size and statistical relevance of these differences vary between the different bacteria.

The clearest differences are found for ***E. coli***, ***P. aeruginosa*** and ***S. pneumoniae***, where the difference between the normal and mutant populations is several times larger than its statistical uncertainty. Comparitavely, the differences observed for ***B. subtilis***, ***M. tuberculosis*** and ***S. enterica*** are much closer to their uncertainties, meaning that these results do not provide equally strong evidence for an asymmetry.

---

## Next Steps

The movement of each bacterium is described by the three momentum components `px`, `py` and `pz`, from which the total momentum can be calculated as:

$$
p = \sqrt{p_x^2 + p_y^2 + p_z^2}
$$

The next stage of the project will check whether the differences between normal and mutant bacterial strains change as a function of momentum.