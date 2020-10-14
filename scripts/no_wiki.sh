#!/bin/bash
#
#SBATCH --job-name=no_wiki
#SBATCH --comment="Trains a PyTorch model for a bachelor thesis"
#SBATCH --mail-type=ALL
#SBATCH --mail-user="niklas.amslgruber@campus.lmu.de"
#SBATCH --ntasks=1
#SBATCH --output=out/no-wiki.%j.out
#SBATCH --partition=All

source ~/miniconda3/bin/activate thesis

cd ~/Desktop/textKGCN
python main.py --show_eval --plot --no_wiki
