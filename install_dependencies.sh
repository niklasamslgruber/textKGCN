#!/bin/bash
pip install torch==1.6.0+cpu torchvision==0.7.0+cpu
pip install klepto==0.1.9
pip install pytz
pip install sklearn
pip install pandas
pip install matplotlib
pip install torch-scatter==2.0.5+cpu -f https://pytorch-geometric.com/whl/torch-1.6.0.html
pip install torch-sparse==0.6.7+cpu -f https://pytorch-geometric.com/whl/torch-1.6.0.html
pip install torch-cluster==1.5.7+cpu -f https://pytorch-geometric.com/whl/torch-1.6.0.html
pip install torch-spline-conv==1.2.0+cpu -f https://pytorch-geometric.com/whl/torch-1.6.0.html
pip install torch-geometric
pip install spacy
python -m spacy download en

echo "Successfully installed all dependencies. You are now ready to run textKGCN"
