#!/bin/bash
#SBATCH --job-name=t19_idf_wiki_norm_pmi_ohsumed
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/t19_idf_wiki_norm_pmi_ohsumed.%j.out
#SBATCH --partition=Gobi

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --threshold 19 --dataset ohsumed --method idf_wiki_norm_pmi &&
python main.py --show_eval --plot --threshold 19 --dataset ohsumed --method idf_wiki_norm_pmi