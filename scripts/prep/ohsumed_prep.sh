#!/bin/bash
#SBATCH --job-name=ohsumed_prep
#SBATCH --comment='Prepare datasets'
#SBATCH --mail-type=ALL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/ohsumed_prep.%j.out
#SBATCH --partition=All

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python prep_data.py --dataset ohsumed && python prep_graph.py --dataset ohsumed