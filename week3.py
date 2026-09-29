# Dictionary that matches bacterial ID with the bacterial strain
bacterial_strains = { 
    "211": "E. coli (wild type)",
    "-211": "E. coli (mutant)",
    "321": "B. subtilis (wild type)",
    "-321": "B. subtilis (mutant)",
    "2212": "P. aeruginosa (wild type)",
    "-2212": "P. aeruginosa (mutant)",
    "3122": "S. pneumoniae (wild type)",
    "-3122": "S. pneumoniae (mutant)",
    "3312": "M. tuberculosis (wild type)",
    "-3312": "M. tuberculosis (mutant)",
    "3334": "S. enterica (wild type)",
    "-3334": "S. enterica (mutant)"
}

# Function 1. "count" (returns total number of experiments AND total number of bacteria of each strain)
def count(filename):
    experiment_count = 0 # total number of valid experiments in the batch (start with 0)
    bacteria_count = {} # dictionary that matches bacteriall ID with the total count for that strain (start with empty)
    for bacterial_ID in bacterial_strains: # loop through each bacterial strain from the bacterial_strains dictionary
        bacteria_count[bacterial_ID] = 0 
    current_line = 0 # introduce a tracker for which line is being currently analyzed to help the user locate potential formatting errors in the dataset (this is different than "rows" because we don't care if that line has valid data)
    with open(filename, "r") as infile:
        for header in infile: # line 1 in the file is header and then the program jump to the next header by the number of rows
            current_line += 1 # update line tracker with each subsequent analyzed row
            try:   
                experiment_info = header.split() # the header includes two values that are named experiment_info
                rows = int(experiment_info[1]) # the second value is the number of bacteria in a given run, so essentially the number of rows that belong to this run
            except (IndexError, ValueError):
                raise ValueError(f"Invalid header at line {current_line}. Analysis stopped.")
            if rows < 0: # protection against a negative number of bacteria (potential formatting error in the dataset)
                raise ValueError(f"Invalid header at line {current_line}. Analysis stopped.")
            if rows >= 1: # skips empty experiments
                valid_experiment = False # definition of a valid experiment = experiment contains at least one bacterial specimen with an ID from the dictionary
                for _ in range(rows):  
                    row = next(infile) # go to the next row within the range defined by the number of rows (experiment_info[1] from the header)
                    current_line += 1 # update line tracker with each subsequent analyzed row
                    row_info = row.split() # to separate momentum components and bacterial ID in each line
                    bacterial_ID = row_info[3] # bacterial ID is the fourth value in the line so has index [3]
                    if bacterial_ID in bacterial_strains: # checking if the ID is listed in the dictionary
                        valid_experiment = True 
                        bacteria_count[bacterial_ID] += 1 # count this valid ID into the total bacteria count  
                if valid_experiment == True:
                    experiment_count += 1 # count this valid experiment into the total experiment count
    return bacteria_count, experiment_count
# weakness of this approach: the next headers are found based on the information about the number of bacteria (= number of rows) in each run; the whole program gets shifted if the header has wrong formatting or contains an error
# my other idea was to treat each line that has two values as a header; but then the weakness would be incorrectly formatted data entry (e.g. a line that only has the px momentum component and the ID) so no solution is ideal

# Function 2. "average" (returns the average count of each bacterial strain per experiment)
def average(bacteria_count, experiment_count):
    average_count = {}
    for bacterial_ID in bacteria_count:
        average_count[bacterial_ID] = bacteria_count[bacterial_ID] / experiment_count
    return average_count

# Function 3. "uncertainty" (returns the uncertainty for each average count)
def uncertainty(average_count):
    uncertainty_count = {}
    for bacterial_ID in average_count:
        uncertainty_count[bacterial_ID] = average_count[bacterial_ID]**0.5
    return uncertainty_count

# Instructions and user's input to locate the dataset
print()
print("🧮 BACTERIAL COUNT CALCULATOR 🧮")
print(r"""
       _______________________
    .-'                       '-.
  .'    o    .    o     .        '.
 /   .     o    .     o     .      \
|  o    .     o    .      o     .   |~~~~\____/~~~~\____/~~~~
 \    o    .      o    .      o     /
  '.     .    o      .     o      .'
    '-._________________________.-'

""") # bacterium ASCII art created with the help of AI 
print("This program finds the average count of each bacterial strain per experiment.")
print()
input("Press enter to start...") 
print()
print("Instructions:")
print("1. Make sure you have downloaded output-Set#.txt.")
print("2. Place output-Set#.txt in the same folder as the downloaded Python file.")
print("3. Check your current working directory in the VS Code terminal.")
print()
print("Example:")
print("If your current working directory is 'msp' and both files are in a folder called 'PRA2003', the file path is: PRA2003/output-Set#.txt.")
print()

while True: # protection if the user enters a wrong file path 
    directory = input("Enter the path to output-Set#.txt. ")
    try:
        infile = open(directory, "r")
        break
    except FileNotFoundError:
        print("File not found. Please check the file path.")

# Waiting message for the user while the analysis is running
print()
print("⏳ Analyzing the dataset... This may take a moment. ⏳")
print()

# Running the functions on the data from the file 
bacteria_count, experiment_count = count(directory)
average_count = average(bacteria_count, experiment_count)
uncertainty_count = uncertainty(average_count)

# Printing the final results
print()
print("📊 RESULTS 📊")
print("Total number of valid experiments:", experiment_count)
print()
for bacterial_ID in bacterial_strains:
    print(bacterial_strains[bacterial_ID], "Total count:", bacteria_count[bacterial_ID])
    print("Average count per experiment:", average_count[bacterial_ID], "+/-", uncertainty_count[bacterial_ID])
    print()
print()
