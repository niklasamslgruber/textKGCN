#!/bin/bash
#SBATCH --job-name=t8_idf_wiki_r52
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/t8_idf_wiki_r52.%j.out
#SBATCH --partition=Gobi

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --threshold 8 --dataset r52 --method idf_wiki &&
python main.py --show_eval --plot --threshold 8 --dataset r52 --method idf_wiki