#!/bin/bash
#SBATCH --job-name=no_wiki_w15_r52
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/no_wiki_w15_r52.%j.out
#SBATCH --partition=All

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --no_wiki --dataset r52 --word_window_size 15 &&
python main.py --no_wiki --dataset r52 --word_window_size 15 &&
python main.py --no_wiki --dataset r52 --word_window_size 15