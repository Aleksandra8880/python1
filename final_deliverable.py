""" 
INSTRUCTIONS
Analyse all sub-samples, separately
• Calculate the mean bacteria/molecule/particle asymmetry and its
statistical uncertainty
- Is the asymmetry per species significant?
• Perform a differential analysis as a function of momentum
- Calculate the mean difference between the relevant bacteria/molecules/
particles of interest as a function of P
- Assign statistical uncertainty for the mean difference between the relevant
bacteria/molecules/particles of interest as a function of P bin from the spread
of the results of all sub-samples

"""
"""
DATA FRAME
    ID  Momentum    BIN     file number
1   211 
2
3
...

"""




from pathlib import Path
from statistics import stdev
import os 
from math import sqrt
import pandas as pd

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
                    rows.append({"ID" : bacteria_id ,
                        "momentum" : total_momentum
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


files = ["output-Set1.txt","output-Set2.txt","output-Set3.txt", "output-Set4.txt", "output-Set5.txt","output-Set6.txt","output-Set7.txt","output-Set8.txt","output-Set9.txt","output-Set10.txt"]
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
df = pd.DataFrame(rows, columns = ["ID","momentum"])
print(df.head())
""""

#initiating the dictionaries connecting p with overall averages and std
averages_normal = {p : 0 for p in bacteria_code}
"""
"""
averages_normal {211: 19.96404222526273, -211: 19.931721898491062, 321: 2.5109760539147103, -321: 2.505280866934113,
 2212: 1.2089141646344372, 
-2212: 1.1850237360153653, 3122: 0.276800090574915, -3122: 0.2718939099983327, 3312: 0.039469937734426135, 
-3312: 0.03902893521802833, 3334: 0.001187962955206821, -3334: 0.0011524239744295493}
"""
"""
std_normalwithp = {p : 0 for p in bacteria_code}


for p in bacteria_code:
    #reminder: "totalaverage_file" collects list of average for each bacteria ID
    n1 = sum(totalaverage_file[p])
    #number of files used = sub-samples
    n2 = len(files)
    average_from_all_files = n1/n2
    #after calculating the average per 10 files we want to store it within the dictionary "averages_normal", where the average is the value
    averages_normal[p] = average_from_all_files
    #when calculating the summation we need to access averages of each separate run for each ID, we use "totalaverage_file" again
    top = 0
    for value in totalaverage_file[p]:
        top += (value - averages_normal[p])**2 
    
    bottom = len(files) - 1
    #calculating standard deviation
    standard_deviation = sqrt(top/bottom)

    #connecting the results to the dictionary
    std_normalwithp[p] = standard_deviation

    print(f"For {p} the average from all files is {average_from_all_files} with standard deviation {standard_deviation}")


weighted_average = {p : 0 for p in bacteria_code}
weighted_std = {p : 0 for p in bacteria_code}


def calculate_weighted_average(files):
    

    for p in bacteria_code:
        #sums all the values from the weights dictionary; our denominator
        W = sum(weights.values())


        if not W == 0:

            xw = 0 
            for file in files:
                #weighted_average[p]= sum(weights[file]*averages_perfile[file])/W 
                xw += weights[file]*averages_perfile[file][p]
            
            weighted_average[p] = xw / W          

            #weighted_std = sqrt(summation(weights* [mean from one file - total mean]^2)/ [down] )
            #down = W - wi^2 / W
            t = 0
            w_2 = 0
            for file in files:
                mean_minus_weightedmean = weights[file]*(averages_perfile[file][p]-weighted_average[p])**2
                t += mean_minus_weightedmean 
                w_2 += weights[file]**2
            D = (W**2 - w_2)/W
            if D > 0:
                V = t/D
                weighted_std[p] = (V )**0.5
            else:
                weighted_std[p] = None

        else:
            print("Incorrect weights, denominator cannot be zero.")
    
        print(f"For {p} weighted average is {weighted_average[p]} with weighted standard deviation: {weighted_std[p]}.\n")
    return weighted_average[p] , weighted_std[p]
calculate_weighted_average(files)


def weighted_vs_unweighted():

    for p in bacteria_code:   
        difference = weighted_average[p] - averages_normal[p]
        if difference == 0:
            print(f"Results between weighted and unweighted means are the same.")

        
        
    #dealing with their stdeviations sqrt(normal**2 - weighted**2)
        std_propagation = (std_normalwithp[p])**2  - (weighted_std[p])**2
        if std_propagation <0:
            std_propagation = -std_propagation
            sigma = sqrt(std_propagation)
        else:
            sigma = sqrt(std_propagation)
        #let's check whether the difference in values is in 3sigma range
        if difference >= 3*sigma:
            print(f"{p}There is a significant difference between the weighted mean and a regular one.")
        print(f"{p}The difference between the weighted mean and unweighted one is insignificant. The number of events per file are consistent.")
weighted_vs_unweighted()

i_asymmetry = {i  : 0 for i in mutant_wild_pairs}
def mutant_vs_wild_asymmetry():
        
    for i in mutant_wild_pairs:
        denominator = averages_normal[i[0]]+averages_normal[i[1]]
        numerator = averages_normal[i[0]]-averages_normal[i[1]]
        if not denominator == 0 :
            mutant_wild_asymmetry = numerator/denominator
            i_asymmetry[i] = mutant_wild_asymmetry
            print(f"Assymetry of pair {i} is {i_asymmetry[i]}")
        else:
            print("The asymmetry cannot be determined. Denominator is zero. Re-check the input files and calculations. ")
    return mutant_wild_asymmetry
mutant_vs_wild_asymmetry()

#checking whether the assymetry is significant. From all ten files calcualte delta(mean_N211 - mean_N-211). Calcuate the standard deviation of those - this is the uncertainty of the main result

"""
""" Perform a differential analysis as a function of momentum
- Calculate the mean difference between the relevant bacteria/molecules/
particles of interest as a function of P
- Assign statistical uncertainty for the mean difference between the relevant
bacteria/molecules/particles of interest as a function of P bin from the spread
of the results of all sub-samples
"""




"""""
print(f"weights {weights}")
print(f"totalaverage_file {totalaverage_file}") 
print(f"averages_normal {averages_normal}") 
print(f"std_normalwithp {std_normalwithp}") 
print(f"weighted average {weighted_average}") 
print(f"weighted std {weighted_std}") 
print(f"I_asymmetry {i_asymmetry}")
"""         
""""
weights {'output-Set1.txt': 461368, 'output-Set2.txt': 461516, 'output-Set3.txt': 461343, 'output-Set4.txt': 461322, 'output-Set5.txt': 461498, 'output-Set6.txt': 461668, 'output-Set7.txt': 461532, 'output-Set8.txt': 461543, 'output-Set9.txt': 461513, 'output-Set10.txt': 461329}

std_normalwithp {211: 0.03277297367603035, -211: 0.031862995623137325, 321: 0.004760470013110587, -321: 0.005510374977956562, 2212: 0.0019158652790257896, -2212: 0.002419119037614167, 3122: 0.0010762078233972018, -3122: 0.0009852549484234705, 3312: 0.0002835326780196851, -3312: 0.00040171753717196235, 3334: 4.1700896418102735e-05, -3334: 5.083297255816441e-05}

weighted average {211: 19.964037869108523, -211: 19.93171763208854, 321: 2.5109753063732927, -321: 2.505280161018257, 2212: 1.2089139502348183, -2212: 1.1850234211525426, 3122: 0.2767999701818043, -3122: 0.27189383682165774, 3312: 0.03946988622278006, -3312: 0.03902889764557607, 3334: 0.0011879603834065208, -3334: 0.0011524212548259536}

weighted std {211: 0.0327720070641392, -211: 0.03186181249654672, 321: 0.00476017143083106, -321: 0.005510077983665912, 2212: 0.001915752247257024, -2212: 0.0024191180818885333, 3122: 0.0010762047195403772, -3122: 0.0009852467879904842, 3312: 0.00028354309004001476, -3312: 0.00040170944387888757, 3334: 4.169983580006227e-05, -3334: 5.0834194233980064e-05}

I_asymmetry {(211, -211): 0.0008101192565559722, (321, -321): 0.0011353459502695781, (2212, -2212): 0.009979552357054559, (3122, -3122): 0.008941560453470589, (3312, -3312): 0.00561794710944335, (3334, -3334): 0.01518508769949144}
"""
