#!/bin/bash
#SBATCH --job-name=raw_w15_t50_20ng
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/raw_w15_t50_20ng.%j.out
#SBATCH --partition=All

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --word_window_size 15 --threshold 50 --dataset 20ng --raw_count &&
python main.py --show_eval --plot --word_window_size 15 --threshold 50 --dataset 20ng --raw_count &&
python main.py --show_eval --plot --word_window_size 15 --threshold 50 --dataset 20ng --raw_count