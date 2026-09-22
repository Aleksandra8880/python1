
from pathlib import Path

#python list of all the bacteria we are intersted in
bacteria_code = [211, -211, 321, -321, 2212, -2212, 3122, -3122, 3312,-3312, 3334,-3334]


#taking an imput from the user, after right-clicking the file in VS you can choose "copy path" of the file
file = Path(input("Enter the path of your file: "))
if not file.exists():
    raise ValueError("File not found, check whether the full directory was entered. ")
with open(file , "r") as infile:
    print("File found, the calculations will be performed.")

def mean_valuebacteria():
    events_count = 0
    bacteria_count = {p: 0 for p in bacteria_code}
    relevant_rows = 0
    with open ( file, "r") as infile:
        # here we need to split the lines into lists, line numbering starts from 0
        for line_number, line in enumerate(infile):
            
            data = line.split()

            #checking the how many valid events we have  
            #zeroes out the count of sub-variable relevant_rows whenever a new header is reached - > in in next lines bacteria is found, event_count will be increased
            if len(data) == 2:
                relevant_rows = 0 
                continue
                 

            try:
                #we check whether any non-useful lines are there
                if len(data) != 4:
                    raise ValueError(f"This row is not a header, but is also does not have 4 entries: {line}. It should be checked.")

                #connecting each element of the row = line, with the corresponding physical quantity, we are now sure len(data) == 4, so no index error should occur
                px = float(data[0])
                py = float(data[1])
                pz = float(data[2])
                bacteria_id = int(data[3])

                #checking if the row has data about our bacteria of interest
                if bacteria_id in bacteria_code:
                    bacteria_count[bacteria_id] += 1
                    relevant_rows += 1

                    # we still inside the loop that checks the data between the headers. 
                    # The relevant_rows increases each time the bacteria is found, but we only care if one bacteria is found and count that part as a valid event
                    #Therefore this part of the code ensures increasing the event_count max only once per investigated chunck
                    if relevant_rows == 1:
                        events_count += 1

            #error handling, we would like to know if something is wrong with our data            
            except ValueError as error:
                print(f"Skipping invalid line{line},  {error}")
                continue
            

        # each p is a "key" in the bacteria_count dictionary, its value is the count strating at zero. p is taken from the bacteria_code python list
        for p in bacteria_count:
            number_of_bacteria = bacteria_count[p] 
            average = number_of_bacteria / events_count
            uncertainty = (average)**0.5
            print(f"For {p} average bacteria per event : {average} +/- {uncertainty}")

mean_valuebacteria()