#!/bin/bash
#SBATCH --job-name=t60_idf_20ng
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/t60_idf_20ng.%j.out
#SBATCH --partition=Kalahari

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --threshold 60 --dataset 20ng --method idf &&
python main.py --show_eval --plot --threshold 60 --dataset 20ng --method idf