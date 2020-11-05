#!/bin/bash
#SBATCH --job-name=w15_t18_idf_wiki_r8
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/w15_t18_idf_wiki_r8.%j.out
#SBATCH --partition=All

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --word_window_size 15 --threshold 18 --dataset r8 --method idf_wiki &&
python main.py --show_eval --plot --word_window_size 15 --threshold 18 --dataset r8 --method idf_wiki &&
python main.py --show_eval --plot --word_window_size 15 --threshold 18 --dataset r8 --method idf_wiki