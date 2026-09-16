import math

def calculate_momentum(px, py, pz):
    momentum = math.sqrt(px**2 + py**2 + pz**2)
    return momentum
# Open the file containing the bacterial data
file = open("output-Set0.txt", "r")

# Read the first line
header = file.readline()

# Split the first line into separate values
event_data = header.split()

# First number = event ID
event_id = int(event_data[0])

# Second number = number of bacteria in this event
number_bacteria = int(event_data[1])

print("Event:", event_id)
print("Number of bacteria:", number_bacteria)
# Go through each bacterium
for i in range(number_bacteria):

    # Read
    line = file.readline()
    data = line.split()

    #  momentum components and bacterial ID
    px = float(data[0])
    py = float(data[1])
    pz = float(data[2])
    bacteria_id = int(data[3])

    # momentum calculation
    momentum = calculate_momentum(px, py, pz)

    # Print the result
    print("Bacterium:", i + 1,
          "ID:", bacteria_id,
          "Momentum:", momentum)

file.close()