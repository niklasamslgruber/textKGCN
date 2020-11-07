#!/bin/bash
#SBATCH --job-name=no_wiki_w15_ohsumed
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/no_wiki_w15_ohsumed.%j.out
#SBATCH --partition=Sibirien

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --no_wiki --dataset ohsumed --word_window_size 15 &&
python main.py --no_wiki --dataset ohsumed --word_window_size 15 &&
python main.py --no_wiki --dataset ohsumed --word_window_size 15