import numpy as np

########################################################
# INTPUT FILES
########################################################
directory = "PRA2003"
filenames = []
for i in range(1, 11):
    filenames.append(f"{directory}/output-Set{i}.txt")

########################################################
# STRAIN DICTIONARY
########################################################
bacterial_strains = { 
    "211": "E. coli (wild type)",
    "-211": "E. coli (mutant)",
    "321": "B. subtilis (wild type)",
    "-321": "B. subtilis (mutant)",
    "2212": "P. aeruginosa (wild type)",
    "-2212": "P. aeruginosa (mutant)",
    "3122": "S. pneumoniae (wild type)",
    "-3122": "S. pneumoniae (mutant)",
    "3312": "M. tuberculosis (wild type)",
    "-3312": "M. tuberculosis (mutant)",
    "3334": "S. enterica (wild type)",
    "-3334": "S. enterica (mutant)"
}

########################################################
# COUNT FUNCTION (per batch)
########################################################
def count(filename):
    experiment_count = 0  
    bacteria_count = {}  
    for bacterial_ID in bacterial_strains:  
        bacteria_count[bacterial_ID] = 0 
    current_line = 0  
    with open(filename, "r") as infile:
        for header in infile:  
            current_line += 1  
            try:   
                experiment_info = header.split()  
                rows = int(experiment_info[1])  
            except (IndexError, ValueError):
                raise ValueError(f"Invalid header at line {current_line}. Analysis stopped.")
            if rows < 0:  
                raise ValueError(f"Invalid header at line {current_line}. Analysis stopped.")
            if rows >= 1:  
                valid_experiment = False 
                for _ in range(rows):  
                    row = next(infile)  
                    current_line += 1  
                    row_info = row.split()  
                    bacterial_ID = row_info[3]  
                    if bacterial_ID in bacterial_strains:  
                        valid_experiment = True 
                        bacteria_count[bacterial_ID] += 1  
                if valid_experiment == True:
                    experiment_count += 1  
    return bacteria_count, experiment_count

########################################################
# AVERAGE FUNCTION (per batch)
########################################################
def average(bacteria_count, experiment_count):
    average_count = {}
    for bacterial_ID in bacteria_count:
        average_count[bacterial_ID] = bacteria_count[bacterial_ID] / experiment_count
    return average_count

########################################################
# NORMAL AVERAGES FUNCTION (10 batches)
########################################################
def normal_average(batch_results):
    normal_averages = {}

    for bacterial_ID in bacterial_strains:
        total = 0

        for filename in filenames:
            total += batch_results[filename]["averages"][bacterial_ID]

        normal_averages[bacterial_ID] = total / 10

    return normal_averages

########################################################
# WEIGHTED AVERAGES FUNCTION (10 batches)
########################################################
def weighted_average(batch_results):
    weighted_averages = {}

    for bacterial_ID in bacterial_strains:
        weighted_total = 0
        total_experiments = 0

        for filename in filenames:
            batch_average = batch_results[filename]["averages"][bacterial_ID]
            experiment_count = batch_results[filename]["experiments"]

            weighted_total += batch_average * experiment_count
            total_experiments += experiment_count

        weighted_averages[bacterial_ID] = weighted_total / total_experiments

    return weighted_averages

########################################################
# UNCERTAINTY FUNCTION (10 batches)
########################################################
def uncertainty(batch_results):
    uncertainties = {}

    for bacterial_ID in bacterial_strains:
        batch_averages = []

        for filename in filenames:
            batch_averages.append(
                batch_results[filename]["averages"][bacterial_ID]
            )

        uncertainties[bacterial_ID] = np.std(batch_averages)

    return uncertainties

########################################################
# MEAN DIFFERENCE FUNCTION (WT vs. mutated) / final values!
########################################################
def difference(normal_averages):

    differences = {}

    for bacterial_ID in bacterial_strains:
        if int(bacterial_ID) > 0:  # only go through WT IDs
            mutant_ID = str(-int(bacterial_ID))

            differences[bacterial_ID] = (normal_averages[bacterial_ID]- normal_averages[mutant_ID])

    return differences

########################################################
# MUTANT VS WILDTYPE FUNCTION / batch values!
########################################################
def mutant_vs_wildtype(batch_results):
    batch_differences = {}

    for bacterial_ID in bacterial_strains:
        if int(bacterial_ID) > 0:  # only go through WT IDs
            mutant_ID = str(-int(bacterial_ID))

            differences = []

            for filename in filenames:
                wt_average = batch_results[filename]["averages"][bacterial_ID]
                mutant_average = batch_results[filename]["averages"][mutant_ID]

                differences.append(wt_average - mutant_average)

            batch_differences[bacterial_ID] = differences

    return batch_differences

