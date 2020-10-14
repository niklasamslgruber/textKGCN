#!/bin/bash
#
#SBATCH --job-name=raw20-3
#SBATCH --comment="Trains a PyTorch model for a bachelor thesis"
#SBATCH --mail-type=ALL
#SBATCH --mail-user="niklas.amslgruber@campus.lmu.de"
#SBATCH --ntasks=1
#SBATCH --output=out/raw20-3.%j.out
#SBATCH --begin 20:00
#SBATCH --partition=All

source ~/miniconda3/bin/activate thesis

cd textKGCN
python main.py --show_eval --plot --raw_count --word_window_size 20 --threshold 3
