from math import sqrt
from pathlib import Path
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

with open("result0.txt", "w") as outfile:
    outfile.write(f"Analysis results of bacteria movement and wild-mutant asymmetry \n\n")

#creating the function calculate_momentum
def calculate_momentum(px,py,pz):
    total_momentum = (px**2 + py**2 + pz**2)**0.5
    return total_momentum

#python list of all the bacteria we are intersted in
bacteria_code = [211, -211, 321, -321, 2212, -2212, 3122, -3122, 3312,-3312, 3334,-3334]
mutant_wild_pairs = [(211,-211), (321,-321),(2212,-2212),(3122,-3122), (3312,-3312), (3334,-3334)
                     ]
files = ["output-Set1.txt","output-Set2.txt","output-Set3.txt", "output-Set4.txt", "output-Set5.txt","output-Set6.txt","output-Set7.txt","output-Set8.txt","output-Set9.txt","output-Set10.txt"]

#setting up the bins and the x- axis

bins_sections = [np.arange(0,61,1),
                 np.arange(0,61,4),
                 np.arange(0,61,2),
                 np.arange(0,61,4),
                 np.arange(0,61,4),
                 np.arange(0,61,6),
]

#connecting the personalized bins to the bacteria. The size of the bin depends of how often the bacteria occurs, to make it significant
bins_i = dict(zip(mutant_wild_pairs,bins_sections))

centers = {i : (edges[:-1] + edges[1:])/2  for i, edges in bins_i.items()}

momenta_file = {file : { p :[] for p in bacteria_code} for file in files}




def mean_valuebacteria(file):
    events_count = 0
    bacteria_count = {p: 0 for p in bacteria_code}
    relevant_rows = 0
    averages = {p : 0 for p in bacteria_code}
    with open ( file, "r") as infile:
        # here we need to split the lines into lists, line numbering starts from 0
        for line_number, line in enumerate(infile):
            
            data = line.split()
                 

            try:
                #checking the how many valid events we have  
                #zeroes out the count of sub-variable relevant_rows whenever a new header is reached - > in in next lines bacteria is found, event_count will be increased
                if len(data) == 2:
                    relevant_rows = 0 
                    continue
                


                #we check whether any non-useful lines are there
                elif len(data) == 4:
                    
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
                        momenta_file[file][bacteria_id].append(total_momentum)


                    # we still inside the loop that checks the data between the headers. 
                    # The relevant_rows increases each time the bacteria is found, but we only care if one bacteria is found and count that part as a valid event
                    #Therefore this part of the code ensures increasing the event_count max only once per investigated chunck
                        if relevant_rows == 1:
                            events_count += 1
                else:
                    raise ValueError(f"This row is not a header but it also does not have 4 entries. It should be checked.")
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


#initiating the dictionaries connecting p with overall averages and std
averages_normal = {p : 0 for p in bacteria_code}

#first_file = files[0]
#print(first_file)
"""
for bacteria_id, values in momenta_file[first_file].items():
    print(f"{bacteria_id}: {values[:5]}")
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
    with open("result0.txt", "a") as outfile:
        outfile.write(f"For {p} the average from all files is {average_from_all_files} with standard deviation {standard_deviation}\n")
    print(f"For {p} the average from all files is {average_from_all_files} with standard deviation {standard_deviation}")

"""
CHECKING THE WEIGHTED AVERAGE

