import os #library to create files etc.
import math #library for math expressions

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

def calculations(bacteria, events): #separate function for calculations
    average=bacteria/events #calculates average count of bacterial strain
    uncertainty=math.sqrt(average) #calculates the uncertainty 
    return average, uncertainty 

def count_bacteria(bacterial_id): #main function
    count={bacterial_id[name]:0 for name in bacterial_id} #creates a dictionary using dictionary comprehension (iterates over dict with bacterial names)
    #key is name of bacteria and the initial value is 0
    event_count=0 #initates the event count
    event_has_bacteria=False #variable to track validity of an even
    file_name=input("Enter the pathway to the file you want to work with:\n") #asks user for a pathway to open the file
    

    with open (file_name, "r") as file: #opens the file for reading

        for line in file: #iterates over each line
            values=line.split() #splits the line in to separate values 

            if len(values)==2: #if it is a header
                if event_has_bacteria: #ifprevious event contains data 
                    event_count+=1 #increases event count
                    event_has_bacteria=False #resets the tracking variable
            elif len(values)==4 and values[3] in bacterial_id: #if it is a data line and bacterias id is present in my list
                count[bacterial_id[values[3]]]+=1 #increases the number of this specific strain
                event_has_bacteria=True #indicates that there is bacteria in this event
        if event_has_bacteria: #checks the last event
            event_count+=1 #if there was bacteria in last event, counts the event
    print(f"Event count: {event_count}") #prints the event count

    print("Which bacteria are you interesed in? (Enter the bacteria's ID e.g. 211)\n")
    for i in bacterial_id:
        print(f"- ID {i}: {bacterial_id[i]}")
    print("- all")
    answer=input("")

    if answer.lower()=="all":
        for i in count: #iterates over dict with numbers of bacteria
            average, uncertainty = calculations(count[i], event_count) #calculates average and uncertainty for each specie
            print(f"The average count of {i} is {average} ± {uncertainty}") #prints the result for user
    else:
        average, uncertainty = calculations(count[bacterial_id[answer]], event_count) #calculates average and uncertainty for each specie
        print(f"The average count of {bacterial_id[answer]} is {average} ± {uncertainty}") #prints the result for user  

count_bacteria(bacterial_id) #runs the function