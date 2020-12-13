#!/bin/bash
#SBATCH --job-name=t9_count_r52
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/t9_count_r52.%j.out
#SBATCH --partition=Luna

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --threshold 9 --dataset r52 --method count &&
python main.py --show_eval --plot --threshold 9 --dataset r52 --method count