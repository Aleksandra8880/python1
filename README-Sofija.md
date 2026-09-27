# **Monitoring Bacterial Movement and Populations**
## _Description_
This project aims to compare the bacterial movement and population growth under specific nutrient or stress conditions. 

The data were obtained from a simulation of bacterial tracking experiment. Each input contains the ID of experiment run, number of bacteria tracked, their 3D momentum components (px, py, pz) in 10⁻²⁰ kg m/s and ID of bacterial strain or genetic variant.

The data set contains following bacterial strains:

* _E. coli WT_ (wild type)
* _E. coli mutant_
* _Bacillus subtilis WT_
* _Bacillus subtilis mutant_
* _Pseudomonas aeruginosa WT_
* _Pseudomonas aeruginosa antibiotic-resistant_
* _Streptococcus pneumoniae_
* _Capsule-deficient streptococcus pneumoniae_
* _Mycobacterium tuberculosis_
* _Drug-resistant mycobacterium tuberculosis_
* _Salmonella enterica_
* _Salmonella mutant_

## _Research Questions_
The project focuses on answering the following research questions:

1. What are the average counts and statistical uncertainties of each bacterial strain?
2. Is there any asymmetry between the normal and the mutant strain, if so - how large is it?
3. Is there any asymmetry between the normal and the mutant strain as a function of their momentum?

## _Installation_
1. Make sure you have Python 3 installed. No additional packages are required, only Python's standart library.

2. Clone the repository
```bash
git clone https://github.com/sofijaponomarjova/Monitoring-Bacterial-Movement-and-Population.git
cd Monitoring-Bacterial-Movement-and-Population
```
**Alternatively, download the repository as a ZIP file:**
* Press green button "<> Code"
* Click "Download ZIP"

**Dataset**

You can downoload the dataset files here: https://surfdrive.surf.nl/index.php/s/7udCnWTk4yMUASD 
## _Usage_
1. Open the folder
2. Run in Terminal

```python3 task2.py```

This program cleans the data and then calculates the momentum for each bacteria.

## Results

E. coli WT average: 19.964042225262727 ± 0.03109117275389914

E. coli mutant average: 19.931721898491062 ± 0.030227891773527003

Bacillus subtilis WT average: 2.5109760539147103 ± 0.004516178392308326

Bacillus subtilis mutant average: 2.5052808669341133 ± 0.005227600707582858

Pseudomonas aeruginosa WT average: 1.2089141646344372 ± 0.0018175493915266539

Pseudomonas aeruginosa antibiotic-resistant average: 1.1850237360153653 ± 0.002294977826980593

Streptococcus pneumoniae average: 0.27680009057491506 ± 0.0010209803872882224

Capsule-deficient streptococcus pneumoniae average: 0.2718939099983327 ± 0.0009346949138909668

Mycobacterium tuberculosis average: 0.03946993773442613 ± 0.00026898271608880936

Drug-resistant mycobacterium tuberculosis average: 0.039028935218028325 ± 0.0003811027180490271

Salmonella enterica average: 0.001187962955206821 ± 3.9560943945588565e-05

Salmonella mutant average: 0.0011524239744295493 ± 4.822439205619068e-05