
from pathlib import Path
from statistics import stdev
import os 
from math import sqrt

#python list of all the bacteria we are intersted in
bacteria_code = [211, -211, 321, -321, 2212, -2212, 3122, -3122, 3312,-3312, 3334,-3334]
mutant_wild_pairs = [(211,-211), (321,-321),(2212,-2212),(3122,-3122), (3312,-3312), (3334,-3334)]

 
def mean_valuebacteria(file):
    events_count = 0
    bacteria_count = {p: 0 for p in bacteria_code}
    relevant_rows = 0
    averages = {p : 0 for p in bacteria_code}
    with open ( file, "r") as file:
        # here we need to split the lines into lists, line numbering starts from 0
        for line_number, line in enumerate(file):
            
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
            
            
    return events_count , averages

files = ["output-Set1.txt","output-Set2.txt","output-Set3.txt","output-Set4.txt","output-Set5.txt","output-Set6.txt","output-Set7.txt","output-Set8.txt","output-Set9.txt","output-Set10.txt"]

#w = [os.path.getsize("output-Set1.txt"),os.path.getsize("output-Set2.txt"),os.path.getsize("output-Set3.txt"),os.path.getsize("output-Set4.txt"),os.path.getsize("output-Set5.txt"),os.path.getsize("output-Set6.txt"),os.path.getsize("output-Set7.txt"),os.path.getsize("output-Set8.txt"),os.path.getsize("output-Set9.txt"),os.path.getsize("output-Set10.txt")]
events = []
totalaverage_file = {p: [] for p in bacteria_code}
for file in files:
    try:
        
        event_count, averages = mean_valuebacteria(file)
        events.append(event_count)

        for p in bacteria_code:
            totalaverage_file[p].append(averages[p])

    except FileNotFoundError as e:
        print("File missing, file could not be found")


#initiating the dictionaries connecting p with overall averages and std
averages_normal = {p : 0 for p in bacteria_code}
std_normalwithp = {p : 0 for p in bacteria_code}

for p in bacteria_code:
    n1 = sum(totalaverage_file[p])
    #number of files used = sub-samples
    n2 = len(files)
    average_from_all_files = n1/n2
    #calculating standard deviation
    top = sum(averages[p]-average_from_all_files)
    bottom = len(files) - 1
    standard_deviation = sqrt(top/bottom)
    #connecting the results to the dictionary
    averages_normal[p] = average_from_all_files
    std_normalwithp[p] = standard_deviation

    print(f"For {p} the average from all files is {average_from_all_files} with standard deviation {standard_deviation}")




for i in mutant_wild_pairs:
    def mutant_wild_asymmetry():
        
        denominator = average_from_all_files[i[0]]+average_from_all_files[i[1]]
        numerator = average_from_all_files[i[0]]-average_from_all_files[i[1]]
        if not denominator == 0 :
            mutant_wild_asymmetry[i] = numerator/denominator
            print(f"Assymetry of pair {i} is {mutant_wild_asymmetry[i]}")
        else:
            print("The asymmetry cannot be determined. Denominator is zero. Re-check the input files and calculations. ")
        return mutant_wild_asymmetry

w = events_count = mean_valuebacteria(file)
aver = averages[p] = mean_valuebacteria(file)
averages_perfile = {file : aver for file in files}
weights = {file : w  for file in files}
weighted_average = {p : 0 for p in bacteria_code}
weighted_std = {p : 0 for p in bacteria_code}

def calculate_weighted_average(files):

    for p in bacteria_code:

        if not sum(w) == 0:

            weighted_average[p]= sum(weights[file]*averages_perfile[file])/sum(w)
            

            #weighted_std = sqrt(summation(weights* [mean from one file - total mean])/ [down] )
            #down = W - wi^2 / W


            mean_minus_weightedmean = weights[file]*(averages_perfile[file]-weighted_average[p])
            V = sum(mean_minus_weightedmean/D)
            W = sum(w)
            D = ( W**2 - weights[file]**2)/W



            weighted_std = (V )**0.5

        else:
            print("Incorrect weights, denominator cannot be zero.")
    return weighted_average[p] , weighted_std[p]



def weighted_vs_unweighted():

    for p in bacteria_code:   
        difference = calculate_weighted_average(w,averages[p]) - averages_normal[p]
        if difference == 0:
            print(f"Results between weighted and unweighted means are the same.")

        
        
    #dealing with their stdeviations sqrt(normal**2 - weighted**2)
        std_propagation = (std_normalwithp[p])**2  - weighted_std[p]
        sigma = sqrt(std_propagation)
        #let's check whether the difference in values is in 3sigma range
        if difference >= 3*sigma:
            print(f"There is a significant difference between the weighted mean and a regular one.")
        print("The difference between the weighted mean and unweighted one is insignificant. The number of events per file must be consistent.")

    


