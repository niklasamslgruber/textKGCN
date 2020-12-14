#!/bin/bash
#SBATCH --job-name=t7_idf_wiki_norm_ohsumed
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/t7_idf_wiki_norm_ohsumed.%j.out
#SBATCH --partition=Antarktis

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --threshold 7 --dataset ohsumed --method idf_wiki_norm &&
python main.py --show_eval --plot --threshold 7 --dataset ohsumed --method idf_wiki_norm