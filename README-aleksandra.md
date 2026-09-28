## Topic
**Monitoring bacterial movement and populations**

Each row of the input file contains all three momentum components of different bacterial strains with the corresponding ID code. Therefore the population of all bacteria types is represented by the number of rows. We can analyse the mobility and number of each species. The measurements were taken under different conditions such as: stress and nutrients. 

$$
p = \sqrt{{p_{x}}^2 + {p_{y}}^2 + {p_{z}}^2 }
$$

## Strains analyzed
- E.coli WT
- E.coli mutant
- Bacillus subtilis WT
- Bacillus subtilis mutant
- Pseudomonas aeruginosa WT
- Pseudomonas aeruginosa antibiotic-resistant
- Streptococcus pneumoniae
- Capsule-deficient streptococcus pneumoniae
- Mycobacterium tuberculosis
- Drug-resistant mycobacterium tuberculosis
- Salmonella enteric
- Salmonella mutant

## Research outcomes:
For 211 the average from all files is 19.96404222526273 with standard deviation 0.03277297367603035
For -211 the average from all files is 19.931721898491062 with standard deviation 0.031862995623137325
For 321 the average from all files is 2.5109760539147103 with standard deviation 0.004760470013110587
For -321 the average from all files is 2.505280866934113 with standard deviation 0.005510374977956562
For 2212 the average from all files is 1.2089141646344372 with standard deviation 0.0019158652790257896
For -2212 the average from all files is 1.1850237360153653 with standard deviation 0.002419119037614167
For 3122 the average from all files is 0.276800090574915 with standard deviation 0.0010762078233972018
For -3122 the average from all files is 0.2718939099983327 with standard deviation 0.0009852549484234705
For 3312 the average from all files is 0.039469937734426135 with standard deviation 0.0002835326780196851
For -3312 the average from all files is 0.03902893521802833 with standard deviation 0.00040171753717196235
For 3334 the average from all files is 0.001187962955206821 with standard deviation 4.1700896418102735e-05
For -3334 the average from all files is 0.0011524239744295493 with standard deviation 5.083297255816441e-05

Assymetry of pair (211, -211) is 0.0008101192565559722 
Assymetry of pair (321, -321) is 0.0011353459502695781
Assymetry of pair (2212, -2212) is 0.009979552357054559
Assymetry of pair (3122, -3122) is 0.008941560453470589
Assymetry of pair (3312, -3312) is 0.00561794710944335
Assymetry of pair (3334, -3334) is 0.01518508769949144

The wild strains are more present within the sample.

As a part of investigation the weighted average was a also calculated, taking the event_count of each file as a weight. However, the difference between the averages was not significant. The analyzed sub-samples were all similar size, therefore this simplification is reasonable and supports the expected outcomes.
## Questions to address: ##
- What are the average counts of each bacterial strain and their statistical uncertainties? 
- Is there any asymmetry between the normal and the mutant strain? 
- Is there any asymmetry as a function of their momentum? 

## Libraries Used
- python
- matplotlib
- Path
- statistics
- math
- 
## Example of use
## Installation

## License
This project is licensed under the MIT License.
