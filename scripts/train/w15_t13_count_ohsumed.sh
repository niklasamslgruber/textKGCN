#!/bin/bash
#SBATCH --job-name=w15_t13_count_ohsumed
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/w15_t13_count_ohsumed.%j.out
#SBATCH --partition=Luna

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --word_window_size 15 --threshold 13 --dataset ohsumed --method count &&
python main.py --show_eval --plot --word_window_size 15 --threshold 13 --dataset ohsumed --method count &&
python main.py --show_eval --plot --word_window_size 15 --threshold 13 --dataset ohsumed --method count