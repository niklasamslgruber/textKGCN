#!/bin/bash
#SBATCH --job-name=t13_ohsumed
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/t13_ohsumed.%j.out
#SBATCH --partition=Sibirien

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --threshold 13 --dataset ohsumed --plot --method count &&
python main.py --threshold 13 --dataset ohsumed --plot --method idf &&
python main.py --threshold 13 --dataset ohsumed --plot --method idf_wiki &&
python main.py --threshold 13 --dataset ohsumed --plot --method count_norm &&
python main.py --threshold 13 --dataset ohsumed --plot --method count_norm_pmi &&
python main.py --threshold 13 --dataset ohsumed --plot --method idf_norm &&
python main.py --threshold 13 --dataset ohsumed --plot --method idf_wiki_norm &&
python main.py --threshold 13 --dataset ohsumed --plot --method idf_norm_pmi &&
python main.py --threshold 13 --dataset ohsumed --plot --method idf_wiki_norm_pmi