########################################################
# DIFFERENCE UNCERTAINTY FUNCTION (WT - mutant per batch: standard deviations of the 10 subsamples)
########################################################
def difference_uncertainty(batch_differences):
    difference_uncertainties = {}

    for bacterial_ID in batch_differences:
        difference_uncertainties[bacterial_ID] = np.std(batch_differences[bacterial_ID])

    return difference_uncertainties

########################################################
# CALLING FUNCTIONS & PRINTING RESULTS: average per batch
########################################################
batch_results = {}

for filename in filenames:
    bacteria_count, experiment_count = count(filename)
    average_count = average(bacteria_count, experiment_count)

    batch_results[filename] = {
        "experiments": experiment_count,
        "averages": average_count
    }

    print()
    print(filename)
    print("Valid experiments:", batch_results[filename]["experiments"])

    for bacterial_ID in bacterial_strains:
        print(
            bacterial_strains[bacterial_ID],
            batch_results[filename]["averages"][bacterial_ID]
        )

########################################################
# CALLING FUNCTIONS & PRINTING RESULTS: final average + uncertainty
########################################################
uncertainties = uncertainty(batch_results)

print()
print("Final average bacterial counts:")

for bacterial_ID in bacterial_strains:
    print(
        bacterial_strains[bacterial_ID],
        f"{normal_averages[bacterial_ID]} ± {uncertainties[bacterial_ID]}"
    )

########################################################
# CALLING FUNCTIONS & PRINTING RESULTS: WT vs. mutated average difference
########################################################

differences = difference(normal_averages)
print()
print("WT - mutant mean differences:")

for bacterial_ID in differences:
    print(bacterial_strains[bacterial_ID], differences[bacterial_ID])

########################################################
# CALLING FUNCTIONS & PRINTING RESULTS: mutant vs wildtype PER BATCH
########################################################
batch_differences = mutant_vs_wildtype(batch_results)
print()
print("WT - mutant differences for each batch:")

for bacterial_ID in batch_differences:
    print(bacterial_strains[bacterial_ID],batch_differences[bacterial_ID])

########################################################
# CALLING FUNCTIONS & PRINTING RESULTS: final asymmetries with uncertainties
########################################################

difference_uncertainties = difference_uncertainty(batch_differences)
print()
print("WT - mutant differences with uncertainties:")

for bacterial_ID in differences:
    print(
        bacterial_strains[bacterial_ID],
        f"{differences[bacterial_ID]} ± "
        f"{difference_uncertainties[bacterial_ID]}"
    )

########################################################
# VISUALIZING RESULTS
########################################################


import matplotlib.pyplot as plt 

species = [
    "E. coli",
    "B. subtilis",
    "P. aeruginosa",
    "S. pneumoniae",
    "M. tuberculosis",
    "S. enterica"
]

differences = [
    0.0323203267716643,
    0.005695186980597899,
    0.023890428619071757,
    0.004906180576582375,
    0.0004410025163977954,
    3.5538980777271786e-05
]

uncertainties = [
    0.0042902526496286925,
    0.003126804988542691,
    0.002252841421777521,
    0.000553707068697177,
    0.00046324293250109836,
    6.50736814848038e-05
]

x = np.arange(len(species))

plt.errorbar(
    x,
    differences,
    yerr=uncertainties,
    color="#FCF6F5",
    ecolor="#990011",
    markeredgecolor="#990011",
    markeredgewidth=0.5,
    fmt="D",
    markersize=6,
    elinewidth=1.2,
    capsize=4,
    capthick=1.2,
    zorder=3
)

plt.xticks(x, species, fontfamily="serif", fontstyle="italic", rotation=20, ha="right")
plt.xticks(fontfamily="serif")
plt.axhline(y=0, color="black", linestyle="--", linewidth=1, alpha=0.7)
plt.grid(axis="y", linestyle=":", linewidth=0.7, alpha=0.3,zorder=0)

plt.xlabel("Bacterial species", fontfamily="serif", fontweight="bold", color="#990011")
plt.ylabel("Asymmetry", fontfamily="serif", fontweight="bold", color="#990011")

plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)

plt.tight_layout()
plt.show()
