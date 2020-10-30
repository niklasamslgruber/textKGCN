#!/bin/bash
#SBATCH --job-name=r8_prep
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/r8_prep.%j.out
#SBATCH --partition=All

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python prep_graph.py --dataset r8