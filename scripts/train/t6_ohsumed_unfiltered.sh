#!/bin/bash
#SBATCH --job-name=t6_ohsumed
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/t6_ohsumed.%j.out
#SBATCH --partition=Kalahari

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --threshold 6 --dataset ohsumed --plot --method count --version unfiltered &&
python main.py --threshold 6 --dataset ohsumed --plot --method count --version unfiltered &&
python main.py --threshold 6 --dataset ohsumed --plot --method count --version unfiltered &&
python main.py --threshold 6 --dataset ohsumed --plot --method idf --version unfiltered &&
python main.py --threshold 6 --dataset ohsumed --plot --method idf --version unfiltered &&
python main.py --threshold 6 --dataset ohsumed --plot --method idf --version unfiltered &&
python main.py --threshold 6 --dataset ohsumed --plot --method idf_wiki --version unfiltered &&
python main.py --threshold 6 --dataset ohsumed --plot --method idf_wiki --version unfiltered &&
python main.py --threshold 6 --dataset ohsumed --plot --method idf_wiki --version unfiltered &&
python main.py --threshold 6 --dataset ohsumed --plot --method count_norm --version unfiltered &&
python main.py --threshold 6 --dataset ohsumed --plot --method count_norm --version unfiltered &&
python main.py --threshold 6 --dataset ohsumed --plot --method count_norm --version unfiltered &&
python main.py --threshold 6 --dataset ohsumed --plot --method count_norm_pmi --version unfiltered &&
python main.py --threshold 6 --dataset ohsumed --plot --method count_norm_pmi --version unfiltered &&
python main.py --threshold 6 --dataset ohsumed --plot --method count_norm_pmi --version unfiltered &&
python main.py --threshold 6 --dataset ohsumed --plot --method idf_norm --version unfiltered &&
python main.py --threshold 6 --dataset ohsumed --plot --method idf_norm --version unfiltered &&
python main.py --threshold 6 --dataset ohsumed --plot --method idf_norm --version unfiltered &&
python main.py --threshold 6 --dataset ohsumed --plot --method idf_wiki_norm --version unfiltered &&
python main.py --threshold 6 --dataset ohsumed --plot --method idf_wiki_norm --version unfiltered &&
python main.py --threshold 6 --dataset ohsumed --plot --method idf_wiki_norm --version unfiltered &&
python main.py --threshold 6 --dataset ohsumed --plot --method idf_norm_pmi --version unfiltered &&
python main.py --threshold 6 --dataset ohsumed --plot --method idf_norm_pmi --version unfiltered &&
python main.py --threshold 6 --dataset ohsumed --plot --method idf_norm_pmi --version unfiltered &&
python main.py --threshold 6 --dataset ohsumed --plot --method idf_wiki_norm_pmi --version unfiltered &&
python main.py --threshold 6 --dataset ohsumed --plot --method idf_wiki_norm_pmi --version unfiltered &&
python main.py --threshold 6 --dataset ohsumed --plot --method idf_wiki_norm_pmi --version unfiltered