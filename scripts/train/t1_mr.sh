#!/bin/bash
#SBATCH --job-name=no_wiki_mr
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/no_wiki_mr.%j.out
#SBATCH --partition=All

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --threshold 1 --dataset mr --method count &&
python main.py --threshold 1 --dataset mr --method idf &&
python main.py --threshold 1 --dataset mr --method idf_wiki &&
python main.py --threshold 1 --dataset mr --method count_norm &&
python main.py --threshold 1 --dataset mr --method count_norm_pmi &&
python main.py --threshold 1 --dataset mr --method idf_norm &&
python main.py --threshold 1 --dataset mr --method idf_wiki_norm &&
python main.py --threshold 1 --dataset mr --method idf_norm_pmi &&
python main.py --threshold 1 --dataset mr --method idf_wiki_norm_pmi