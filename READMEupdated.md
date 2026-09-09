# Monitoring Bacterial Movement and Populations 🧫
PRA2003 Programming Skill - Group Python 1 (Zofia Cebulska, Cecilia Zanardi, Aleksandra Chmielewska, Lisa O'Houlihan, Rafaella Tokatlidou, Sofija Ponomarjova)
## Introduction
This project will analyze simulated data from a bacterial tracking experiment under specific nutrient and stress conditions.
The goal is to compare the following wild type and mutant bacterial strains in terms of their abundance and momentum: 
- *Escherichia coli* (wild type and mutant)  
- *Bacillus subtilis* (wild type and mutant)  
- *Pseudomonas aeruginosa* (wild type and antibiotic-resistant mutant)
- *Streptococcus pneumoniae* (wild type and capsule-deficient mutant)
- *Mycobacterium tuberculosis* (wild type and drug-resistant mutant)
- *Salmonella enterica* (wild type and mutant)
## Input Structure 
The dataset consists of 3D momentum components and the corresponding bacterial strain. The header contains the event ID and the number of bacteria tracked, while each row provides information about the momentum components in the x, y, and z directions (10<sup>-20</sup> kg·m/s) and the bacterial ID.
## Research Questions 
The project will aim to answer the following questions: 
1. What are the average counts of each bacterial strain and their statistical uncertainties?
2. Is there any asymmetry between the normal and the mutant strain? If so, is that difference statistically significant?
3. Is there an asymmetry between the normal and mutant strains as a function of their momentum? If so, is that difference statistically singificant? 

 