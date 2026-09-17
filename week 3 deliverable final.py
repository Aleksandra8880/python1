# Week 3 Deliverable - Bacteria Analysis
# Dataset 7

import math

print("\n==========================================")
print("          WEEK 3 BACTERIA ANALYSIS")
print("==========================================")

# Dictionary linking each bacterial ID to its name
# Only these bacterial IDs are included in the analysis
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

# Start the count for each bacterial ID at 0
bacteria_counts = {}

for bacteria_id in bacteria:
    bacteria_counts[bacteria_id] = 0


# Calculate the average and statistical uncertainty
def calculate_results(count, number_of_events):
    average = count / number_of_events
    uncertainty = math.sqrt(average)
    return average, uncertainty


# Variables used while reading the dataset
total_events = 0
relevant_events = 0
invalid_lines = 0

# Keeps track of whether the current event contain at least one bacterial ID from the dictionary
event_has_selected_bacteria = False


try:
    with open("output-Set7.txt", "r") as infile:

        for line in infile:
            values = line.split()

            # Ignore completely empty lines
            if len(values) == 0:
                continue

            # A line with 2 values is the start of a new event
            if len(values) == 2:

                try:
                    event_number = int(values[0])
                    number_of_entries = int(values[1])

                    # Number of entries should not be negative
                    if number_of_entries < 0:
                        raise ValueError

                    # Before starting the new event, check whether
                    # the previous event contained selected bacteria
                    if total_events > 0:
                        if event_has_selected_bacteria:
                            relevant_events += 1

                    # Count every event found in the dataset
                    total_events += 1

                    # Reset for the new event
                    event_has_selected_bacteria = False

                except ValueError:
                    invalid_lines += 1

            # A line with 4 values contains an entry from the event
            elif len(values) == 4:

                try:
                    bacteria_id = int(values[3])

                    # Only include IDs that are in our bacteria dictionary
                    if bacteria_id in bacteria_counts:
                        bacteria_counts[bacteria_id] += 1

                        # This event contains at least one bacterium
                        # that is relevant to our analysis
                        event_has_selected_bacteria = True

                except ValueError:
                    invalid_lines += 1

            # Any other number of values is unexpected
            else:
                invalid_lines += 1


        # The final event also needs to be checked because
        # there is no new event after it to trigger the check
        if total_events > 0:
            if event_has_selected_bacteria:
                relevant_events += 1


    # Only calculate results if relevant events were found
    if relevant_events > 0:

        print("\n==========================================")
        print("                  RESULTS")
        print("==========================================")

        print(f"\nTotal events found: {total_events}")
        print(f"Relevant events found: {relevant_events}")
        print(f"Events not included: {total_events - relevant_events}")
        print(f"Invalid lines found: {invalid_lines}")

        print("\n------------------------------------------")

        total_selected_bacteria = 0

        # Calculate results separately for each bacterial ID
        for bacteria_id in bacteria:

            count = bacteria_counts[bacteria_id]
            total_selected_bacteria += count

            average, uncertainty = calculate_results(
                count, relevant_events
            )

            print(f"\n{bacteria[bacteria_id]} (ID: {bacteria_id})")
            print(f"Total count: {count}")
            print(f"Average per relevant event: {average}")
            print(f"Statistical uncertainty: +/- {uncertainty}")


        # Calculate the combined average of all selected bacteria
        combined_average = total_selected_bacteria / relevant_events

        print("\n------------------------------------------")
        print("              OVERALL SUMMARY")
        print("------------------------------------------")

        print(f"Total selected bacteria: {total_selected_bacteria}")
        print(f"Combined average per relevant event: {combined_average}")

        print(
            "\nNote: Only events containing at least one bacterial ID "
            "from the dictionary are included in the averages."
        )

        print("\n==========================================")
        print("Analysis completed!")
        print("==========================================")


    else:
        print("\nError: No relevant bacterial events were found.")


except FileNotFoundError:
    print("\nError: output-Set7.txt could not be found.")
    print("Make sure the dataset and Python file are in the same folder.")