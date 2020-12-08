#!/bin/bash
#SBATCH --job-name=t16_idf_wiki_ohsumed
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/t16_idf_wiki_ohsumed.%j.out
#SBATCH --partition=Luna

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --threshold 16 --dataset ohsumed --method idf_wiki &&
python main.py --show_eval --plot --threshold 16 --dataset ohsumed --method idf_wiki