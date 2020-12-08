#!/bin/bash
#SBATCH --job-name=t30_count_20ng
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/t30_count_20ng.%j.out
#SBATCH --partition=Luna

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --threshold 30 --dataset 20ng --method count &&
python main.py --show_eval --plot --threshold 30 --dataset 20ng --method count