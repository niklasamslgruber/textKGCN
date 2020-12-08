#!/bin/bash
#SBATCH --job-name=t4_count_mr
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/t4_count_mr.%j.out
#SBATCH --partition=Gobi

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --threshold 4 --dataset mr --method count &&
python main.py --show_eval --plot --threshold 4 --dataset mr --method count