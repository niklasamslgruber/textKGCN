#!/bin/bash
#SBATCH --job-name=t4_mr
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/t4_mr.%j.out
#SBATCH --partition=All

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --threshold 5 --dataset mr --method count &&
python main.py --threshold 5 --dataset mr --method idf &&
python main.py --threshold 5 --dataset mr --method idf_wiki &&
python main.py --threshold 5 --dataset mr --method count_norm &&
python main.py --threshold 5 --dataset mr --method count_norm_pmi &&
python main.py --threshold 5 --dataset mr --method idf_norm &&
python main.py --threshold 5 --dataset mr --method idf_wiki_norm &&
python main.py --threshold 5 --dataset mr --method idf_norm_pmi &&
python main.py --threshold 5 --dataset mr --method idf_wiki_norm_pmi