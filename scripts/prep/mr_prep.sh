#!/bin/bash
#SBATCH --job-name=mr_prep
#SBATCH --comment='Train model'
#SBATCH --mail-type=ALL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/mr_prep.%j.out
#SBATCH --partition=All

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python prep_graph.py --dataset mr