#!/bin/bash
#SBATCH --job-name=t3_r52
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/t3_r52.%j.out
#SBATCH --partition=Antarktis

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --threshold 3 --dataset r52 --plot --method idf_norm --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_norm --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_norm --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_norm --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_norm --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_norm --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_norm --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_norm --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_wiki_norm --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_wiki_norm --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_wiki_norm --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_wiki_norm --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_wiki_norm --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_wiki_norm --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_wiki_norm --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_wiki_norm --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_wiki_norm --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_wiki_norm --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_norm_pmi --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_norm_pmi --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_norm_pmi --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_norm_pmi --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_norm_pmi --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_norm_pmi --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_norm_pmi --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_norm_pmi --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_norm_pmi --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_norm_pmi --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_wiki_norm_pmi --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_wiki_norm_pmi --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_wiki_norm_pmi --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_wiki_norm_pmi --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_wiki_norm_pmi --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_wiki_norm_pmi --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_wiki_norm_pmi --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_wiki_norm_pmi --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_wiki_norm_pmi --version filtered &&
python main.py --threshold 3 --dataset r52 --plot --method idf_wiki_norm_pmi --version filtered