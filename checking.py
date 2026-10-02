#I needed a file to work on a smaller sample, because my laptop was overheating
from pathlib import Path
from statistics import stdev
import os 
from math import sqrt
import pandas as pd
from bisect import bisect_right

bins_sections = [0,5,10,15,20,40,60,80]

#creating the function calculate_momentum
def calculate_momentum(px,py,pz):
    total_momentum = (px**2 + py**2 + pz**2)**0.5
    return total_momentum

#python list of all the bacteria we are intersted in
bacteria_code = [211, -211, 321, -321, 2212, -2212, 3122, -3122, 3312,-3312, 3334,-3334]
mutant_wild_pairs = [(211,-211), (321,-321),(2212,-2212),(3122,-3122), (3312,-3312), (3334,-3334)]
rows = []

def mean_valuebacteria(file):
    events_count = 0
    bacteria_count = {p: 0 for p in bacteria_code}
    relevant_rows = 0
    averages = {p : 0 for p in bacteria_code}
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
                    total_momentum = calculate_momentum(px,py,pz)

                    bin_number = bisect_right(bins_sections,total_momentum)



                    rows.append({"ID" : bacteria_id ,
                        "momentum" : total_momentum,
                        "bin" : bin_number
                        #"sample" = sample_dict.key
                    })

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
            #averages collects p : average structures, when we read all files in "totalaverage_file" we colllect structures p : list of averages
            # in structure "averages_perfile" we store file : [list of averages of all p per one file]
            averages[p] = average
            #uncertainty = (average)**0.5
            #print(f"For {p} average bacteria per event : {average} +/- {uncertainty}")
            
    print(f"File{file} processed.") 
    #print(averages)       
    
    return events_count , averages 


files = ["output-Set1.txt","output-Set2.txt","output-Set3.txt"]
sample_dict = {1 : "output-Set1.txt",2:"output-Set2.txt",3:"output-Set3.txt", 4:"output-Set4.txt", 5:"output-Set5.txt",6:"output-Set6.txt",7:"output-Set7.txt",8:"output-Set8.txt",9:"output-Set9.txt",10:"output-Set10.txt"}


#the list of all events from all 10 files
events = []
#a dictionary with p as key an value: list with average count of certain ID per file
totalaverage_file = {p: [] for p in bacteria_code}


#list storing that for each file we have a certain average
averages_perfile ={}
#list storing events per file
weights = {file : 0  for file in files}
for file in files:
    try:
        
        event_count, averages = mean_valuebacteria(file)
        events.append(event_count)
        #for each file(dictionary key) the value is an averages dictionary from the function meanvalue_bacteria with the structure p: average(of individual file)
        averages_perfile[file] = averages
        weights[file] = event_count

        for p in bacteria_code:
            totalaverage_file[p].append(averages[p])

    except FileNotFoundError as e:
        print("File missing, file could not be found")
df = pd.DataFrame(rows, columns = ["ID","momentum", "bin"])
print(df.head())