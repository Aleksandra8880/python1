print()
print(" 🧫 BACTERIAL COUNT CALCULATOR 🧫")
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
print("This program calculates the total momentum of each bacterium in the dataset.")
print()
input("Press enter to start...") 
print()
print("Instructions:")
print("1. Make sure you have downloaded output-Set0.txt.")
print("2. Place output-Set0.txt in the same folder as the downloaded Python file.")
print("3. Check your current working directory in the VS Code terminal.")
print()
print("Example:")
print("If your current working directory is 'msp' and both files are in a folder called 'PRA2003', the file path is: PRA2003/output-Set0.txt.")
print()

while True: # protection if the user enters a wrong file path 
    directory = input("Enter the path to output-Set0.txt. ")
    try:
        infile = open(directory, "r")
        break
    except FileNotFoundError:
        print("File not found. Please check the file path.")

def calculate_momentum(px, py, pz): # create a function that calculates and returns the total momentum
    ptotal = (px**2 + py**2 + pz**2) **0.5 # I thought of implementing a protection against a negative value under the root, but since everything is squared it's not possible for a value to be negative
    return ptotal
    
with open(directory, "r") as infile: # open and read the file
    next(infile) # skip the first line (header)

    for line_number, line in enumerate(infile, start=2): # introduce a for loop to check each line of the dataset (number the lines to potentially inform the user in which line there is an error)
        column = line.split() # split each data entry into momentum components and bacterial ID

        try: 
            px = float(column[0])
            py = float(column[1])
            pz = float(column[2])
        except (ValueError, IndexError): # protection against invalid/missing momentum components (try replacing a momentum value in the input file with "potato" or remove a value completely to see how this protection works)
            print("Line", str(line_number) + ":", "Invalid or incomplete momentum components. Bacterial specimen skipped.")
            continue

        try:
            bacterium = column[3]
        except IndexError: # protection against missing bacterial ID (protection against invalid bacterial ID implemented in the end of the code)
            print("Line", str(line_number) + ":", "Missing bacterial ID. Bacterial specimen skipped.")
            continue
 
        if bacterium == "211": # match IDs with the names of bacteria
            bacterium = "E. coli (wild type)"
        elif bacterium == "-211":
            bacterium = "E. coli (mutant)"
        elif bacterium == "321":
            bacterium = "B. subtilis (wild type)"
        elif bacterium == "-321":
            bacterium = "B. subtilis (mutant)"
        elif bacterium == "2212":
            bacterium = "P. aeruginosa (wild type)"
        elif bacterium == "-2212":
            bacterium = "P. aeruginosa (mutant)"
        elif bacterium == "3122":
            bacterium = "S. pneumoniae (wild type)"
        elif bacterium == "-3122":
            bacterium = "S. pneumoniae (mutant)"
        elif bacterium == "3312":
            bacterium = "M. tuberculosis (wild type)"
        elif bacterium == "-3312":
            bacterium = "M. tuberculosis (mutant)"
        elif bacterium == "3334":
            bacterium = "Salmonella (enteric)"
        elif bacterium == "-3334":
            bacterium = "Salmonella (mutant)"
        else: 
            print("Line", str(line_number) + ":", "Unknown ID. Bacterial specimen skipped.")
            continue # there are some uknown bacterial ID in the dataset that are excluded from analysis

        ptotal = calculate_momentum(px, py, pz) # for each bacterium calculate the total momentum using the function
        print(bacterium + ":", ptotal, "\u00d7 10\u207b\u00b2\u2070 kg m/s") # print the final result (used unicode for units and exponents)
