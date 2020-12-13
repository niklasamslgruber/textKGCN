#!/bin/bash
#SBATCH --job-name=t4_idf_norm_pmi_mr
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/t4_idf_norm_pmi_mr.%j.out
#SBATCH --partition=Sibirien

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --threshold 4 --dataset mr --method idf_norm_pmi &&
python main.py --show_eval --plot --threshold 4 --dataset mr --method idf_norm_pmi