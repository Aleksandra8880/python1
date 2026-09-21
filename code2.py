# This code is for file 7

import math
import os
import urllib.request

def download_file(url, local_filename):
    """Download the file from the URL if it does not exist locally."""
    if not os.path.exists(local_filename):
        print(f"Downloading {local_filename}...")
        urllib.request.urlretrieve(url, local_filename)
        print("Download complete.")
    else:
        print(f"File {local_filename} found. Skipping download.")

def process_all_bacteria(filename, bacteria_order):
    total_events = 0
    relevant_events = 0
    counts = {bac_id: 0 for bac_id in bacteria_order}

    with open(filename, "r") as infile:
        while True:
            header_line = infile.readline()
            if not header_line:
                break  # End of file reached
            
            parts = header_line.split()
            if not parts:
                continue

            event_id = int(parts[0])
            num_bacteria = int(parts[1])
            total_events += 1

            event_has_target = False

            for _ in range(num_bacteria):
                bac_line = infile.readline()
                tokens = bac_line.split()
                if not tokens:
                    continue

                bac_id = int(tokens[-1])

                if bac_id in counts:
                    counts[bac_id] += 1
                    event_has_target = True

            # Only count this event as relevant if at least one target bacterium was found
            if event_has_target:
                relevant_events += 1

    return total_events, relevant_events, counts

def main():
    strains = [
        (211, "E. coli (wild type)"),
        (-211, "E. coli (mutant)"),
        (321, "B. subtilis (wild type)"),
        (-321, "B. subtilis (mutant)"),
        (2212, "P. aeruginosa (wild type)"),
        (-2212, "P. aeruginosa (mutant)"),
        (3122, "S. pneumoniae (wild type)"),
        (-3122, "S. pneumoniae (mutant)"),
        (3312, "M. tuberculosis (wild type)"),
        (-3312, "M. tuberculosis (mutant)"),
        (3334, "S. enterica (wild type)"),
        (-3334, "S. enterica (mutant)"),
    ]

    bacteria_order = [bac_id for bac_id, _ in strains]
    url = "https://surfdrive.surf.nl/s/?dir=/&editing=false&openfile=true"
    filename = "output-Set7.txt"

    download_file(url, filename)

    total_events, relevant_events, counts = process_all_bacteria(filename, bacteria_order)

    print(f"Total events inspected: {total_events}")

    # Print matching the exact reference output format
    for bac_id, name in strains:
        count = counts[bac_id]
        mean = count / relevant_events if relevant_events > 0 else 0.0
        uncertainty = math.sqrt(mean)
        print(f"{name} {mean} +/- {uncertainty}")


if __name__ == "__main__":
    main()