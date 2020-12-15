#!/bin/bash
#SBATCH --job-name=t40_20ng
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/t40_20ng.%j.out
#SBATCH --partition=Antarktis

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --threshold 50 --dataset 20ng --method count &&
python main.py --threshold 50 --dataset 20ng --method idf &&
python main.py --threshold 50 --dataset 20ng --method idf_wiki &&
python main.py --threshold 50 --dataset 20ng --method count_norm &&
python main.py --threshold 50 --dataset 20ng --method count_norm_pmi &&
python main.py --threshold 50 --dataset 20ng --method idf_norm &&
python main.py --threshold 50 --dataset 20ng --method idf_wiki_norm &&
python main.py --threshold 50 --dataset 20ng --method idf_norm_pmi &&
python main.py --threshold 50 --dataset 20ng --method idf_wiki_norm_pmi