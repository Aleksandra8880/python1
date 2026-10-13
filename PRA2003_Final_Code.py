# PRA2003 - Final Bacteria Analysis
# Bacterial abundance and momentum comparison

import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Bacterial strains and their IDs
pairs = [
    ("E. coli", 211, -211),
    ("B. subtilis", 321, -321),
    ("P. aeruginosa", 2212, -2212),
    ("S. pneumoniae", 3122, -3122),
    ("M. tuberculosis", 3312, -3312),
    ("S. enterica", 3334, -3334)
]

bacteria = {}

for name, normal_id, variant_id in pairs:
    bacteria[normal_id] = f"{name} WT"
    bacteria[variant_id] = f"{name} variant"


# Calculate the mean and standard deviation
def mean_sd(values):
    mean = statistics.mean(values)

    if len(values) > 1:
        sd = statistics.stdev(values)
    else:
        sd = 0.0

    return mean, sd


# Save results to a CSV file
def save_csv(folder, filename, headings, rows):
    filepath = folder / filename

    with filepath.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headings)
        writer.writerows(rows)


# Analyse one dataset file
def analyse_file(filepath, bin_widths):
    counts = {bacteria_id: 0 for bacteria_id in bacteria}
    momentum_bins = {bacteria_id: defaultdict(int) for bacteria_id in bacteria}

    total_events = 0
    valid_events = 0
    invalid_lines = 0

    with filepath.open(encoding="utf-8") as file:
        while True:
            header = file.readline()

            if not header:
                break

            if not header.strip():
                continue

            values = header.split()

            if len(values) != 2:
                raise ValueError(f"{filepath.name}: invalid event header")

            try:
                event_number = int(values[0])
                number_of_entries = int(values[1])
            except ValueError:
                raise ValueError(f"{filepath.name}: invalid event header")

            if number_of_entries < 0:
                raise ValueError(f"{filepath.name}: negative particle count")

            total_events += 1
            valid_current_event = False

            # Read all bacterial entries belonging to this event
            for _ in range(number_of_entries):
                line = file.readline()

                if not line:
                    raise ValueError(
                        f"{filepath.name}: incomplete event {event_number}"
                    )

                values = line.split()

                if len(values) != 4:
                    invalid_lines += 1
                    continue

                try:
                    px = float(values[0])
                    py = float(values[1])
                    pz = float(values[2])
                    bacteria_id = int(values[3])

                    if not all(math.isfinite(p) for p in (px, py, pz)):
                        raise ValueError

                except ValueError:
                    invalid_lines += 1
                    continue

                if bacteria_id in counts:
                    counts[bacteria_id] += 1
                    valid_current_event = True

                    # Calculate the total momentum from px, py and pz
                    momentum = math.sqrt(px**2 + py**2 + pz**2)

                    # Only include momentum values below 60
                    if momentum < 60:
                        width = bin_widths[abs(bacteria_id)]
                        bin_number = int(momentum / width)
                        momentum_bins[bacteria_id][bin_number] += 1

            # Count the event only if it contained a selected bacterium
            if valid_current_event:
                valid_events += 1

    if valid_events == 0:
        raise ValueError(f"{filepath.name}: no valid events")

    return {
        "filename": filepath.name,
        "events": total_events,
        "valid": valid_events,
        "invalid": invalid_lines,
        "counts": counts,
        "bins": momentum_bins
    }


# Create and save momentum graphs
def plot_momentum(folder, filename, title, x, y, width=None, errors=None):
    fig, ax = plt.subplots(figsize=(9, 5))

    if errors is None:
        ax.bar(
            x, y,
            width=width,
            color="mediumpurple",
            edgecolor="black",
            linewidth=0.2
        )
        ax.set_ylabel("Bacteria (pooled counts)")

    else:
        ax.errorbar(
            x, y,
            yerr=errors,
            fmt="o",
            markersize=3,
            color="indigo",
            ecolor="mediumvioletred",
            capsize=2
        )

        ax.axhline(0, color="grey", linestyle="--")
        ax.set_ylabel("Mean WT - variant counts per subsample")

    ax.set_xlabel("Momentum (raw dataset units)")
    ax.set_title(title)
    ax.grid(axis="y", alpha=0.25)

    fig.tight_layout()
    fig.savefig(folder / filename, dpi=180)
    plt.close(fig)


