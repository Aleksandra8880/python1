"""Week 2 Deliverable: Read particle event data and calculate momentum magnitude."""
# Importing important libraries
import math
import os
import urllib.request


def get_momentum(px, py, pz):
    """Calculates the magnitude of total momentum: sqrt(px^2 + py^2 + pz^2)."""
    return math.sqrt(px * px + py * py + pz * pz)


# Commands to download the file locally
def download_file(url, local_filename):
    """Downloads the file from a URL if it does not already exist locally."""
    if not os.path.exists(local_filename):
        print(f"Downloading {local_filename}...")
        urllib.request.urlretrieve(url, local_filename)
        print("Download complete.")
    else:
        print(f"File '{local_filename}' already found. Skipping download.")


def process_event(filename):
     """Reads an event file, validates particle count, and computes all momenta."""
     momenta = []
     with open(filename, "r") as infile:
        # Read event header: <event_id> <expected_count>
        header = infile.readline().strip().split()
        event_id = int(header[0])
        number_of_bacteria = int(header[1])

        for line in infile:
            line = line.strip()
            if not line:
                continue
        
            parts = line.split()
            if len(parts) < 4:
                continue

            # Extract 3-momentum components (ignoring particle code at index 3)
            px = float(parts[0])
            py = float(parts[1])
            pz = float(parts[2])
        
            p = get_momentum(px, py, pz)
            momenta.append(p)
            print(f"p: {p:.4f}")

     if len(momenta) == number_of_bacteria:
         print(f"Successfully processed all {number_of_bacteria} bacteria for Event {event_id}")

     return momenta

def main():
     url = "https://surfdrive.surf.nl/s/EL7lViIcZGfKOx3/download"
     filename = "output-Set0.txt"
     download_file(url, filename)
     process_event(filename)

if __name__ == "__main__":
    main()
