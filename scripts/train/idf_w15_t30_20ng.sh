#!/bin/bash
#SBATCH --job-name=idf_w15_t30_20ng
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/idf_w15_t30_20ng.%j.out
#SBATCH --partition=All

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --word_window_size 15 --threshold 30 --dataset 20ng &&
python main.py --show_eval --plot --word_window_size 15 --threshold 30 --dataset 20ng &&
python main.py --show_eval --plot --word_window_size 15 --threshold 30 --dataset 20ng