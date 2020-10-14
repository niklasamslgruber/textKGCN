#!/bin/bash
#
#SBATCH --job-name=no_wiki20
#SBATCH --comment="Trains a PyTorch model for a bachelor thesis"
#SBATCH --mail-type=ALL
#SBATCH --mail-user="niklas.amslgruber@campus.lmu.de"
#SBATCH --ntasks=1
#SBATCH --output=out/no-wiki20.%j.out
#SBATCH --begin 20:00
#SBATCH --partition=All

source ~/miniconda3/bin/activate thesis

cd textKGCN
python main.py --show_eval --plot --no_wiki --word_window_size 20