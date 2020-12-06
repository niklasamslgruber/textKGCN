#!/bin/bash
#SBATCH --job-name=w15_t16_count_ohsumed
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/w15_t16_count_ohsumed.%j.out
#SBATCH --partition=Sibirien

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --word_window_size 15 --threshold 16 --dataset ohsumed --method count &&
python main.py --show_eval --plot --word_window_size 15 --threshold 16 --dataset ohsumed --method count