#!/bin/bash
#SBATCH --job-name=20ng_prep
#SBATCH --comment='Prepare datasets'
#SBATCH --mail-type=ALL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/20ng_prep.%j.out
#SBATCH --partition=All

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python prep_data.py --dataset 20ng && python prep_graph.py --dataset 20ng