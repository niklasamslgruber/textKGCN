#!/bin/bash
#SBATCH --job-name=no_wiki_ohsumed
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/no_wiki_ohsumed.%j.out
#SBATCH --partition=Antarktis

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --no_wiki --plot --dataset ohsumed --version unfiltered &&
python main.py --no_wiki --plot --dataset ohsumed --version unfiltered &&
python main.py --no_wiki --plot --dataset ohsumed --version unfiltered