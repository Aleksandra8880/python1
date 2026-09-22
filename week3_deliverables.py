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
    try:
        average=bacteria/events #calculates average count of bacterial strain
        uncertainty=math.sqrt(average) #calculates the uncertainty 
        return average, uncertainty 
    except ZeroDivisionError:
        print ("There are no events!")
        return (0,0)
    except:
        print("An error occured!")
        return (0,0)

def count_bacteria(bacterial_id): #main function
    try:

        file_exists=False #variable to check of user's file exist
        while file_exists==False: #loop is running if user enters incorrect file name
            try: #accounts for error of wrong file name
                file_name=input("Enter the pathway to the file you want to work with:\n") #asks user for a pathway to open the file
                event_count=0 #initates the event count
                event_has_bacteria=False #variable to track validity of an event
                count={bacterial_id[name]:0 for name in bacterial_id} #creates a dictionary using dictionary comprehension (iterates over dict with bacterial names)
                #key is name of bacteria and the initial value is 0
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
                    file_exists=True #allows to exit the loop
            except FileNotFoundError:
                print("This file doesn't exist!") #warns user
                file_exists=False #continues the loop
            except:
                print("Couldn't open the file!")


        print("This program calculates the average amount of a bacterial strain per event.")
        print("Which bacteria are you interesed in? (Enter the bacteria's ID e.g. 211)\n")
        for i in bacterial_id: #iterates over bacterial id dictionary
            print(f"- ID {i}: {bacterial_id[i]}") #prints all available strraints for user
        print("- all\n") #prints an option to choose all

        answer_is_true=False
        while not answer_is_true: #asks for user's input until its correct
            answer=input("") 
            if answer in bacterial_id or answer.strip().lower()=="all": #if valid input saves the answer
                answer_is_true=True
            else:
                print("Incorrect index!") #warns about error
                

        print(f"Event count: {event_count}") #prints the event count
        if event_count==0: #handles possible divisom by 0
            print("There are no events. Can't count the bacteria.")
        elif answer.strip().lower()=="all": #checks if user asked for all strains
            for i in count: #iterates over dict with numbers of bacteria
                average, uncertainty = calculations(count[i], event_count) #calculates average and uncertainty for each specie
                print(f"Bacteria: {i} Average per event: {average} ± {uncertainty}") #prints the result for user
        else:
            average, uncertainty = calculations(count[bacterial_id[answer.strip()]], event_count) #calculates average and uncertainty for each specie
            print(f"The average count of {bacterial_id[answer.strip()]} is {average} ± {uncertainty} bacteria per event.") #prints the result for user  
    except:
        print("Something went wrong :(")

count_bacteria(bacterial_id) #runs the function