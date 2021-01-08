#!/bin/bash
#SBATCH --job-name=no_wiki_r52
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/no_wiki_r52.%j.out
#SBATCH --partition=Gobi

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --no_wiki --plot --dataset r52 --version unfiltered &&
python main.py --no_wiki --plot --dataset r52 --version unfiltered &&
python main.py --no_wiki --plot --dataset r52 --version unfiltered