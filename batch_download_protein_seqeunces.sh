#!/bin/bash

# Define your email address (required by NCBI)
EMAIL="yourmail@unl.edu"

# Define the input file with protein IDs
IDS_FILE="uniq_list_ids.txt"

# Define the output file for the downloaded protein sequences
OUTPUT_FILE="batch_protein_sequences.fasta"

# Define the NCBI API URL
API_URL="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

# Set the database (in this case, "protein")
DB="protein"

# Set the file format (in this case, "fasta")
FORMAT="fasta"

# Initialize the output file
> "$OUTPUT_FILE"

# Loop through each protein ID in the input file and fetch in batches
BATCH_SIZE=500
current_batch=0
ids_in_batch=""

while read -r ID; do
  ids_in_batch="$ids_in_batch,$ID"
  ((current_batch++))

  # If the batch size is reached, fetch the batch
  if [ $current_batch -eq $BATCH_SIZE ]; then
    ids_in_batch=${ids_in_batch:1}  # Remove the leading comma
    echo "Fetching sequences for batch: $ids_in_batch..."
    curl -s "$API_URL" -d "db=$DB&id=$ids_in_batch&rettype=$FORMAT" >> "$OUTPUT_FILE"
    current_batch=0
    ids_in_batch=""
  fi
done < "$IDS_FILE"

# Fetch any remaining IDs in the last batch
if [ -n "$ids_in_batch" ]; then
  ids_in_batch=${ids_in_batch:1}  # Remove the leading comma
  echo "Fetching sequences for batch: $ids_in_batch..."
  curl -s "$API_URL" -d "db=$DB&id=$ids_in_batch&rettype=$FORMAT" >> "$OUTPUT_FILE"
fi

echo "Finished fetching protein sequences. Saved in $OUTPUT_FILE."
