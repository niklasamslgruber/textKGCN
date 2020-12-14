#!/bin/bash
#SBATCH --job-name=t20_idf_norm_20ng
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/t20_idf_norm_20ng.%j.out
#SBATCH --partition=Kalahari

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --threshold 20 --dataset 20ng --method idf_norm &&
python main.py --show_eval --plot --threshold 20 --dataset 20ng --method idf_norm