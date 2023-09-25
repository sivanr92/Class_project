#!/bin/bash
#SBATCH --time=24:00:00          # Run time in hh:mm:ss
#SBATCH --mem=100gb       # Maximum memory required per CPU (in megabytes)
#SBATCH --job-name=hmmscan
#SBATCH --error=/home/yourlab/user/gh31_project/job.%J.err
#SBATCH --output=/home/yourlab/user/gh31_project/job.%J.out
#SBATCH --partition=yourpartition,batch,guest

ml hmmer/3.3
hmmscan --domtblout gh31_hmmscan.out.dm dbCAN-fam-HMMs.txt batch_500_protein_sequences.fasta > gh31_hmmscan.out
