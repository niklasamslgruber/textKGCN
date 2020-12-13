#!/bin/bash
#SBATCH --job-name=t5_idf_wiki_r8
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/t5_idf_wiki_r8.%j.out
#SBATCH --partition=Sibirien

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --threshold 5 --dataset r8 --method idf_wiki &&
python main.py --show_eval --plot --threshold 5 --dataset r8 --method idf_wiki