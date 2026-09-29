# Biology-Themed Project: Bacterial Movement and Populations
## Topic

This project models how different bacterial species move and proliferate under specific nutrient or stress conditions

The data come from simulated bacterial tracking experiments. Each simulation contains information about the number of bacteria observed, their 3D momentum  (`px`, `py`, and `pz`), and an ID corresponding to a specific bacterial strain or genetic variant.

The bacterial strains included in the dataset are:

- E. coli WT and E. coli mutant
- Bacillus subtilis WT and Bacillus subtilis mutant
- Pseudomonas aeruginosa WT and antibiotic-resistant Pseudomonas aeruginosa
- Streptococcus pneumoniae and capsule-deficient Streptococcus pneumoniae
- Mycobacterium tuberculosis and drug-resistant Mycobacterium tuberculosis
- Salmonella enterica and Salmonella mutant

## Research Questions

The project will aim to answer the following questions:

1. What are the average counts of each bacterial strain and their statistical uncertainties?

2. Is there an asymmetry between the normal and mutant bacterial strains? If so, how large?

3. Is there an asymmetry between the normal and mutant bacterial strains as a function of their momentum? ## Week 4 - Statistical Analysis

# Week 4 - Bacteria Analysis

## Analysis


The sample was divided into 10 sub-samples of 500,000 events, each one was analysed separately. In total, 4,614,632 valid events were used in the analysis.

For each bacterial strain, I calculated the average number per valid event using the full sample.

The statistical uncertainty was calculated using the sub-sampling method. I calculated the average for each of the 10 sub-samples separately and used the standard deviation of these results as the statistical uncertainty.

## Results

| Bacterial strain | Average per valid event | Statistical uncertainty |
|---|---:|---:|
| E. coli (wild type) | 19.9640 | ± 0.0328 |
| E. coli (mutant) | 19.9317 | ± 0.0319 |
| B. subtilis (wild type) | 2.5110 | ± 0.0048 |
| B. subtilis (mutant) | 2.5053 | ± 0.0055 |
| P. aeruginosa (wild type) | 1.2089 | ± 0.0019 |
| P. aeruginosa (mutant) | 1.1850 | ± 0.0024 |
| S. pneumoniae (wild type) | 0.27680 | ± 0.00108 |
| S. pneumoniae (mutant) | 0.27189 | ± 0.00099 |
| M. tuberculosis (wild type) | 0.03947 | ± 0.00028 |
| M. tuberculosis (mutant) | 0.03903 | ± 0.00040 |
| S. enterica (wild type) | 0.001188 | ± 0.000042 |
| S. enterica (mutant) | 0.001152 | ± 0.000051 |

## Wild type vs mutant comparison

The difference between the wild type and mutant strains was also calculated. The statistical uncertainty of each difference was calculated from the spread of the results from the 10 sub-samples.

| Bacterial strains | Mean difference per valid event | Statistical uncertainty |
|---|---:|---:|
| E. coli WT vs mutant | 0.03232 | ± 0.00452 |
| B. subtilis WT vs mutant | 0.00570 | ± 0.00330 |
| P. aeruginosa WT vs mutant | 0.02389 | ± 0.00237 |
| S. pneumoniae WT vs mutant | 0.00491 | ± 0.00058 |
| M. tuberculosis WT vs mutant | 0.000441 | ± 0.000488 |
| S. enterica WT vs mutant | 0.0000355 | ± 0.0000686 |