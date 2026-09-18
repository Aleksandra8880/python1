# Week 3 - Bacteria Analysis
# Dataset 7

# This program analyses 12 bacterial strains from Dataset 7.
# The output shows the average per event and its statistical uncertainty.

# Import the math module
import math


# create a dictionary that links each bacterial ID to its name
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


# Create a dictionary to store the count of each bacterial strain
counts = {}

# Go through every bacterial ID in the bacteria dictionary, start count at zero
for bacteria_id in bacteria:
    counts[bacteria_id] = 0


# Open Dataset 7, in reading mode "r"
file = open("output-Set7.txt", "r")


# Start a count of valid events, events that contain zero entries and entries of unknown ids
number_events = 0
zero_events = 0
unknown_ids = 0



# Keep reading until the end of the file
while True:

    # Read an event header
    header = file.readline()

    # Stop when there is nothing left to read
    if not header:
        break

    # Separate the two values in the event header
    event_data = header.split()

    # First value = event number
    event_number = int(event_data[0])

    # Second value = number of bacteria in this event
    number_bacteria = int(event_data[1])

    # Check if this event has zero bacteria, if so count it as a zero event
    if number_bacteria == 0:
        zero_events += 1

  

    # Keep track of whether this event contains one of the bacteria were considering
    valid_event = False

# Repeat for every bacterium belonging to this event
    for i in range(number_bacteria):

        # Read one bacteria entry
        line = file.readline()

        # split the line of code into  px, py, pz and bacterial ID
        data = line.split()

        # The last value (3) is the bacterial ID
        # data[0] = px, data[1] = py, data[2] = pz, data[3] = bacterial ID.
        bacteria_id = int(data[3])

        # Count the bacterium if its ID is in our dictionary, if so add 1 to the count of bacterial strains
        if bacteria_id in counts:
          counts[bacteria_id] += 1
          valid_event = True
        else:
        # If the ID is not in our dictionary, count it separately.
            unknown_ids += 1
    # After reading the whole event, add it to count only if it contain one of the 12 considered IDs
    if valid_event:
        number_events += 1

# Close the dataset
file.close()


print("\nBACTERIA ANALYSIS - DATASET 7")
print("----------------------------------------")
print("This analysis counts 12 selected bacterial strains.")
# Show the total number of events analysed
print("Total number of events:", number_events)
print("Events with 0 bacteria:", zero_events)
print("Entries with IDs not in dictionary:", unknown_ids)
print("RESULTS")
print("----------------------------------------")


# Calculate the results for each bacterial ID
for bacteria_id in bacteria:

    # Total number of this bacterial strain
    count = counts[bacteria_id]

    # Average number of this bacterial strain per valid event
    average = count / number_events

    # Statistical uncertainty
    uncertainty = math.sqrt(average)

    # Print the strain name and its results in a readable format.
    print("Bacterial strain:", bacteria[bacteria_id])
    print("Total count:", count)
    print("Average per valid event:", average)
    print("Statistical uncertainty: +/-", uncertainty)
    print()
    
