from math import sqrt #imports sqrt function from math library
import os #library to create files etc.
import math

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


def calculate_momentum(x,y,z): #defines the function to calculate momentum
    sqrd_values=x**2+y**2+z**2 #saves into a variable sum of squared momentum components
    try: 
        p=sqrt(sqrd_values) #tries to calculate the final momentum
        return p #returns the momentum
    except ValueError: #if a value error occurs (e.g. number inside sqrt is negative warns the user about error)
        print("Can't compute the square root of negative number")
    except: #if another error occurs warns the user about error
        print("An error occured")


def clean_file(filename, bacterial_id): #a function to clean dataset
    name, doc_ext=filename.rsplit(".", 1)
    cleaned_filename=f"{name}_cleaned.{doc_ext}" #introduces name for cleaned file
    if os.path.exists(cleaned_filename): #check if cleaned version already exists
        return cleaned_filename #refers user to it
    incorrect_values=0 #counts how many data lines were removed
    with open(filename, "r") as file: #opens file for reading
        lines=file.readlines() #reads file lien by line and saves into a list
        clean_version=[lines[0]] #creates a list with cleaned version of file, writes the header into it

        for line in lines [1:]: #iterates over lines of file starting from 2nd (skips header)
            values=line.split() #splits line in separate values 
            if values[3] in bacterial_id: #checks if bacterial id is valid (present in list of existing id's)
                clean_version.append(line) #if so, adds to cleaned_list
            else:
                incorrect_values+=1 #counts incorrect bacterial id

    if incorrect_values>0: #checks if during cleaning any data was removed 
        with open(cleaned_filename, 'w') as final_file: #opens a new file
            final_file.writelines(clean_version) #saves cleaned data to new file
        return cleaned_filename #returns it for further analyses
    else: #if no data was removed
        return filename #returns the original file for further analyses


def bacterial_momentum():
    print("--The momentum of each bacteria--\n") #prints the title
    dataset=input("Enter the name of the file you want to work with:") #asks user for file name
    filename=clean_file(dataset, bacterial_id) #saves the name of file that will be used in a variable
    with open(filename, "r") as file: #opens the file for reading
        for i, line in enumerate(file): #iterates over each line in file, saves line index as "i" and line content as "line"
            values=line.split() #splits the line string into separate values
            if i==0: 
                continue #skips the first line
            x=float(values[0]) #saves x component as separate variable
            y=float(values[1]) #saves y component as separate variable
            z=float(values[2]) #saves z component as separate variable
            momentum=calculate_momentum(x, y, z) #calls the function to calculate the momentum and saves the result in a variable
            print(f"Bacteria No. {i} Momentum: {momentum}") #prints the calculated momentum & explains what's printed

def count_bacteria(bacterial_id):
    dataset=input("Enter the path for the file you want to work with:\n") #asks user for file path
    print("Here's the list of bacterias present in the experiment:\n") 
    for name in bacterial_id: #iterates over available bacterial straints & prints it
        print(f"- {bacterial_id[name]} ID {name}")
    print() #empty line
    bacterial_strain=input("Which bacteria are you interested into? Enter bacteria's ID (e.g. '211')\n") #saves the straint that user choose into a variable
    event_count=0 #sets an event counter
    bacteria_count=0 #sets overall bacteria counter
    per_event_count=0 #sets bacteria count per event/run/experiment
    with open(dataset, "r") as file: #opens the data file
        for line in file: #iterates over every line
            values=line.split() #splits line into separate variables
            if len(values)==2: #activated if line is a header
                if per_event_count>0: #if there was at least one bacteria of chosen strain in the event
                    event_count+=1 #counts an event as valid
                    per_event_count=0 #sets the counter of bacteria per evenet back to zero
            else:
                if bacterial_strain==values[3]: #selects the lines with required bacteria strain
                    bacteria_count+=1 #adds bacteria to total list of bacterias
                    per_event_count+=1 #adds bacteria to the list of bacterias in this specific event (to check validity of event)
        if per_event_count>0: #when the dataset is finished checks the last event
            event_count+=1 #if there was at least one bacteria in event, adds event to list
    average_count=bacteria_count/event_count #calculates average amount of bacteria per event by dividing total number of bacteria with number of valid events 
    uncertanty=math.sqrt(average_count) #calculates the uncertanty - square root of mean 
    print(f"There is on average {average_count} ± {uncertanty} bacterias per event.") #prints the output
    print(f"There are {event_count} events and {bacteria_count} {bacterial_strain}")

#bacterial_momentum()
count_bacteria(bacterial_id)

