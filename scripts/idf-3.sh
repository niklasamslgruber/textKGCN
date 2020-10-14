#!/bin/bash
#
#SBATCH --job-name=idf-3
#SBATCH --comment="Trains a PyTorch model for a bachelor thesis"
#SBATCH --mail-type=ALL
#SBATCH --mail-user="niklas.amslgruber@campus.lmu.de"
#SBATCH --ntasks=1
#SBATCH --output=out/idf-3.%j.out
#SBATCH --begin 20:08
#SBATCH --partition=All

source ~/miniconda3/bin/activate thesis

cd textKGCN
python main.py --show_eval --plot --threshold 3
