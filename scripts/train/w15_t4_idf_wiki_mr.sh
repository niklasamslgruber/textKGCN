#!/bin/bash
#SBATCH --job-name=w15_t4_idf_wiki_mr
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/w15_t4_idf_wiki_mr.%j.out
#SBATCH --partition=All

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --word_window_size 15 --threshold 4 --dataset mr --method idf_wiki &&
python main.py --show_eval --plot --word_window_size 15 --threshold 4 --dataset mr --method idf_wiki &&
python main.py --show_eval --plot --word_window_size 15 --threshold 4 --dataset mr --method idf_wiki