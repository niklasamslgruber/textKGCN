#!/bin/bash
#SBATCH --job-name=w15_t4_count_r8
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/w15_t4_count_r8.%j.out
#SBATCH --partition=Luna

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --word_window_size 15 --threshold 4 --dataset r8 --method count &&
python main.py --show_eval --plot --word_window_size 15 --threshold 4 --dataset r8 --method count