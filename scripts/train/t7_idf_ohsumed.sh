#!/bin/bash
#SBATCH --job-name=t7_idf_ohsumed
#SBATCH --comment='Train model'
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'
#SBATCH --ntasks=1
#SBATCH --output=out/t7_idf_ohsumed.%j.out
#SBATCH --partition=Kalahari

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --threshold 7 --dataset ohsumed --method idf &&
python main.py --show_eval --plot --threshold 7 --dataset ohsumed --method idf