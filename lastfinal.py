
import numpy as np
import matplotlib.pyplot as plt


def bacteria_analysis():

    # The 10 sub-samples
    files = ["data/output-Set1.txt", "data/output-Set2.txt",
             "data/output-Set3.txt", "data/output-Set4.txt",
             "data/output-Set5.txt", "data/output-Set6.txt",
             "data/output-Set7.txt", "data/output-Set8.txt",
             "data/output-Set9.txt", "data/output-Set10.txt"]

    # Wild type and mutant pairs
    pairs = [(211, -211, "E. coli"),
             (321, -321, "B. subtilis"),
             (2212, -2212, "P. aeruginosa"),
             (3122, -3122, "S. pneumoniae"),
             (3312, -3312, "M. tuberculosis"),
             (3334, -3334, "S. enterica")]

    # The two species for the momentum analysis
    # E. coli has bin width 1, S. pneumoniae has bin width 2
    focus_species = [(211, -211, "E. coli", 1),
                     (3122, -3122, "S. pneumoniae", 2)]

    # List of all valid bacterial IDs
    all_ids = []
    for wild_id, mutant_id, name in pairs:
        all_ids.append(wild_id)
        all_ids.append(mutant_id)

    # Store the average counts for each sub-sample
    averages = {}
    for bacteria_id in all_ids:
        averages[bacteria_id] = []

    # Store WT-mutant differences for each sub-sample
    differences = {}
    for wild_id, mutant_id, name in pairs:
        differences[wild_id] = []

    # Store momentum counts for each of the 10 files
    momentum_results = []

    total_valid_events = 0

    # PART 1: READ THE FILES

    for file in files:

        # Count bacteria in this file
        counts = {}
        for bacteria_id in all_ids:
            counts[bacteria_id] = 0

        # Create empty momentum histograms
        momentum_counts = {}
        for wild_id, mutant_id, name, bin_width in focus_species:
            number_of_bins = int(60 / bin_width)
            momentum_counts[wild_id] = np.zeros(number_of_bins)
            momentum_counts[mutant_id] = np.zeros(number_of_bins)

        valid_events = 0
        event_is_valid = False

        with open(file, "r") as infile:
            for line in infile:

                data = line.split()

                # Header: event number and number of bacteria
                if len(data) == 2:

                    # Count the previous event if it was valid
                    if event_is_valid:
                        valid_events += 1

                    event_is_valid = False
                    continue

                # Bacterial entry: px py pz ID
                if len(data) != 4:
                    continue

                bacteria_id = int(data[3])

                # Ignore IDs that are not in our list
                if bacteria_id not in counts:
                    continue

                counts[bacteria_id] += 1
                event_is_valid = True

                # Calculate momentum for our two focus species
                for wild_id, mutant_id, name, bin_width in focus_species:

                    if bacteria_id == wild_id or bacteria_id == mutant_id:

                        px = float(data[0])
                        py = float(data[1])
                        pz = float(data[2])

                        # Total momentum
                        momentum = np.sqrt(px**2 + py**2 + pz**2)

                        # Only use momentum from 0 to 60
                        if momentum < 60:
                            bin_number = int(momentum / bin_width)
                            momentum_counts[bacteria_id][bin_number] += 1

        # Count the final event
        if event_is_valid:
            valid_events += 1

        if valid_events == 0:
            raise ValueError("No valid events found in " + file)

        total_valid_events += valid_events

        # Average bacteria per valid event for this file
        for bacteria_id in all_ids:
            average = counts[bacteria_id] / valid_events
            averages[bacteria_id].append(average)

        # WT-mutant difference per valid event for this file
        for wild_id, mutant_id, name in pairs:
            difference = (counts[wild_id] - counts[mutant_id]) / valid_events
            differences[wild_id].append(difference)

        # Keep the momentum counts from this file
        momentum_results.append(momentum_counts)

        print(file, "processed:", valid_events, "valid events")

    print("\nTotal valid events:", total_valid_events)

    # PART 2: AVERAGE ABUNDANCE AND WT-MUTANT DIFFERENCE

    print("\nAVERAGE BACTERIA PER VALID EVENT")

    for wild_id, mutant_id, name in pairs:

        for bacteria_id in [wild_id, mutant_id]:

            mean = np.mean(averages[bacteria_id])
            uncertainty = np.std(averages[bacteria_id], ddof=1)

            print(f"{name} ({bacteria_id}): {mean:.6f} +/- {uncertainty:.6f}")

    print("\nWT - MUTANT DIFFERENCES")

    for wild_id, mutant_id, name in pairs:

        mean_difference = np.mean(differences[wild_id])
        uncertainty = np.std(differences[wild_id], ddof=1)

        print(f"{name}: {mean_difference:.6f} +/- {uncertainty:.6f}")

    # PART 3: ASYMMETRY AS A FUNCTION OF MOMENTUM

    # One graph for each of our two species
    for wild_id, mutant_id, name, bin_width in focus_species:

        number_of_bins = int(60 / bin_width)

        momenta = []
        mean_differences = []
        uncertainties = []

        for bin_number in range(number_of_bins):

            # Total WT and mutant counts across all 10 files
            n_wild = 0
            n_mutant = 0

            for momentum_counts in momentum_results:
                n_wild += momentum_counts[wild_id][bin_number]
                n_mutant += momentum_counts[mutant_id][bin_number]

            # Mean WT-mutant difference across 10 sub-samples
            difference = (n_wild - n_mutant) / 10

            # Poisson uncertainty
            # For a count N, the uncertainty is sqrt(N)
            # For WT-mutant, the variances are added
            # Divide by 10 because we plot the mean difference
            uncertainty = np.sqrt(n_wild + n_mutant) / 10

            # Centre of this momentum bin
            momentum = (bin_number + 0.5) * bin_width

            momenta.append(momentum)
            mean_differences.append(difference)
            uncertainties.append(uncertainty)

        
        # PLOT

        plt.figure(figsize=(11, 6))

        # Plot the mean differences with Poisson error bars
        plt.errorbar(momenta, mean_differences,
                     yerr=uncertainties,
                     fmt="o",
                     color="#6043A8",
                     ecolor="#B6A4DF",
                     markersize=5,
                     markeredgecolor="white",
                     markeredgewidth=0.6,
                     elinewidth=1.5,
                     capsize=3,
                     label="Mean WT - mutant difference")

        # Horizontal line at zero
        plt.axhline(0, color="#39445C",
                    linestyle="--", linewidth=1.5,
                    label="No difference (WT = mutant)")

        # Titles and axis labels
        plt.title(f"{name}\nWild-type vs mutant abundance by momentum",
                  fontsize=16, fontweight="bold",
                  color="#25243A", pad=18)

        plt.xlabel("Total momentum p (10⁻²⁰ kg·m/s)",
                   fontsize=12, labelpad=10)

        plt.ylabel("Mean WT - mutant count per sub-sample",
                   fontsize=12, labelpad=10)

        # Grid and background
        plt.grid(axis="y", alpha=0.15)
        plt.gca().set_axisbelow(True)
        plt.gca().set_facecolor("#FAF9FD")

        # Remove unnecessary borders
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)

        # Legend
        plt.legend(loc="upper right",
                   frameon=False, fontsize=10)

        plt.tight_layout()
        plt.savefig(f"{name.replace(' ', '_')}_momentum.png", dpi=300, bbox_inches="tight")
        plt.show()
  

bacteria_analysis()