# Main analysis
def main():

    print("\n==========================================")
    print("        PRA2003 FINAL BACTERIA ANALYSIS")
    print("==========================================")

    # Find the dataset files
    root = Path(__file__).resolve().parent

    if (root / "data").is_dir():
        data_folder = root / "data"
    else:
        data_folder = root

    # Set0 only contains one event so it is excluded
    files = [
        data_folder / f"output-Set{i}.txt"
        for i in range(1, 11)
    ]

    missing = [file.name for file in files if not file.is_file()]

    if missing:
        print("\nMissing dataset files:")
        for filename in missing:
            print(f"- {filename}")
        return

    figures_folder = root / "figures"
    results_folder = root / "results"

    figures_folder.mkdir(exist_ok=True)
    results_folder.mkdir(exist_ok=True)

    # Use smaller momentum bins for E. coli
    bin_widths = {
        normal_id: (1 if normal_id == 211 else 2)
        for _, normal_id, _ in pairs
    }

    print("\n==========================================")
    print("             DATASET ANALYSIS")
    print("==========================================")

    file_results = []

    # Analyse the ten sub-samples separately
    for filepath in files:
        print(f"\nAnalysing {filepath.name}...")

        result = analyse_file(filepath, bin_widths)
        file_results.append(result)

        print(f"Events found: {result['events']}")
        print(f"Valid events: {result['valid']}")
        print(f"Invalid lines: {result['invalid']}")

    # Combine the results from all ten sub-samples
    total_events = sum(result["events"] for result in file_results)
    total_valid = sum(result["valid"] for result in file_results)
    total_invalid = sum(result["invalid"] for result in file_results)

    total_selected = sum(
        sum(result["counts"].values())
        for result in file_results
    )

    print("\n==========================================")
    print("             OVERALL SUMMARY")
    print("==========================================")

    print(f"\nSub-samples analysed: {len(file_results)}")
    print(f"Total events analysed: {total_events:,}")
    print(f"Total valid events: {total_valid:,}")
    print(f"Total invalid lines: {total_invalid:,}")
    print(f"Total selected bacteria: {total_selected:,}")

    # Save the information for each sub-sample
    subsample_rows = []

    for result in file_results:
        subsample_rows.append([
            result["filename"],
            result["events"],
            result["valid"],
            result["invalid"],
            sum(result["counts"].values())
        ])

    save_csv(
        results_folder,
        "subsamples.csv",
        ["file", "events", "valid_events", "invalid_lines", "bacteria"],
        subsample_rows
    )

    print("\n==========================================")
    print("             BACTERIAL ABUNDANCE")
    print("==========================================")

    abundance_results = []

    # Calculate the average abundance for every strain
    for bacteria_id, name in bacteria.items():
        total_count = sum(
            result["counts"][bacteria_id]
            for result in file_results
        )

        average = total_count / total_valid

        subsample_averages = [
            result["counts"][bacteria_id] / result["valid"]
            for result in file_results
        ]

        mean, sd = mean_sd(subsample_averages)
        sem = sd / math.sqrt(len(subsample_averages))

        abundance_results.append([
            bacteria_id,
            name,
            total_count,
            average,
            mean,
            sd,
            sem
        ])

        print(f"\n{name} (ID: {bacteria_id})")
        print(f"Total count: {total_count:,}")
        print(f"Average per valid event: {average:.8f}")
        print(f"Standard deviation: {sd:.8f}")

    save_csv(
        results_folder,
        "abundance.csv",
        [
            "id",
            "strain",
            "total_count",
            "pooled_mean_per_valid_event",
            "mean_of_subsample_averages",
            "sample_sd",
            "sem"
        ],
        abundance_results
    )

    print("\n==========================================")
    print("         NORMAL VS VARIANT COMPARISON")
    print("==========================================")

    difference_results = []

    for name, normal_id, variant_id in pairs:

        # Compare the two strains within each sub-sample
        differences = [
            (
                result["counts"][normal_id]
                - result["counts"][variant_id]
            ) / result["valid"]
            for result in file_results
        ]

        mean_difference, difference_sd = mean_sd(differences)
        difference_sem = difference_sd / math.sqrt(len(differences))

        difference_results.append([
            name,
            mean_difference,
            difference_sd,
            difference_sem
        ])

        print(f"\n{name}")
        print(f"Mean difference per valid event: {mean_difference:.8f}")
        print(f"Standard deviation: {difference_sd:.8f}")

        # Create the individual momentum histograms
        width = bin_widths[normal_id]
        combined_bins = defaultdict(int)

        for bacteria_id in (normal_id, variant_id):
            total_bins = defaultdict(int)

            for result in file_results:
                for bin_number, count in result["bins"][bacteria_id].items():
                    total_bins[bin_number] += count
                    combined_bins[bin_number] += count

            bin_numbers = sorted(total_bins)

            x_values = [
                (bin_number + 0.5) * width
                for bin_number in bin_numbers
            ]

            y_values = [
                total_bins[bin_number]
                for bin_number in bin_numbers
            ]

            plot_momentum(
                figures_folder,
                f"momentum_{bacteria_id}.png",
                bacteria[bacteria_id],
                x_values,
                y_values,
                width=width
            )

        # Create the combined momentum histogram
        bin_numbers = sorted(combined_bins)

        x_values = [
            (bin_number + 0.5) * width
            for bin_number in bin_numbers
        ]

        y_values = [
            combined_bins[bin_number]
            for bin_number in bin_numbers
        ]

        plot_momentum(
            figures_folder,
            f"momentum_combined_{normal_id}_{variant_id}.png",
            f"{name}: combined",
            x_values,
            y_values,
            width=width
        )

        # Calculate the WT minus variant counts for each momentum bin
        momentum_rows = []
        number_of_samples = len(file_results)

        for bin_number in range(math.ceil(60 / width)):
            normal_count = sum(
                result["bins"][normal_id].get(bin_number, 0)
                for result in file_results
            )

            variant_count = sum(
                result["bins"][variant_id].get(bin_number, 0)
                for result in file_results
            )

            mean_difference = (
                normal_count - variant_count
            ) / number_of_samples

            # Poisson uncertainty for the difference in counts
            # The variances are added even though the counts are subtracted
            poisson_error = math.sqrt(
                normal_count + variant_count
            ) / number_of_samples

            momentum_rows.append([
                (bin_number + 0.5) * width,
                mean_difference,
                poisson_error
            ])

        save_csv(
            results_folder,
            f"momentum_difference_{normal_id}_{variant_id}.csv",
            [
                "momentum_bin_centre",
                "mean_WT_minus_variant_counts",
                "poisson_error_on_mean"
            ],
            momentum_rows
        )

        # Plot the momentum differences with Poisson error bars
        plot_momentum(
            figures_folder,
            f"asymmetry_{normal_id}_{variant_id}.png",
            f"{name}: mean difference ± Poisson uncertainty",
            [row[0] for row in momentum_rows],
            [row[1] for row in momentum_rows],
            errors=[row[2] for row in momentum_rows]
        )

    save_csv(
        results_folder,
        "differences.csv",
        [
            "species",
            "mean_difference_per_valid_event",
            "sample_sd",
            "sem"
        ],
        difference_results
    )

    print("\n==========================================")
    print("             ANALYSIS COMPLETED")
    print("==========================================")

    print(f"\n24 figures saved to: {figures_folder}")
    print(f"9 CSV files saved to: {results_folder}")


if __name__ == "__main__":
    main()
