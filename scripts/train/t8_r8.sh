#!/bin/bash
#SBATCH --job-name=t7_r8
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/t7_r8.%j.out
#SBATCH --partition=All

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --threshold 8 --dataset r8 --method count &&
python main.py --threshold 8 --dataset r8 --method idf &&
python main.py --threshold 8 --dataset r8 --method idf_wiki &&
python main.py --threshold 8 --dataset r8 --method count_norm &&
python main.py --threshold 8 --dataset r8 --method count_norm_pmi &&
python main.py --threshold 8 --dataset r8 --method idf_norm &&
python main.py --threshold 8 --dataset r8 --method idf_wiki_norm &&
python main.py --threshold 8 --dataset r8 --method idf_norm_pmi &&
python main.py --threshold 8 --dataset r8 --method idf_wiki_norm_pmi