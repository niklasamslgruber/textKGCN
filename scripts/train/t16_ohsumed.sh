#!/bin/bash
#SBATCH --job-name=t16_ohsumed
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/t16_ohsumed.%j.out
#SBATCH --partition=Gobi

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --threshold 16 --dataset ohsumed --plot --method idf_norm_pmi &&
python main.py --threshold 16 --dataset ohsumed --plot --method idf_norm_pmi &&
python main.py --threshold 16 --dataset ohsumed --plot --method idf_norm_pmi &&
python main.py --threshold 16 --dataset ohsumed --plot --method idf_wiki_norm_pmi &&
python main.py --threshold 16 --dataset ohsumed --plot --method idf_wiki_norm_pmi &&
python main.py --threshold 16 --dataset ohsumed --plot --method idf_wiki_norm_pmi &&
python main.py --threshold 16 --dataset ohsumed --plot --method idf_wiki_norm_pmi &&
python main.py --threshold 16 --dataset ohsumed --plot --method idf_wiki_norm_pmi