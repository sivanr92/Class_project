import re
from Bio import SeqIO

# Function to extract sequence from a given region
def extract_sequence(sequence, start, end):
    return sequence[start - 1:end]

# Read GH31 sequences from the FASTA file
gh31_sequences = SeqIO.to_dict(SeqIO.parse("batch_500_protein_sequences.fasta", "fasta"))

# Open the overview file containing the data
with open("gh31_hmmscan.out.dm.ps.stringent", "r") as file:
    for line in file:
        # Split the line into columns
        columns = line.strip().split("\t")
        
        # Check if the line has enough columns
        if len(columns) >= 10:
            sequence_id = columns[2]
            description = columns[7]+","+columns[8]
            
            
            #print (sequence_id,description)
            
            # Check if GH31 regions were found
            if description:
                extracted_sequence = ""
                
                # Extract and concatenate GH31 sequences based on the regions
                # print (description)
                # print (int(description.split(",")[0]), int(description.split(",")[1]))
                start, end = int(description.split(",")[0]), int(description.split(",")[1])
                
                # Check if the sequence ID is present in the GH31 FASTA file
                if sequence_id in gh31_sequences:
                    sequence = str(gh31_sequences[sequence_id].seq)
                    extracted_sequence = extract_sequence(sequence, start, end)
            
                    # Print or process the extracted GH31 sequence
                    #print(f">{sequence_id}|GH31{'('+str(start)+'-'+str(end)+')'}|{(end-start)+1}|{len(extracted_sequence)}")
                    print(f">{sequence_id}|GH31{'('+str(start)+'-'+str(end)+')'}|{len(extracted_sequence)}")
                    print(f"{extracted_sequence}")
