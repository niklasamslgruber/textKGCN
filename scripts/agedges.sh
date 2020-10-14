#!/bin/bash
#
#SBATCH --job-name=ag_data
#SBATCH --comment="Calculates doc2doc edges for the AG News dataset"
#SBATCH --mail-type=ALL
#SBATCH --mail-user="niklas.amslgruber@campus.lmu.de"
#SBATCH --ntasks=1
#SBATCH --output=out/ag_dataset.%j.out
#SBATCH --begin 20:00
#SBATCH --partition=All

source ~/miniconda3/bin/activate thesis

cd textKGCN
python prep_data.py
