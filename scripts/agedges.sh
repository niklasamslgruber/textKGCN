#!/bin/bash
#
#SBATCH --job-name=ag_data
#SBATCH --comment="Calculates doc2doc edges for the AG News dataset"
#SBATCH --mail-type=ALL
#SBATCH --mail-user="niklas.amslgruber@campus.lmu.de"
#SBATCH --ntasks=1
#SBATCH --output=out/ag_dataset.%j.out
#SBATCH --partition=All

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python prep_data.py
python prep_graph.py
