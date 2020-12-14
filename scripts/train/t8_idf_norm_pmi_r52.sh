#!/bin/bash
#SBATCH --job-name=t8_idf_norm_pmi_r52
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/t8_idf_norm_pmi_r52.%j.out
#SBATCH --partition=All

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --threshold 8 --dataset r52 --method idf_norm_pmi &&
python main.py --show_eval --plot --threshold 8 --dataset r52 --method idf_norm_pmi