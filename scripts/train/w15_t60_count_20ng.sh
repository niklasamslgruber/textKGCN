#!/bin/bash
#SBATCH --job-name=w15_t60_count_20ng
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/w15_t60_count_20ng.%j.out
#SBATCH --partition=Luna

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --word_window_size 15 --threshold 60 --dataset 20ng --method count &&
python main.py --show_eval --plot --word_window_size 15 --threshold 60 --dataset 20ng --method count &&
python main.py --show_eval --plot --word_window_size 15 --threshold 60 --dataset 20ng --method count