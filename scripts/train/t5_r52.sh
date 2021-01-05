#!/bin/bash
#SBATCH --job-name=t5_r52
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/t5_r52.%j.out
#SBATCH --partition=Sibirien

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --threshold 5 --dataset r52 --plot --method count &&
python main.py --threshold 5 --dataset r52 --plot --method count &&
python main.py --threshold 5 --dataset r52 --plot --method count &&
python main.py --threshold 5 --dataset r52 --plot --method count &&
python main.py --threshold 5 --dataset r52 --plot --method count &&
python main.py --threshold 5 --dataset r52 --plot --method count &&
python main.py --threshold 5 --dataset r52 --plot --method count &&
python main.py --threshold 5 --dataset r52 --plot --method count &&
python main.py --threshold 5 --dataset r52 --plot --method count &&
python main.py --threshold 5 --dataset r52 --plot --method count &&
python main.py --threshold 5 --dataset r52 --plot --method idf &&
python main.py --threshold 5 --dataset r52 --plot --method idf &&
python main.py --threshold 5 --dataset r52 --plot --method idf &&
python main.py --threshold 5 --dataset r52 --plot --method idf &&
python main.py --threshold 5 --dataset r52 --plot --method idf &&
python main.py --threshold 5 --dataset r52 --plot --method idf &&
python main.py --threshold 5 --dataset r52 --plot --method idf &&
python main.py --threshold 5 --dataset r52 --plot --method idf &&
python main.py --threshold 5 --dataset r52 --plot --method idf &&
python main.py --threshold 5 --dataset r52 --plot --method idf &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki &&
python main.py --threshold 5 --dataset r52 --plot --method count_norm &&
python main.py --threshold 5 --dataset r52 --plot --method count_norm &&
python main.py --threshold 5 --dataset r52 --plot --method count_norm &&
python main.py --threshold 5 --dataset r52 --plot --method count_norm &&
python main.py --threshold 5 --dataset r52 --plot --method count_norm &&
python main.py --threshold 5 --dataset r52 --plot --method count_norm &&
python main.py --threshold 5 --dataset r52 --plot --method count_norm &&
python main.py --threshold 5 --dataset r52 --plot --method count_norm &&
python main.py --threshold 5 --dataset r52 --plot --method count_norm &&
python main.py --threshold 5 --dataset r52 --plot --method count_norm &&
python main.py --threshold 5 --dataset r52 --plot --method count_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method count_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method count_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method count_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method count_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method count_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method count_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method count_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method count_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method count_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method idf_norm &&
python main.py --threshold 5 --dataset r52 --plot --method idf_norm &&
python main.py --threshold 5 --dataset r52 --plot --method idf_norm &&
python main.py --threshold 5 --dataset r52 --plot --method idf_norm &&
python main.py --threshold 5 --dataset r52 --plot --method idf_norm &&
python main.py --threshold 5 --dataset r52 --plot --method idf_norm &&
python main.py --threshold 5 --dataset r52 --plot --method idf_norm &&
python main.py --threshold 5 --dataset r52 --plot --method idf_norm &&
python main.py --threshold 5 --dataset r52 --plot --method idf_norm &&
python main.py --threshold 5 --dataset r52 --plot --method idf_norm &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki_norm &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki_norm &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki_norm &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki_norm &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki_norm &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki_norm &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki_norm &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki_norm &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki_norm &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki_norm &&
python main.py --threshold 5 --dataset r52 --plot --method idf_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method idf_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method idf_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method idf_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method idf_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method idf_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method idf_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method idf_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method idf_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method idf_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki_norm_pmi &&
python main.py --threshold 5 --dataset r52 --plot --method idf_wiki_norm_pmi