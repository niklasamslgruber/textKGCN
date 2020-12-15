#!/bin/bash
#SBATCH --job-name=no_wiki_20ng
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/no_wiki_20ng.%j.out
#SBATCH --partition=Sibirien

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --no_wiki --dataset 20ng &&
python main.py --no_wiki --dataset 20ng &&
python main.py --no_wiki --dataset 20ng &&
python main.py --no_wiki --dataset 20ng &&
python main.py --no_wiki --dataset 20ng