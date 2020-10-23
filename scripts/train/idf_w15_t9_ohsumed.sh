#!/bin/bash
#SBATCH --job-name=idf_w15_t9_ohsumed
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/idf_w15_t9_ohsumed.%j.out
#SBATCH --partition=All

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --word_window_size 15 --threshold 9 --dataset ohsumed &&
python main.py --show_eval --plot --word_window_size 15 --threshold 9 --dataset ohsumed &&
python main.py --show_eval --plot --word_window_size 15 --threshold 9 --dataset ohsumed