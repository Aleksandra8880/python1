
#The code's user needs to download the file output-Set0.txt from the GitHub repository when dowloading the code itself and store it in the same folder

#code that reads one run and calculates the total momentum for all of the bacteria and returns the total momentum in the output file and prints in in the terminal with the communicates about the exceptions


#creating the function calculate_momentum
def calculate_momentum(px,py,pz):
    total_momentum = (px**2 + py**2 + pz**2)**0.5
    return total_momentum

# reading the file in python and storing the cleaned results in a newly created results file
def clean_data():
    with open("output-Set0.txt", "r") as infile:
        with open("result0.txt", "w") as outfile:
        # here we need to split the lines into lists, line numbering starts from 1, not Python's 0 default
            for line_number, line in enumerate(infile, start = 1):
                data = line.split()
            

            #checking if all lines have 4 values
                if len(data) != 4:
                    print(f"Skipping line {line_number}: {line.split()}")
                    continue # we print the communicate in the terminal and move on


            #change the data type(string -> float)
                px = float(data[0])
                py = float(data[1])
                pz = float(data[2])
                bacteria_id = int(data[3])

            #checking if the bacteria is from the available bacteria pull
            #create a list of values which bacteria id can take, the communicate about this problem is printed in the terminal
                bacteria_code = [211, -211, 321, -321, 2212, -2212, 3122, -3122, 3312,-3312, 3334,-3334]
                if bacteria_id not in bacteria_code:
                    print(f"Skipping line {line_number}: {line.split()}, bacteria outside of the investigated polulations.")
                    continue 
            


        # add a function to ensure px, py , pz are positive numbers or 0
                if px < 0:
                    px = -px
                if py < 0:
                    py = -py
                if pz < 0:
                    pz = -pz
                    
                #calling the function calculate_momentum
                total_momentum = calculate_momentum(px,py,pz)

            #store in the new file result0.txt the total momentum for each bacteria with the corresponding identification code
                outfile.write(f"BacteriaID: {bacteria_id}, Total momentum: {total_momentum} \n")

            #this prints what we calculated in the terminal, so it is after all the checking
                print(f"BacteriaID: {bacteria_id}, Total momentum: {total_momentum} \n")
                


clean_data()
