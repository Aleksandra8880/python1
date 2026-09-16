# Week 3 Deliverable - Bacteria Analysis
# Dataset 7

import math

print("\n==========================================")
print("          WEEK 3 BACTERIA ANALYSIS")
print("==========================================")

# Dictionary linking each bacterial ID to its name
# This keeps the IDs together and makes it easier to loop through them later
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

# Make another dictionary to keep track of the counts
bacteria_counts = {}

# Go through each ID and start its count at 0
for bacteria_id in bacteria:
    bacteria_counts[bacteria_id] = 0


# Function to calculate the average and uncertainty
# Using a function means the same calculation can be reused for every bacterial ID
def calculate_results(count, number_of_events):

    # Average = total bacteria divided by the total events found
    average = count / number_of_events

    # For counting data the uncertainty is based on the square root of the count
    uncertainty = math.sqrt(count) / number_of_events

    # Return sends both results back to where the function was called
    return average, uncertainty


# Start these counters at 0 before reading the dataset
number_of_events = 0
invalid_lines = 0
entry_mismatches = 0

# Keep track of how many entries should be in an event
number_of_entries = 0
entries_found = 0


try:
    # Open dataset 7 in read mode
    # infile is used because we are reading information from the file
    with open("output-Set7.txt", "r") as infile:

        # Read through the dataset one line at a time
        for line in infile:

            # Split the current line into its separate values
            values = line.split()

            # Skip any empty lines
            if len(values) == 0:
                continue


            # Event headers have 2 values
            if len(values) == 2:

                # Before starting a new event, check the previous one
                if number_of_events > 0:
                    if entries_found != number_of_entries:
                        entry_mismatches += 1

                try:
                    # First value is the event number
                    event_number = int(values[0])

                    # Second value tells us how many entries are in that event
                    number_of_entries = int(values[1])

                    # The number of entries should not be negative
                    if number_of_entries < 0:
                        raise ValueError

                    # Count the events instead of assuming there are exactly 500,000
                    number_of_events += 1

                    # Reset the entry counter for the new event
                    entries_found = 0

                except ValueError:
                    # Count the header as invalid if its values do not make sense
                    invalid_lines += 1


            # Bacteria entries have 4 values
            elif len(values) == 4:

                try:
                    # Count each entry in the current event
                    entries_found += 1

                    # The last value of each bacteria line is its ID
                    bacteria_id = int(values[3])

                    # Only count the bacterial IDs we are interested in
                    if bacteria_id in bacteria_counts:
                        bacteria_counts[bacteria_id] += 1

                except ValueError:
                    # Count the line as invalid if the ID is not an integer
                    invalid_lines += 1


            else:
                # Lines that don't match the expected structure are counted as invalid
                invalid_lines += 1


        # Check the number of entries in the final event
        if number_of_events > 0:
            if entries_found != number_of_entries:
                entry_mismatches += 1


    # Only continue with the maths if at least one event was found
    # This also avoids trying to divide by 0
    if number_of_events > 0:

        print("\n==========================================")
        print("                  RESULTS")
        print("==========================================")

        # Show the checks made while reading the dataset
        print(f"\nTotal events found: {number_of_events}")
        print(f"Invalid lines found: {invalid_lines}")
        print(f"Events with entry count mismatch: {entry_mismatches}")

        print("\n------------------------------------------")

        # Start a total for all the bacteria we are analysing
        total_selected_bacteria = 0

        # Loop through all bacterial IDs to calculate each result
        for bacteria_id in bacteria:

            # Get the total count for the current bacterial ID
            count = bacteria_counts[bacteria_id]

            # Add the current count to the total of all selected bacteria
            total_selected_bacteria += count

            # Use the function to calculate both results
            average, uncertainty = calculate_results(
                count, number_of_events
            )

            # Print the results for the current bacterium
            print(f"\n{bacteria[bacteria_id]} (ID: {bacteria_id})")
            print(f"Total count: {count}")
            print(f"Average per event: {average:.4f}")
            print(f"Statistical uncertainty: +/- {uncertainty:.6f}")


        # Calculate the average for all selected bacteria together
        combined_average = total_selected_bacteria / number_of_events

        print("\n------------------------------------------")
        print("              OVERALL SUMMARY")
        print("------------------------------------------")
        print(f"Total selected bacteria: {total_selected_bacteria}")
        print(f"Combined average per event: {combined_average:.4f}")

        # Explain what the overall total represents
        print(
            "\nNote: This total only includes the 12 bacterial IDs "
            "selected for this analysis."
        )
        print(
            "Other IDs are present in the dataset, but they are not included because they are not bacteria of interest.")

        print("\n==========================================")
        print("Analysis completed!")
        print("==========================================")


    else:
        # Avoid dividing by 0 if no events were found
        print("\nError: No events were found in the dataset.")


# Give a clear error if Python cannot find the dataset
except FileNotFoundError:
    print("\nError: output-Set7.txt could not be found.")
    print("Make sure the dataset and Python file are in the same folder.")