"""


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
        else:
        
            print(f"{p}The difference between the weighted mean and unweighted one is insignificant. The number of events per file are consistent.")
weighted_vs_unweighted()


""""
CHECKING ASYMMETRY
"""

i_asymmetry = {i  : 0 for i in mutant_wild_pairs}
i_uncertainty = {i  : 0 for i in mutant_wild_pairs}

def mutant_vs_wild_asymmetry():
    count = {}    
    for i in mutant_wild_pairs:

        count[i[0]] = []
        for file in files:
        
            count[i[0]].append(len(momenta_file[file][i[0]]) )

        count[i[1]] = []
        for file in files:
        
            count[i[1]].append( len(momenta_file[file][i[1]]))
        
        asymmetry = ( np.asarray(count[i[0]]) - np.asarray(count[i[1]]))
        #mean difference from all 10 files
        mean_asym = np.mean(asymmetry)

        #now take a squareroot to obtain the standard deviation of the Poisson distribution
        if mean_asym >= 0:
            uncertainty_A = np.sqrt(mean_asym)

        i_asymmetry[i] = asymmetry
        i_uncertainty[i] = uncertainty_A

        #checking whether it crosses the 0
        up_bound = mean_asym - 3*uncertainty_A
        low_bound = mean_asym + 3*uncertainty_A

        if up_bound > 0:
            with open("result0.txt", "a") as outfile:
                outfile.write(f"There is a significant asymmetry in pair {i}. Wild type is more present within the samples.\n")
            print(f"There is a significant asymmetry in pair {i}. Wild type is more present within the samples.")
        if low_bound < 0:
            with open("result0.txt", "a") as outfile:
                outfile.write(f"There is a significant asymmetry in pair {i}. Wild type is more present within the samples.\n")
            print(f"There is a significant asymmetry in pair {i}. Mutant type is more present within the samples.")
        with open("result0.txt", "a") as outfile:
            outfile.write(f"Assymetry of pair {i} is {mean_asym} with the standard deviation {uncertainty_A}\n")
        print(f"Assymetry of pair {i} is {mean_asym} with the standard deviation {uncertainty_A}")
        
    
mutant_vs_wild_asymmetry()

"""
ASYMMETRY AS A FUNCTION OF MOMENTUM
"""

hist_binned = {p: [] for p in bacteria_code}
# different bins per files, maybe iterate per numpy array
for file in files:
    for i , edges in bins_i.items():

        for p in i:
        #occurance is the number of bacteria which falls into each bin, occurance is a list of length equal to the number of bins
            occurance , bins = np.histogram(momenta_file[file][p], bins = edges)
            hist_binned[p].append(occurance)

#print(hist_binned[211][:3])


#transforming 'hist_binned' into a numpy array, rows are histogram counts, colums are bins
for p in bacteria_code:
    hist_binned[p] = np.asarray(hist_binned[p])

# for each i we store "difference" , "mean_dots", "errorbars", do each i has its own dictionary of those
difference_results = {}

for i in mutant_wild_pairs:
    #wild type histogram
    occurance1 = hist_binned[i[0]]
    #mutant strain histogram
    occurance2 = hist_binned[i[1]]
    #now we need to substract them, substracting two numpy array rows per file , bin by bin
    difference = occurance1 - occurance2

    mean_asym = np.mean(difference , axis = 0)

    # mean_asymmetry can be negative, therefore we need the absolute value to take a sqrt

    absolute_mean_asym = np.abs(mean_asym)

    errors = np.sqrt(absolute_mean_asym)

    #print(errors)


    difference_results[i] = {"difference"  : difference, 
                               "mean dots" : mean_asym,
                               "errorbars" : errors}

"""
CURVE FITTING
"""

#block for curve fitting
pair1 = (211,-211)
x = centers[pair1]
def model_f211(x, A , k ):
    return A * np.exp(-k * x)

y_data1 = difference_results[pair1]["mean dots"]
errorbars1 = difference_results[pair1]["errorbars"]

popt , pcov = curve_fit(model_f211, x , y_data1 , sigma = errorbars1 , p0 = [2800 , 0.2])

A_opt , k_opt = popt
with open("result0.txt", "a") as outfile:
    outfile.write(f"{pair1} A : {A_opt} ,k: {k_opt}\n")
print(f"{pair1} A : {A_opt} ,k: {k_opt}")

x_model = np.linspace(min(x) , max(x), 200)
y_model = model_f211(x_model, A_opt , k_opt)

y_fitted = model_f211(x,*popt)

residuals1 = y_data1 - y_fitted

fig, (ax_data, ax_residuals) = plt.subplots(
    2, 1,
    figsize=(7, 6),
    sharex=True,
    gridspec_kw={"height_ratios": [3, 1]},
)

# Upper plot: data and fitted curve
ax_data.errorbar(
    x, y_data1,
    yerr=errorbars1,
    fmt="o",
    capsize=4,
    label="data",
)
ax_data.plot(
    x_model, y_model,
    color="violet",
    label="exponential decay fit",
)
ax_data.set_ylabel(f"N({pair1[0]}) - N({pair1[1]})")
ax_data.set_title(f"Pair {pair1}")
ax_data.legend()

# Lower plot: residuals
ax_residuals.errorbar(
    x, residuals1,
    yerr=errorbars1,
    fmt="o",
    capsize=4,
)
ax_residuals.axhline(0, color="black", linestyle="--" , label = "zero-residuals line")
ax_residuals.set_xlabel("Momentum [kg m/s]")
ax_residuals.set_ylabel(f"Data {pair1} vs fit")
ax_residuals.legend()
plt.tight_layout()
plt.show()

#block for curve fitting
pair2 = (321, -321)
x = centers[pair2]
def model_f211(x, A , k ):
    return A * np.exp(-k * x)

y_data2 = difference_results[pair2]["mean dots"]
errorbars2 = difference_results[pair2]["errorbars"]

popt , pcov = curve_fit(model_f211, x , y_data2 , sigma = errorbars2 , p0 = [600 , 0.2])

A_opt , k_opt = popt
with open("result0.txt", "a") as outfile:
    outfile.write(f"{pair2} A : {A_opt} ,k: {k_opt}\n")
print(f"{pair2} A : {A_opt} ,k: {k_opt}")

x_model = np.linspace(min(x) , max(x), 200)
y_model = model_f211(x_model, A_opt , k_opt)
y_fitted = model_f211(x,*popt)
residuals2 = y_data2 - y_fitted

fig, (ax_data, ax_residuals) = plt.subplots(
    2, 1,
    figsize=(7, 6),
    sharex=True,
    gridspec_kw={"height_ratios": [3, 1]},
)

# Upper plot: data and fitted curve
ax_data.errorbar(
    x, y_data2,
    yerr=errorbars2,
    fmt="o",
    capsize=4,
    label="data",
)
ax_data.plot(
    x_model, y_model,
    color="violet",
    label="exponential decay fit",
)
ax_data.set_ylabel(f"N({pair2[0]}) - N({pair2[1]})")
ax_data.set_title(f"Pair {pair2}")
ax_data.legend()

# Lower plot: residuals
ax_residuals.errorbar(
    x, residuals2,
    yerr=errorbars2,
    fmt="o",
    capsize=4,
)
ax_residuals.axhline(0, color="black", linestyle="--", label = "zero-residuals line")
ax_residuals.set_xlabel("Momentum [kg m/s]")
ax_residuals.set_ylabel(f"Data {pair2} vs fit")
ax_residuals.legend()
plt.tight_layout()
plt.show()

#block for cuve fitting
pair3 = (2212 , -2212)
x = centers[pair3]
def model_f211(x, A , k ):
    return A * np.exp(-k * x)

y_data3 = difference_results[pair3]["mean dots"]
errorbars3 = difference_results[pair3]["errorbars"]

popt , pcov = curve_fit(model_f211, x , y_data3 , sigma = errorbars3 , p0 = [3700 , 0.1])

A_opt , k_opt = popt
with open("result0.txt", "a") as outfile:
    outfile.write(f"{pair3} A : {A_opt} ,k: {k_opt}\n")
print(f"{pair3} A : {A_opt} ,k: {k_opt}")

x_model = np.linspace(min(x) , max(x), 200)
y_model = model_f211(x_model, A_opt , k_opt)
y_fitted = model_f211(x,*popt)
residuals3 = y_data3 - y_fitted

fig, (ax_data, ax_residuals) = plt.subplots(
    2, 1,
    figsize=(7, 6),
    sharex=True,
    gridspec_kw={"height_ratios": [3, 1]},
)

# Upper plot: data and fitted curve
ax_data.errorbar(
    x, y_data3,
    yerr=errorbars3,
    fmt="o",
    capsize=4,
    label="data",
)
ax_data.plot(
    x_model, y_model,
    color="violet",
    label="exponential decay fit",
)
ax_data.set_ylabel(f"N({pair3[0]}) - N({pair3[1]})")
ax_data.set_title(f"Pair {pair3}")
ax_data.legend()

# Lower plot: residuals
ax_residuals.errorbar(
    x, residuals3,
    yerr=errorbars3,
    fmt="o",
    capsize=4,
)
ax_residuals.axhline(0, color="black", linestyle="--", label = "zero-residuals line")
ax_residuals.set_xlabel("Momentum [kg m/s]")
ax_residuals.set_ylabel(f"Data {pair3} vs fit")
ax_residuals.legend()
plt.tight_layout()
plt.show()

#block for cuve fitting
pair4 = (3122,-3122)
x = centers[pair4]
def model_f211(x, A , k ):
    return A * np.exp(-k * x)

y_data4 = difference_results[pair4]["mean dots"]
errorbars4 = difference_results[pair4]["errorbars"]

popt , pcov = curve_fit(model_f211, x , y_data4 , sigma = errorbars4 , p0 = [800 , 0.1])

A_opt , k_opt = popt
with open("result0.txt", "a") as outfile:
    outfile.write(f"{pair4} A : {A_opt} ,k: {k_opt}\n")
print(f"{pair4} A : {A_opt} ,k: {k_opt}")

x_model = np.linspace(min(x) , max(x), 200)
y_model = model_f211(x_model, A_opt , k_opt)
y_fitted = model_f211(x,*popt)
residuals4 = y_data4 - y_fitted

fig, (ax_data, ax_residuals) = plt.subplots(
    2, 1,
    figsize=(7, 6),
    sharex=True,
    gridspec_kw={"height_ratios": [3, 1]},
)

# Upper plot: data and fitted curve
ax_data.errorbar(
    x, y_data4,
    yerr=errorbars4,
    fmt="o",
    capsize=4,
    label="data",
)
ax_data.plot(
    x_model, y_model,
    color="violet",
    label="exponential decay fit",
)
ax_data.set_ylabel(f"N({pair4[0]}) - N({pair4[1]})")
ax_data.set_title(f"Pair {pair4}")
ax_data.legend()

# Lower plot: residuals
ax_residuals.errorbar(
    x, residuals4,
    yerr=errorbars4,
    fmt="o",
    capsize=4,
)
ax_residuals.axhline(0, color="black", linestyle="--", label = "zero-residuals line")
ax_residuals.set_xlabel("Momentum [kg m/s]")
ax_residuals.set_ylabel(f"Data {pair4} vs fit")
ax_residuals.legend()
plt.tight_layout()
plt.show()


#block for cuve fitting
pair5 = (3312,-3312)
x = centers[pair5]
def model_f211(x, A , k ):
    return A * np.exp(-k * x)

y_data5 = difference_results[pair5]["mean dots"]
errorbars5 = difference_results[pair5]["errorbars"]

popt , pcov = curve_fit(model_f211, x , y_data5 , sigma = errorbars5 , p0 = [60 , 0.1])

A_opt , k_opt = popt
with open("result0.txt", "a") as outfile:
    outfile.write(f"{pair5} A : {A_opt} ,k: {k_opt}\n")
print(f"{pair5} A : {A_opt} ,k: {k_opt}")

x_model = np.linspace(min(x) , max(x), 200)
y_model = model_f211(x_model, A_opt , k_opt)
y_fitted = model_f211(x,*popt)
residuals5 = y_data5 - y_fitted

fig, (ax_data, ax_residuals) = plt.subplots(
    2, 1,
    figsize=(7, 6),
    sharex=True,
    gridspec_kw={"height_ratios": [3, 1]},
)

# Upper plot: data and fitted curve
ax_data.errorbar(
    x, y_data5,
    yerr=errorbars5,
    fmt="o",
    capsize=4,
    label="data",
)
ax_data.plot(
    x_model, y_model,
    color="violet",
    label="exponential decay fit",
)
ax_data.set_ylabel(f"N({pair5[0]}) - N({pair5[1]})")
ax_data.set_title(f"Pair {pair5}")
ax_data.legend()

# Lower plot: residuals
ax_residuals.errorbar(
    x, residuals5,
    yerr=errorbars5,
    fmt="o",
    capsize=4,
)
ax_residuals.axhline(0, color="black", linestyle="--", label = "zero-residuals line")
ax_residuals.set_xlabel("Momentum [kg m/s]")
ax_residuals.set_ylabel(f"Data {pair5} vs fit")
ax_residuals.legend()

plt.tight_layout()
plt.show()

#block for cuve fitting, I had issues here with error bars being zero and scipy was giving me errors

pair6 = (3334,-3334)
x = centers[pair6]

def model_f211(x, A , k ):
    return A * np.exp(-k * x)

y_data6 = difference_results[pair6]["mean dots"]

errorbars6 = difference_results[pair6]["errorbars"]

valid = ( np.isfinite(x)
& np.isfinite(y_data6)
& np.isfinite(errorbars6)
&( errorbars6 > 0)

)

x = x[valid]
y_data6 = y_data6[valid]
errorbars6 = errorbars6[valid]
popt , pcov = curve_fit(model_f211, x , y_data6 , sigma = errorbars6 , p0 = [100 , 0.1])

A_opt , k_opt = popt
with open("result0.txt", "a") as outfile:
    outfile.write(f"{pair6} A : {A_opt} ,k: {k_opt}\n")
print(f"{pair6} A : {A_opt} ,k: {k_opt}")

x_model = np.linspace(min(x) , max(x), 200)
y_model = model_f211(x_model, A_opt , k_opt)
y_fitted = model_f211(x,*popt)

residuals6 = y_data6 - y_fitted

fig, (ax_data, ax_residuals) = plt.subplots(
    2, 1,
    figsize=(7, 6),
    sharex=True,
    gridspec_kw={"height_ratios": [3, 1]},
)

# Upper plot: data and fitted curve
ax_data.errorbar(
    x, y_data6,
    yerr=errorbars6,
    fmt="o",
    capsize=4,
    label="data",
)
ax_data.plot(
    x_model, y_model,
    color="violet",
    label="exponential decay fit",
)
ax_data.set_ylabel(f"N({pair6[0]}) - N({pair6[1]})")
ax_data.set_title(f"Pair {pair6}")
ax_data.legend()

# Lower plot: residuals
ax_residuals.errorbar(
    x, residuals6,
    yerr=errorbars6,
    fmt="o",
    capsize=4,
)
ax_residuals.axhline(0, color="black", linestyle="--", label = "zero-residuals line")
ax_residuals.set_xlabel("Momentum [kg m/s]")
ax_residuals.set_ylabel(f"Data {pair6} vs fit")
ax_residuals.legend()
plt.tight_layout()
plt.show()

