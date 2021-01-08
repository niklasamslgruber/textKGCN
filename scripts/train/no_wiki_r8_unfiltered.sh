#!/bin/bash
#SBATCH --job-name=no_wiki_r8
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/no_wiki_r8.%j.out
#SBATCH --partition=Kalahari

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --no_wiki --plot --dataset r8 --version unfiltered &&
python main.py --no_wiki --plot --dataset r8 --version unfiltered &&
python main.py --no_wiki --plot --dataset r8 --version unfiltered