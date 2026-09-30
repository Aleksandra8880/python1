# Week 4 - Bacteria Analysis

# Datasets

# This program analyses 12 bacterial strains from Dataset 7.

# The output shows the average number of each bacterial strain per valid event
# and its statistical uncertainty using the sub-sampling method.

import statistics
import os


# Create a dictionary that links each bacterial ID to its name
bacteria = {
    211: "E. coli (wild type)",
    -211: "E. coli (mutant)",
    321: "B. subtilis (wild type)",
    -321: "B. subtilis (mutant)",
    2212: "P. aeruginosa (wild type)",
    -2212: "P. aeruginosa (mutant)",
    3122: "S. pneumoniae (wild type)",
    -3122: "S. pneumoniae (mutant)",
    3312: "M. tuberculosis (wild type)",
    -3312: "M. tuberculosis (mutant)",
    3334: "S. enterica (wild type)",
    -3334: "S. enterica (mutant)"
}


# Create a dictionary that links each wild type ID to its mutant ID
pairs = {
    211: -211,
    321: -321,
    2212: -2212,
    3122: -3122,
    3312: -3312,
    3334: -3334
}


# Name of the folder containing the datasets
data_folder = "data"


# Create a list to store the dataset files
files = []


# Protection to check if the data folder exists
if not os.path.isdir(data_folder):
    print("Data folder was not found.")
    exit()


# Go through the files in the data folder
for filename in os.listdir(data_folder):

    # Check if the file is one of the datasets
    if filename.startswith("output-Set") and filename.endswith(".txt"):
        files.append(filename)


# Put the files in order
files.sort()


# Protection: check if any dataset files were found
if len(files) == 0:
    print("No dataset files were found.")
    exit()


# Create a list to store the results from each dataset
file_results = []


# Go through every dataset
for filename in files:

    # Show the progress of the analysis in the terminal
    print("Analysing:", filename)


    # Create a dictionary to store the count of each bacterial strain
    counts = {}


    # Go through every bacterial ID and start the count at zero
    for bacteria_id in bacteria:
        counts[bacteria_id] = 0


    # Start a count of all events, valid events, zero events and unknown IDs
    total_events = 0
    number_events = 0
    zero_events = 0
    unknown_ids = 0


    # Find the dataset file inside the data folder
    filepath = os.path.join(data_folder, filename)


    # Protection to check if the file exists
    if not os.path.exists(filepath):
        print("File not found:", filename)
        continue


    # Open the dataset in reading mode
    file = open(filepath, "r")


    # Keep reading until the end of the file
    while True:

        # Read an event header
        header = file.readline()


        # Stop when there is nothing left to read
        if not header:
            break


        # Separate the two values in the event header
        event_data = header.split()


        # Protection to check that the event header contains two values
        if len(event_data) < 2:
            print("Invalid event header.")
            continue


        # Protection against values that cannot be converted to numbers
        try:

            # First value = event number
            event_number = int(event_data[0])

            # Second value = number of bacteria in this event
            number_bacteria = int(event_data[1])
  except ValueError:
            print("Invalid event header.")
            continue


        # Count the event
        total_events += 1


        # Check if this event has zero bacteria
        if number_bacteria == 0:
            zero_events += 1


        # Keep track of whether this event contains one of the bacteria
        # we are considering
        valid_event = False


        # Repeat for every bacterium belonging to this event
        for i in range(number_bacteria):

            # Read one bacteria entry
            line = file.readline()


            # Protection in case the file ends unexpectedly
            if not line:
                break


            # Split the line into px, py, pz and bacterial ID
            data = line.split()


            # Protection to check that the line contains all four values
            if len(data) < 4:
                continue


            # Protection to check that the bacterial ID is a number
            try:

                # data[0] = px
                # data[1] = py
                # data[2] = pz
                # data[3] = bacterial ID
                bacteria_id = int(data[3])

            except ValueError:
                continue


            # Count the bacterium if its ID is in our dictionary
            if bacteria_id in counts:

                counts[bacteria_id] += 1
                valid_event = True

            else:

                # If the ID is not in our dictionary, count it separately
                unknown_ids += 1


        # Add the event only if it contains one of the 12 considered IDs
        if valid_event:
            number_events += 1


    # Close the dataset
    file.close()


    # Protection to check that there are valid events
    if number_events == 0:
        print("No valid events found in:", filename)
        continue


    # Create a dictionary to store the average of each bacterial strain
    averages = {}


    # Calculate the average for each bacterial ID
    for bacteria_id in bacteria:

        # Total number of this bacterial strain
        count = counts[bacteria_id]

        # Average number of this bacterial strain per valid event
        average = count / number_events

        # Save the average
        averages[bacteria_id] = average


    # Save the results from this dataset
    file_results.append({
        "filename": filename,
        "total_events": total_events,
        "valid_events": number_events,
        "counts": counts,
        "averages": averages
    })


    # Show the data analysis progression in the terminal
    print("Total events:", total_events)
    print("Valid events:", number_events)
    print("Events with 0 bacteria:", zero_events)
    print("Entries with IDs not in dictionary:", unknown_ids)
    print()


