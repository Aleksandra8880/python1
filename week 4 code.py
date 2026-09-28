# Week 4 Deliverable - Bacteria Analysis
# Analyse the full sample using similarly sized sub-samples

import os
import statistics


bacteria = {
    211: "E. coli WT",
    -211: "E. coli mutant",
    321: "Bacillus subtilis WT",
    -321: "Bacillus subtilis mutant",
    2212: "Pseudomonas aeruginosa WT",
    -2212: "P. aeruginosa antibiotic-resistant",
    3122: "Streptococcus pneumoniae",
    -3122: "Capsule-deficient S. pneumoniae",
    3312: "Mycobacterium tuberculosis",
    -3312: "Drug-resistant M. tuberculosis",
    3334: "Salmonella enterica",
    -3334: "Salmonella mutant"
}


# Analyse one dataset file
def analyse_file(filepath):
    counts = {bacteria_id: 0 for bacteria_id in bacteria}
    total_events = 0
    invalid_lines = 0

    with open(filepath, "r") as infile:
        for line in infile:
            values = line.split()

            if len(values) == 0:
                continue

            # Event header
            if len(values) == 2:
                try:
                    event_number = int(values[0])
                    number_of_entries = int(values[1])

                    if number_of_entries < 0:
                        raise ValueError

                    total_events += 1

                except ValueError:
                    invalid_lines += 1

            # Bacterial entry
            elif len(values) == 4:
                try:
                    px = float(values[0])
                    py = float(values[1])
                    pz = float(values[2])
                    bacteria_id = int(values[3])

                    if bacteria_id in counts:
                        counts[bacteria_id] += 1

                except ValueError:
                    invalid_lines += 1

            else:
                invalid_lines += 1

    averages = {}

    if total_events > 0:
        for bacteria_id in bacteria:
            averages[bacteria_id] = counts[bacteria_id] / total_events

    return counts, averages, total_events, invalid_lines


print("\n==========================================")
print("          WEEK 4 BACTERIA ANALYSIS")
print("==========================================")

print("\nEnter the folder containing the output-Set .txt files.")
print("Enter . if the files are in the same folder as this program.")

folder = input("\nDataset folder: ").strip()


if folder == "":
    print("\nError: No folder was entered.")

elif not os.path.isdir(folder):
    print(f"\nError: The folder '{folder}' could not be found.")

