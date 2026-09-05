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
    - 3D momentum vectors (px, py, pz in 10^-20 kg·m/s or 10⁻²⁰ kg·m/s)
    - Integer ID representing the bacterial strain or genetic variant

---

## Installation & Environment Setup

### Prerequisites
- Python 3.9+
- Git

### Setup Instructions
1. Clone the repository and navigate to the project root:
   ```bash
   git clone [https://github.com/Aleksandra8880/python1.git](https://github.com/Aleksandra8880/python1.git)
cd python1
