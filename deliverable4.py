
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
            #averages collects p : average structures, when we read all files in "totalaverage_file" we colllect structures p : list of averages
            # in structure "averages_perfile" we store file : [list of averages of all p per one file]
            averages[p] = average
            uncertainty = (average)**0.5
            #print(f"For {p} average bacteria per event : {average} +/- {uncertainty}")
            
    print(f"File{file} processed.") 
    print(averages)       
    return events_count , averages


files = ["output-Set1.txt","output-Set2.txt","output-Set3.txt","output-Set4.txt","output-Set5.txt","output-Set6.txt","output-Set7.txt","output-Set8.txt","output-Set9.txt","output-Set10.txt"]


#the list of all events from all 10 files
events = []
#a dictionary with p as key an value: list with average count of certain ID per file
totalaverage_file = {p: [] for p in bacteria_code}
""""
It looks like this literally:

totalaverage_file
 {211: [20.024572575471208, 19.971747458376306, 19.94511458936193, 19.98632191831302, 19.93157933512171, 19.933049290832372, 19.947206260887654, 19.978216547537283, 19.92542571931885, 19.997188557406968], 
-211: [19.996584071717155, 19.93428613525858, 19.914467110154483, 19.949180832477097, 19.900389600821672, 19.902367068975973, 19.91029657748542, 19.94433021408623, 19.902180436954104, 19.9631369369799], 
321: [2.5160977787796295, 2.5106778529888456, 2.509016068304927, 2.5141419659153477, 2.508600253955597, 2.507949435525096, 2.5043117270308453, 2.508970995118548, 2.5091579218786904, 2.5208365396495775], 
-321: [2.516511765011878, 2.5059911249014117, 2.501618101932835, 2.507818833699672, 2.502299034882058, 2.501611547692281, 2.501874192905367, 2.5052920312950255, 2.498094311536186, 2.5116977254844155], 
2212: [1.2128951292677428, 1.207331923486943, 1.208708054527759, 1.2114488361708309, 1.2081547482329285, 1.2093279152984395, 1.2082975828328264, 1.2075234593526496, 1.2066463999930663, 1.2088075971811874], 
-2212: [1.1863891730679197, 1.1852936842926356, 1.1843725817883874, 1.18806603630436, 1.1817624345067583, 1.1826312414982194, 1.184000242670064, 1.1877073208780113, 1.182140048059318, 1.1878745970879785], 
3122: [0.2782637720864906, 0.2777693514417702, 0.2766444922758121, 0.27778211314439805, 0.27647573770633893, 0.2768331354999697, 0.27502751705190537, 0.2762992830570499, 0.2753096879177835, 0.2775958155676318], 
-3122: [0.2736297272459295, 0.27298945215333814, 0.27162870142171874, 0.27182098404151545, 0.2716588154228187, 0.2720634741849121, 0.27134196545418304, 0.2708198369382701, 0.2703564146622089, 0.27262972845843203],
 3312: [0.039300514990203046, 0.039385416756948836, 0.03980769189084911, 0.039703287508508156, 0.0396426420049491, 0.03891757713335124, 0.03928004992069889, 0.039461111965732334, 0.039361838128070065, 0.039839247044950565],
-3312: [0.039677654280314195, 0.039348581630972705, 0.03920943853055102, 0.03871482391908472, 0.03856138054769468, 0.03886125960647045, 0.03891387812762712, 0.038418955546937125, 0.03917332772857969, 0.0394100522620516], 
3334: [0.0012874755076208147, 0.0011743904870037008, 0.0011574901970984712, 0.0011770520374055431, 0.0011896042886426377, 0.00112851659634196, 0.00119168335023357, 0.0012046548208942613, 0.0012025663415765103, 0.0011661959252507429], 
-3334: [0.0011791021483934733, 0.001122387956213869, 0.0012051770591512171, 0.0011271953212723435, 0.0012372751344534537, 0.0011783359470441963, 0.0010703483182097882, 0.0011158223610801161, 0.0011115613211328825, 0.0011770341773441513]}
"""


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


#initiating the dictionaries connecting p with overall averages and std
averages_normal = {p : 0 for p in bacteria_code}
""""
averages_normal {211: 19.96404222526273, -211: 19.931721898491062, 321: 2.5109760539147103, -321: 2.505280866934113,
 2212: 1.2089141646344372, 
-2212: 1.1850237360153653, 3122: 0.276800090574915, -3122: 0.2718939099983327, 3312: 0.039469937734426135, 
-3312: 0.03902893521802833, 3334: 0.001187962955206821, -3334: 0.0011524239744295493}
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


            
