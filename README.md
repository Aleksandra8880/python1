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

3. Is there an asymmetry between the normal and mutant bacterial strains as a function of their momentum? 

## Analysis

The full sample contained 5,000,000 events and was divided into 10 sub-samples of 500,000 events, each of which was analysed separately. In total, 4,614,632 valid events were used in the analysis.
 
The 10 files were analysed separately. For each bacterial strain, the total number of bacteria was counted and divided by the number of valid events in that file. The final average for each strain was calculated as the mean of the 10 sub sample averages.
 
The statistical uncertainty was estimated using the sub-sampling method, by calculating the standard deviation of the 10 subsample averages. 

For example, the average abundance of wild type e. coli was calculated by counting all bacteria with ID 211 in each file and dividing by the numbers of valid events. the mean on 10 results was 19.9640, with 0.0328 as standard deviation.

## Results

The average number of bacteria per valid event and the statistical uncertainty for each strain are shown below.

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

## Wild Type vs Mutant Comparison

To compare the wild type and mutant strains was also calculated as:
**difference= WT average - mutant average** 
The difference was calculated separately for each of the 10 sub-samples, the standard deviation of the 10 differences was used as the uncertainty.

| Bacterial strains | Mean difference per valid event | Statistical uncertainty |
|---|---:|---:|
| E. coli WT vs mutant | 0.03232 | ± 0.00452 |
| B. subtilis WT vs mutant | 0.00570 | ± 0.00330 |
| P. aeruginosa WT vs mutant | 0.02389 | ± 0.00237 |
| S. pneumoniae WT vs mutant | 0.00491 | ± 0.00058 |
| M. tuberculosis WT vs mutant | 0.000441 | ± 0.000488 |
| S. enterica WT vs mutant | 0.0000355 | ± 0.0000686 |

All 6 species showed a positive mean difference, meaning the wild type bacteria were slightly more abundant then their corresponding mutants. 

## Asymmetry as a Function of Momentum 
The final part of the analysis investigated the difference between wild type and mutant bacteria and how it changes depending on their momentum.
The analysis focused on  E. coli and S. pneumoniae.

## calculating momentum 
For each bacterium the total momentum was calculated from three components. 

$$ 
p = \sqrt{p_x^2 + p_y^2 + p_z^2} 
$$

The momentum values were then divided into bins between zero and 60 with E. coli having a bin width of 1 and S. pneumoniae of 2. Different bin width were used because E.coli was much more abundant then S. pneumoniae.

## calculating the asymmetry 
for each momentum bin, the number of wild type and mutant bacteria was counted separately in each of the 10 files. The difference was then calculated so the final graph shows the mean WT/mutant difference across the 10 sub samples.

## Statistical Uncertainty
Following the feedback received after our presentation, Poisson uncertainties were used for the momentum histograms instead of the standard deviation across the 10 sub-samples.

$$
\sigma = \sqrt{N}
$$

for the difference between two independent counts the authorities were combined.

$$
\sigma = \sqrt{N_{WT} + N_{mutant}}
$$

Since the graph shows the mean difference across 10 sub samples the uncertainty was divided by 10.

$$
\sigma_{\text{mean}} = \frac{\sqrt{N_{WT} + N_{mutant}}}{10}
$$

These uncertainties were displayed as error bars using plt.errorbar().

## momentum analysis
For E. coli, the WT–mutant difference was largest at the lowest momentum bins. As the momentum increase the difference generally decreased. A similar pattern was observed for S. pneumoniae.
The error bars represent the Poisson uncertainty of the mean count difference in every momentum bin

## Discussion 
The results show that wild type bacteria were generally more abundant than the mutant bacteria in the simulated data set. E. coli showing the largest difference in abundance.
The momentum analysis showed the WT-mutant difference was not constant across momentum but showed larger differences at lower momentum, which normally decreased as the momentum increased.

## Conclusion
The analysis answered the three research questions by calculating the average abundance of each bacterial strain, comparing wild-type and mutant strains, and investigating how their differences change with momentum.

Overall, wild-type bacteria were slightly more abundant than their corresponding mutants.

For E. coli and S. pneumoniae, the largest WT–mutant count differences were observed at lower momentum, with the differences generally decreasing as momentum increased.

The statistical uncertainties were estimated using the sub-sampling method for average abundances and overall differences, and Poisson uncertainties for the momentum histograms

## Libraries used
NumPy: calculations of momentum, means, and standard deviations.
Matplotlib: plotting the momentum-dependent differences with statistical error bars.
