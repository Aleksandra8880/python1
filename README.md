# Monitoring bacterial movement and populations

## Introduction
This project focuses on monitoring bacterial movement and populations using simulated
data from bacterial tracking experiments. Bacterial movement and proliferation under specific nutrient or stress conditions is modelled by the simulation.

The analysis will  compare different bacterial strains and genetic variants, investigate their abundance, and determine whether differences exist between normal and mutant strains. 

## Data
Each input file represents the simulated output of a bacterial tracking experiment.
The header of each file contains an event ID, which identifies the experiment or
simulation run, and the total number of bacterial cells tracked in that event.

The subsequent row contains the three-dimensional momentum components px, py and pz, as well as an integer ID that identifies the bacterial strain or genetic variant.

## Momentum
The movement of each bacterium is described by three momentum components: px, py and pz.
The total momentum can be calculated from these components using:

$$
p = \sqrt{p_x^2 + p_y^2 + p_z^2}
$$ 

This will later be used to verify whether the difference between normal and mutant bacterial strains depends on momentum.

## Research Questions
The analysis will aim to answer the following questions:

1. What are the average counts of each bacterial strain and their statistical uncertainties?

2. Is there an asymmetry between the normal and mutant bacterial strains? If so, how large is this asymmetry?

3. Is there an asymmetry between the normal and mutant bacterial strains as a function of their momentum?
