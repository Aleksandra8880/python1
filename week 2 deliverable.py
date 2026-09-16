# Function to calculate the total momentum
def calculate_momentum(px, py, pz):
    return (px**2 + py**2 + pz**2)**0.5
# **2 means squared and **0.5 takes the square root


# Open the input file
with open("output-Set0.txt", "r") as infile:

    # Read the event header
    header = infile.readline()
    header_values = header.split()
    # split the header into event ID and number of particles

# this converts the header values from text into whole numbers
    event_id = int(header_values[0])
    number_of_particles = int(header_values[1])

    print("Event ID:", event_id)
    print("Number of particles:", number_of_particles)

    # Read the particle data
    for line in infile:
        values = line.split()
        # split the line into px, py, pz, and code

# float is used because the momentum values can be decimal numbers
        px = float(values[0])
        py = float(values[1])
        pz = float(values[2])
# int is used because the code values are whole numbers
        code = int(values[3])

        momentum = calculate_momentum(px, py, pz)

        print("Code:", code, "Momentum:", momentum) 