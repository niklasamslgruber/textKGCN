#!/bin/bash
#SBATCH --job-name=idf_w15_t5_r52
#SBATCH --comment='Train model'
#SBATCH --mail-type=ALL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/idf_w15_t5_r52.%j.out
#SBATCH --partition=All

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --word_window_size 15 --threshold 5 --dataset r52 &&
python main.py --show_eval --plot --word_window_size 15 --threshold 5 --dataset r52 &&
python main.py --show_eval --plot --word_window_size 15 --threshold 5 --dataset r52