else:
    # Find the dataset files automatically
    filenames = [
        filename for filename in os.listdir(folder)
        if filename.startswith("output-Set")
        and filename.endswith(".txt")
    ]

    # Sort by dataset number when possible
    try:
        filenames.sort(
            key=lambda name: int(
                name.replace("output-Set", "").replace(".txt", "")
            )
        )
    except ValueError:
        filenames.sort()

    if len(filenames) == 0:
        print("\nError: No output-Set .txt files were found.")

    else:
        print(f"\nDataset files found: {len(filenames)}")
        print("Starting analysis...")

        file_results = []

        # Analyse each file separately
        for filename in filenames:
            filepath = os.path.join(folder, filename)

            try:
                print(f"\nAnalysing {filename}...")

                counts, averages, events, invalid = analyse_file(filepath)

                file_results.append({
                    "filename": filename,
                    "counts": counts,
                    "averages": averages,
                    "events": events,
                    "invalid": invalid
                })

                print(f"Events found: {events}")
                print(f"Invalid lines: {invalid}")

            except FileNotFoundError:
                print(f"Error: {filename} could not be found.")

            except PermissionError:
                print(f"Error: Permission denied for {filename}.")


        if len(file_results) == 0:
            print("\nNo files could be analysed.")

        else:
            # Find the typical size of the sub-samples
            event_counts = [result["events"] for result in file_results]
            typical_events = statistics.median(event_counts)

            included = [
                result for result in file_results
                if result["events"] == typical_events
            ]

            excluded = [
                result for result in file_results
                if result["events"] != typical_events
            ]

            print("\n==========================================")
            print("            SUB-SAMPLE CHECK")
            print("==========================================")
            print(f"\nTypical sub-sample size: {typical_events:g} events")

            print("\nIncluded sub-samples:")
            for result in included:
                print(f"- {result['filename']}: {result['events']} events")

            if len(excluded) > 0:
                print("\nExcluded files:")
                for result in excluded:
                    print(f"- {result['filename']}: {result['events']} events")

                print("\nExcluded files do not match the typical sub-sample size.")


            # Combine results from the accepted sub-samples
            total_counts = {bacteria_id: 0 for bacteria_id in bacteria}
            subsample_averages = {
                bacteria_id: [] for bacteria_id in bacteria
            }

            total_events = 0
            total_invalid = 0

            for result in included:
                total_events += result["events"]
                total_invalid += result["invalid"]

                for bacteria_id in bacteria:
                    total_counts[bacteria_id] += result["counts"][bacteria_id]
                    subsample_averages[bacteria_id].append(
                        result["averages"][bacteria_id]
                    )


            if len(included) > 0 and total_events > 0:
                print("\n==========================================")
                print("               FINAL RESULTS")
                print("==========================================")

                print(f"\nSub-samples analysed: {len(included)}")
                print(f"Total events analysed: {total_events}")
                print(f"Total invalid lines: {total_invalid}")
                print("\n------------------------------------------")

                total_selected = 0

                # Calculate results for each bacterial strain
                for bacteria_id in bacteria:
                    count = total_counts[bacteria_id]
                    total_selected += count

                    average = count / total_events

                    if len(subsample_averages[bacteria_id]) > 1:
                        uncertainty = statistics.stdev(
                            subsample_averages[bacteria_id]
                        )
                    else:
                        uncertainty = None

                    print(f"\n{bacteria[bacteria_id]} (ID: {bacteria_id})")
                    print(f"Total count: {count}")
                    print(f"Average per event: {average}")

                    if uncertainty is not None:
                        print(f"Statistical uncertainty: +/- {uncertainty}")
                    else:
                        print("Statistical uncertainty: Cannot calculate")


                # Compare each normal strain with its mutant
                print("\n==========================================")
                print("        NORMAL VS MUTANT COMPARISON")
                print("==========================================")

                pairs = [
                    bacteria_id for bacteria_id in bacteria
                    if bacteria_id > 0 and -bacteria_id in bacteria
                ]

                for normal_id in pairs:
                    mutant_id = -normal_id

                    differences = []

                    for result in included:
                        difference = (
                            result["averages"][normal_id]
                            - result["averages"][mutant_id]
                        )
                        differences.append(difference)

                    # Difference over the full 5-million-event sample
                    mean_difference = (
                        total_counts[normal_id]
                        - total_counts[mutant_id]
                    ) / total_events

                    if len(differences) > 1:
                        difference_uncertainty = statistics.stdev(differences)
                    else:
                        difference_uncertainty = None

                    print(
                        f"\n{bacteria[normal_id]} vs "
                        f"{bacteria[mutant_id]}"
                    )
                    print(f"Mean difference per event: {mean_difference}")

                    if difference_uncertainty is not None:
                        print(
                            f"Statistical uncertainty of difference: "
                            f"+/- {difference_uncertainty}"
                        )
                    else:
                        print(
                            "Statistical uncertainty of difference: "
                            "Cannot calculate"
                        )


                print("\n------------------------------------------")
                print("              OVERALL SUMMARY")
                print("------------------------------------------")
                print(f"Total selected bacteria: {total_selected}")
                print(f"Total events analysed: {total_events}")
                print(f"Sub-samples analysed: {len(included)}")

                print("\nThe statistical uncertainty is the standard deviation")
                print("of the results from the included sub-samples.")

                print("\n==========================================")
                print("Analysis completed!")
                print("==========================================")

            else:
                print("\nNo suitable sub-samples were available.")
            