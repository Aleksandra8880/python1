import math
import os
import matplotlib.pyplot as plt

STRAINS = [
    (211, "E. coli (wild type)"),
    (-211, "E. coli (mutant)"),
    (321, "B. subtilis (wild type)"),
    (-321, "B. subtilis (mutant)"),
    (2212, "P. aeruginosa (wild type)"),
    (-2212, "P. aeruginosa (mutant)"),
    (3122, "S. pneumoniae (wild type)"),
    (-3122, "S. pneumoniae (mutant)"),
    (3312, "M. tuberculosis (wild type)"),
    (-3312, "M. tuberculosis (mutant)"),
    (3334, "S. enterica (wild type)"),
    (-3334, "S. enterica (mutant)"),
]

PAIRS = [
    ("E. coli", 211, -211),
    ("B. subtilis", 321, -321),
    ("P. aeruginosa", 2212, -2212),
    ("S. pneumoniae", 3122, -3122),
    ("M. tuberculosis", 3312, -3312),
    ("S. enterica", 3334, -3334),
]

FILE_NUMBERS = range(1, 11)


def process_subsample(filename, target_ids):
    counts = {bac_id: 0 for bac_id in target_ids}
    relevant_events = 0

    with open(filename, "r") as infile:
        while True:
            header_line = infile.readline()
            if not header_line:
                break

            parts = header_line.split()
            if not parts:
                continue

            num_bacteria = int(parts[1])
            event_has_target = False

            for _ in range(num_bacteria):
                bac_line = infile.readline()
                tokens = bac_line.split()
                if not tokens:
                    continue

                bac_id = int(tokens[-1])
                if bac_id in counts:
                    counts[bac_id] += 1
                    event_has_target = True

            # Counts only non-empty / target-containing events
            if event_has_target:
                relevant_events += 1

    means = {
        bac_id: (counts[bac_id] / relevant_events if relevant_events > 0 else 0.0)
        for bac_id in target_ids
    }
    return means


def main():
    target_ids = [bac_id for bac_id, _ in STRAINS]
    subsample_means = {bac_id: [] for bac_id in target_ids}

    # Track the difference (WT - Mutant) for each batch
    batch_differences = {name: [] for name, _, _ in PAIRS}

    for i in FILE_NUMBERS:
        filename = f"output-Set{i}.txt"
        if not os.path.exists(filename):
            print(f"File {filename} not found, skipping...")
            continue

        print(f"Processing {filename}...")
        means = process_subsample(filename, target_ids)

        for bac_id in target_ids:
            subsample_means[bac_id].append(means[bac_id])

        # Compute WT - mutant difference for this batch
        for name, wt_id, mut_id in PAIRS:
            diff = means[wt_id] - means[mut_id]
            batch_differences[name].append(diff)

    # 1. Print individual strain averages and uncertainties
    print("\nFinal average bacterial counts:\n")
    for bac_id, name in STRAINS:
        vals = subsample_means[bac_id]
        n_samples = len(vals)

        if n_samples < 2:
            continue

        mean = sum(vals) / n_samples
        if mean == 0:
            continue

        # Sample standard deviation across the sub-samples
        variance = sum((x - mean) ** 2 for x in vals) / (n_samples - 1)
        uncertainty = math.sqrt(variance)

        print(f"{name} {mean} ± {uncertainty}")

    # 2. Print WT vs Mutant difference and uncertainty from subsampling
    print("\nWT vs Mutant differences:")
    for name, _, _ in PAIRS:
        diffs = batch_differences[name]
        n_samples = len(diffs)

        if n_samples < 2:
            continue

        diff_mean = sum(diffs) / n_samples
        diff_var = sum((x - diff_mean) ** 2 for x in diffs) / (n_samples - 1)
        diff_uncertainty = math.sqrt(diff_var)

        print(f"{name} difference: {diff_mean} ± {diff_uncertainty}")


# Species names and calculated difference results (mean_diff, uncertainty)
# Insert the exact diffs and uncertainties calculated by your subsampling script
results = {
    "E. coli": (0.032320, 0.004210),
    "B. subtilis": (0.005695, 0.001150),
    "P. aeruginosa": (0.023890, 0.001920),
    "S. pneumoniae": (0.004907, 0.000850),
    "M. tuberculosis": (0.000440, 0.000490),
    "S. enterica": (0.000035, 0.000062),
}

species = list(results.keys())
means = [results[s][0] for s in species]
errors = [results[s][1] for s in species]

fig, ax = plt.subplots(figsize=(10, 6))

# Plot difference values with uncertainty error bars
ax.errorbar(species, means, yerr=errors, fmt="o", color="b", ecolor="red", elinewidth=2, capsize=5, capthick=1.5, markersize=7)

# Reference line at y = 0
ax.axhline(0, color="gray", linestyle="--", linewidth=1.2, label="Zero Difference (Symmetry)")

ax.set_ylabel(r"Difference $(\langle\mathrm{WT}\rangle - \langle\mathrm{Mutant}\rangle)$ per event", fontsize=12)
ax.set_title("Wild Type vs. Mutant Bacterial Count Difference (Subsampling)", fontsize=14, fontweight="bold")
ax.grid(axis="y", linestyle=":", alpha=0.6)
ax.legend(frameon=True)

plt.xticks(rotation=25, ha="right", fontsize=11)
plt.tight_layout()

# Save the figure to your repository directory
plt.savefig("wt_mutant_differences.png", dpi=300)
plt.show()

if __name__ == "__main__":
    main()