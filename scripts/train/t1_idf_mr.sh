#!/bin/bash
#SBATCH --job-name=t1_idf_mr
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/t1_idf_mr.%j.out
#SBATCH --partition=Kalahari

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --threshold 1 --dataset mr --method idf &&
python main.py --show_eval --plot --threshold 1 --dataset mr --method idf