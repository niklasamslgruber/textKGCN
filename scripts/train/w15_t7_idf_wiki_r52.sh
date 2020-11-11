#!/bin/bash
#SBATCH --job-name=w15_t7_idf_wiki_r52
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/w15_t7_idf_wiki_r52.%j.out
#SBATCH --partition=Antarktis

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --word_window_size 15 --threshold 7 --dataset r52 --method idf_wiki &&
python main.py --show_eval --plot --word_window_size 15 --threshold 7 --dataset r52 --method idf_wiki &&
python main.py --show_eval --plot --word_window_size 15 --threshold 7 --dataset r52 --method idf_wiki