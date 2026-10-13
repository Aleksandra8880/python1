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

# Sets 1 to 10 (excluding Set0)
FILE_NUMBERS = range(1, 11)

# Folder to store all output PNG figures
OUTPUT_DIR = "plots"

# Momentum bins: 30 bins from 0 to 60 (bin width = 2)
NUM_BINS = 30
BIN_WIDTH = 2.0
BIN_CENTERS = [BIN_WIDTH * (i + 0.5) for i in range(NUM_BINS)]


def process_subsample(filename, target_ids):
    counts = {bac_id: 0 for bac_id in target_ids}
    p_binned_counts = {bac_id: [0] * NUM_BINS for bac_id in target_ids}
    total_events = 0

    with open(filename, "r") as infile:
        while True:
            header_line = infile.readline()
            if not header_line:
                break

            parts = header_line.split()
            if not parts:
                continue

            # Count EVERY event/collision in the file
            total_events += 1
            num_bacteria = int(parts[1])

            for _ in range(num_bacteria):
                bac_line = infile.readline()
                tokens = bac_line.split()
                if not tokens:
                    continue

                # ID is at index 3 (px=0, py=1, pz=2, ID=3)
                try:
                    bac_id = int(tokens[3])
                except (IndexError, ValueError):
                    bac_id = int(tokens[-1])  # fallback

                if bac_id in counts:
                    counts[bac_id] += 1

                    # Momentum p = sqrt(px^2 + py^2 + pz^2)
                    if len(tokens) >= 3:
                        px = float(tokens[0])
                        py = float(tokens[1])
                        pz = float(tokens[2])
                        p = math.sqrt(px**2 + py**2 + pz**2)

                        bin_idx = int(p // BIN_WIDTH)
                        if 0 <= bin_idx < NUM_BINS:
                            p_binned_counts[bac_id][bin_idx] += 1

    # Normalize by all events in the subsample
    norm = total_events if total_events > 0 else 1.0

    means = {bac_id: (counts[bac_id] / norm) for bac_id in target_ids}

    p_means = {
        bac_id: [(c / norm) for c in p_binned_counts[bac_id]]
        for bac_id in target_ids
    }

    return means, p_means


def main():
    # Create the output directory if it doesn't already exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    target_ids = [bac_id for bac_id, _ in STRAINS]
    subsample_means = {bac_id: [] for bac_id in target_ids}
    batch_differences = {name: [] for name, _, _ in PAIRS}
    p_batch_differences = {name: [] for name, _, _ in PAIRS}

    for i in FILE_NUMBERS:
        filename = f"output-Set{i}.txt"
        if not os.path.exists(filename):
            filename = os.path.join("PRA2003", f"output-Set{i}.txt")

        if not os.path.exists(filename):
            print(f"File {filename} not found, skipping...")
            continue

        print(f"Processing {filename}...")
        means, p_means = process_subsample(filename, target_ids)

        for bac_id in target_ids:
            subsample_means[bac_id].append(means[bac_id])

        for name, wt_id, mut_id in PAIRS:
            diff = means[wt_id] - means[mut_id]
            batch_differences[name].append(diff)

            p_diff = [p_means[wt_id][b] - p_means[mut_id][b] for b in range(NUM_BINS)]
            p_batch_differences[name].append(p_diff)

    # Print individual strain averages and uncertainties
    print("\nFinal average bacterial counts:\n")
    for bac_id, name in STRAINS:
        vals = subsample_means[bac_id]
        n_samples = len(vals)

        if n_samples < 2:
            continue

        mean = sum(vals) / n_samples
        if mean == 0:
            continue

        variance = sum((x - mean) ** 2 for x in vals) / (n_samples - 1)
        uncertainty = math.sqrt(variance) / math.sqrt(n_samples)

        print(f"{name} {mean} ± {uncertainty}")

    # Print WT vs Mutant difference and uncertainty
    print("\nWT vs Mutant differences:")
    final_diffs = []
    final_uncerts = []
    pair_names = []

    for name, _, _ in PAIRS:
        diffs = batch_differences[name]
        n_samples = len(diffs)

        if n_samples < 2:
            continue

        diff_mean = sum(diffs) / n_samples
        diff_var = sum((x - diff_mean) ** 2 for x in diffs) / (n_samples - 1)
        diff_uncertainty = math.sqrt(diff_var) / math.sqrt(n_samples)

        print(f"{name} difference: {diff_mean} ± {diff_uncertainty}")

        pair_names.append(name)
        final_diffs.append(diff_mean)
        final_uncerts.append(diff_uncertainty)

    # Overall Asymmetry Plot (All species)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.errorbar(
        pair_names,
        final_diffs,
        yerr=final_uncerts,
        fmt="o",
        color="b",
        ecolor="red",
        elinewidth=2,
        capsize=5,
        capthick=1.5,
        markersize=7,
    )
    ax.axhline(0, color="gray", linestyle="--", linewidth=1.2, label="Zero Difference (Symmetry)")
    ax.set_ylabel(r"Difference $(\langle\mathrm{WT}\rangle - \langle\mathrm{Mutant}\rangle)$ per event", fontsize=12)
    ax.set_title("Wild Type vs. Mutant Bacterial Count Difference (Subsampling)", fontsize=14, fontweight="bold")
    ax.grid(axis="y", linestyle=":", alpha=0.6)
    ax.legend(frameon=True)
    plt.xticks(rotation=25, ha="right", fontsize=11)
    plt.tight_layout()

    # Save to plots directory
    plt.savefig(os.path.join(OUTPUT_DIR, "wt_mutant_differences.png"), dpi=300)
    plt.show()

    # Momentum Asymmetry Plots (Loops through every bacterium)
    for name, _, _ in PAIRS:
        batches_p_diff = p_batch_differences[name]
        n_batches = len(batches_p_diff)

        if n_batches < 2:
            continue

        p_means_list = []
        p_uncert_list = []

        for b in range(NUM_BINS):
            vals_in_bin = [batches_p_diff[k][b] for k in range(n_batches)]
            m_bin = sum(vals_in_bin) / n_batches
            v_bin = sum((x - m_bin) ** 2 for x in vals_in_bin) / (n_batches - 1)
            u_bin = math.sqrt(v_bin) / math.sqrt(n_batches)

            p_means_list.append(m_bin)
            p_uncert_list.append(u_bin)

        # Skip plotting if species has zero counts across all bins
        if all(val == 0 for val in p_means_list):
            continue

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.errorbar(
            BIN_CENTERS,
            p_means_list,
            yerr=p_uncert_list,
            fmt="o",
            color="b",
            ecolor="red",
            elinewidth=2,
            capsize=4,
            markersize=6,
            label=r"Mean asymmetry $\pm$ SEM",
        )
        ax.axhline(0, color="gray", linestyle="--", linewidth=1.2, label="Zero Asymmetry")
        ax.set_xlabel(r"Momentum, $p$ ($10^{-20}$ kg m s$^{-1}$)", fontsize=12)
        ax.set_ylabel("Mean abundance asymmetry (WT - mutant)", fontsize=12)
        ax.set_title(f"{name} abundance asymmetry as a function of momentum", fontsize=14, fontweight="bold")
        ax.grid(axis="both", linestyle=":", alpha=0.6)
        ax.legend(frameon=True)
        plt.tight_layout()

        # Save each species plot to the plots directory
        clean_name = name.replace(" ", "_").replace(".", "")
        plt.savefig(os.path.join(OUTPUT_DIR, f"{clean_name}_momentum_asymmetry.png"), dpi=300)
        plt.show()


if __name__ == "__main__":
    main()
