#!/bin/bash
#SBATCH --job-name=no_wiki_w15_r8
#SBATCH --comment='Train model'
#SBATCH --mail-type=ALL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/no_wiki_w15_r8.%j.out
#SBATCH --partition=All

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --no_wiki --dataset r8 --word_window_size 15 &&
python main.py --no_wiki --dataset r8 --word_window_size 15 &&
python main.py --no_wiki --dataset r8 --word_window_size 15