# Protection to check that some datasets were analysed
if len(file_results) == 0:
    print("No datasets could be analysed.")
    exit()


# Find the typical number of events in the datasets
event_counts = []

for result in file_results:
    event_counts.append(result["total_events"])


typical_events = statistics.median(event_counts)


# Create a list for the datasets that have the typical number of events
included_results = []


# Check which datasets have the correct number of events
for result in file_results:

    if result["total_events"] == typical_events:
        included_results.append(result)

    else:
        print(
            "Excluded:",
            result["filename"],
            "- number of events:",
            result["total_events"]
        )


# Protection to check that at least two subsamples can be used
if len(included_results) < 2:
    print("Not enough subsamples to calculate statistical uncertainty.")
    exit()


# ------------------------------------------------------------
# Combine the results from all included subsamples
# ------------------------------------------------------------

# Create a dictionary to store the total count of each bacterial strain
total_counts = {}

for bacteria_id in bacteria:
    total_counts[bacteria_id] = 0


# Start the total number of events and valid events at zero
total_events_all = 0
total_valid_events = 0


# Go through all included subsamples
for result in included_results:

    # Add the number of events
    total_events_all += result["total_events"]

    # Add the number of valid events
    total_valid_events += result["valid_events"]


    # Add the bacterial counts from this subsample
    for bacteria_id in bacteria:
        total_counts[bacteria_id] += result["counts"][bacteria_id]


# ------------------------------------------------------------
# Final results for each bacterial strain
# ------------------------------------------------------------


print("BACTERIA ANALYSIS - DATASET 7")
print("Number of subsamples analysed:", len(included_results))
print("Events per subsample:", typical_events)
print("Total events analysed:", total_events_all)
print("Total valid events:", total_valid_events)


print("FINAL RESULTS")



# Calculate the final result for each bacterial strain
for bacteria_id in bacteria:

    # Create a list to store the average from each subsample
    subsample_averages = []


    # Get the average from each subsample
    for result in included_results:
        subsample_averages.append(
            result["averages"][bacteria_id]
        )


    # Total number of this bacterial strain in the entire sample
    total_count = total_counts[bacteria_id]


    # Calculate the average using the entire sample
    final_average = total_count / total_valid_events


    # Calculate the statistical uncertainty using the sub-sampling method
    uncertainty = statistics.stdev(subsample_averages)


    # Print the result
    print()
    print("Bacterial strain:", bacteria[bacteria_id])
    print("Total count:", total_count)
    print("Average per valid event:", final_average)
    print("Statistical uncertainty: +/-", uncertainty)


# ------------------------------------------------------------
# Wild type and mutant comparison
# ------------------------------------------------------------

print()
print("WILD TYPE VS MUTANT COMPARISON")



# Calculate the results for each wild type and mutant pair
for wild_type_id in pairs:

    # Get the mutant ID belonging to this wild type
    mutant_id = pairs[wild_type_id]


    # Create a list to store the differences from each subsample
    differences = []


    # Go through every included subsample
    for result in included_results:

        # Get the wild type average for this subsample
        wild_type_average = result["averages"][wild_type_id]

        # Get the mutant average for this subsample
        mutant_average = result["averages"][mutant_id]

        # Calculate wild type minus mutant for this subsample
        difference = wild_type_average - mutant_average

        # Save the difference
        differences.append(difference)


    # Calculate the mean difference using the entire sample
    mean_difference = (
        total_counts[wild_type_id]
        - total_counts[mutant_id]
    ) / total_valid_events


    # Calculate the statistical uncertainty using the sub-sampling method
    uncertainty = statistics.stdev(differences)


    # Print the results
    print()
    print(
        "Bacterial strains:",
        bacteria[wild_type_id],
        "vs",
        bacteria[mutant_id]
    )

    print("Mean difference per valid event:", mean_difference)
    print("Statistical uncertainty: +/-", uncertainty)


# ------------------------------------------------------------
# Overall summary
# ------------------------------------------------------------

print()
print("OVERALL SUMMARY")


print("Total events analysed:", total_events_all)
print("Total valid events:", total_valid_events)
print("Number of subsamples analysed:", len(included_results))

print()
print(
    "The statistical uncertainty is the standard deviation of the results from the included subsamples."
)
