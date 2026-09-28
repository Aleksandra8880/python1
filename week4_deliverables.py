'''
1. deliverable: 10 averages for each ID
2. 1 final average (weighted or normal) of each bacterial strain per event
3. uncertianty - std of point 1 

1 file - 1 sub sample
'''
import numpy as np #imports necessary library
import statistics 
from pathlib import Path

bacterial_id={
    "211":"E. coli WT", 
    "-211":"E. coli mutant", 
    "321":"Bacillus subtilis WT", 
    "-321":"Bacillus subtilis mutant", 
    "2212":"Pseudomonas aeruginosa WT", 
    "-2212":"Pseudomonas aeruginosa antibiotic-resistant", 
    "3122":"Streptococcus pneumoniae", 
    "-3122":"Capsule-deficient streptococcus pneumoniae", 
    "3312":"Mycobacterium tuberculosis", 
    "-3312":"Drug-resistant mycobacterium tuberculosis", 
    "3334":"Salmonella enterica", 
    "-3334":"Salmonella mutant"
    }     #dictionary of all existing bacterial id

def average_in_subsample(event_count, bacteria_count): #calculates the average amount of bacteria per strain in a subsample
    average={}
    if event_count==0: #handles possible divison by 0
            print("There are no events. Can't count the bacteria.")
            return
    for name in bacteria_count: #iterates over dict with numbers of bacteria
        average[name]=bacteria_count[name]/event_count #calculates average and uncertainty for each specie
    return average


def count_bacteria_in_subsample(bacterial_id, file_name): #counts bacteria in a subsample
        try: #accounts for error of wrong file name
            event_count=0 #initates the event count
            event_has_bacteria=False #variable to track validity of an event
            bacteria_count={bacterial_id[name]:0 for name in bacterial_id} #creates a dictionary using dictionary comprehension (iterates over dict with bacterial names)
            #key is name of bacteria and the initial value is 0
            with open (file_name, "r") as file: #opens the file for reading
                for line in file: #iterates over each line
                    values=line.split() #splits the line in to separate values 
                    
                    if len(values)==2: #if it is a header
                        if event_has_bacteria: #ifprevious event contains data 
                            event_count+=1 #increases event count
                            event_has_bacteria=False #resets the tracking variable
                    elif len(values)==4 and values[3] in bacterial_id: #if it is a data line and bacterias id is present in my list
                        bacteria_count[bacterial_id[values[3]]]+=1 #increases the number of this specific strain
                        event_has_bacteria=True #indicates that there is bacteria in this event
                if event_has_bacteria: #checks the last event
                    event_count+=1 #if there was bacteria in last event, counts the event
                return average_in_subsample(event_count, bacteria_count), event_count #returns a list with bacteria strain and its average per subsample
        except FileNotFoundError:
            print("This file doesn't exist!") #warns user
        except:
            print("Couldn't open the file!")

def get_files():
    files_list=[]
    folder=Path(input("Enter the name of folder with your data files:\n").strip())

    if not folder.is_dir():
        print("Folder not found!")
        return []
    
    for f in folder.iterdir():
        if f.is_file() and f.name.startswith("output-Set") and f.name.endswith(".txt"):
            files_list.append(f)
    return files_list
    
def main():
    final_avg_list={} #creates an empty dictionary 
    files_list=get_files()
    if len(files_list)<2:
        print("Need at least 2 files!")
        return

    for bacteria in bacterial_id:
        final_avg_list[bacterial_id[bacteria]]=[] #adds to dict bacterial names as keys and an empty list as values


    try:
        events=[]
        for subsample in files_list: #iterates over all files
            results, event_count =count_bacteria_in_subsample(bacterial_id, subsample) #saves in a variable the list of averages from file
            events.append(event_count)

            for name, avg in results.items(): #iterates over receivef list and saves keys and values to separate variables
                final_avg_list[name].append(avg) #saves the averages in a dictionary using bacteria's name as key and average as value
    except:
        print("Something went wrong with calculating averages!")
        return
    
    final_averages={}
    
    for name, averages in final_avg_list.items(): #iterates over the list of subsample averages per bacterial strain
        weighted_avg=np.average(averages, weights=events)
        std=statistics.stdev(averages)
        final_averages[name]=weighted_avg, std
    


    for name, value in final_averages.items():    
        print(name)
        print(f" weighted average: {value[0]} ± {value[1]}")
    

main()