#!/bin/bash
#SBATCH --job-name=w15_t8_count_r52
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/w15_t8_count_r52.%j.out
#SBATCH --partition=Kalahari

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --word_window_size 15 --threshold 8 --dataset r52 --method count &&
python main.py --show_eval --plot --word_window_size 15 --threshold 8 --dataset r52 --method count