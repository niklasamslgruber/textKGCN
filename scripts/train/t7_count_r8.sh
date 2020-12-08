#!/bin/bash
#SBATCH --job-name=t7_count_r8
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/t7_count_r8.%j.out
#SBATCH --partition=Gobi

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --threshold 7 --dataset r8 --method count &&
python main.py --show_eval --plot --threshold 7 --dataset r8 --method count