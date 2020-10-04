# textKGCN 
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Licsense: MIT](https://img.shields.io/static/v1?label=Python&message=3.6&color=blue)](https://opensource.org/licenses/MIT)

This repository extends [Ken Gu's](https://github.com/codeKgu/Text-GCN) PyTorch implementation of "Graph Convolutional Networks for Text Classification." ([AAAI 2019](https://arxiv.org/abs/1809.05679)) by integrating knowledge graphs into the word document graph.

### Running the project
 ```
$ python main.py
```

###### Optional Arguments:
* `--show_eval`: Prints all evaluation metrics to the console
* `--plot`: Saves the GCN embeddings as a 2D t-SNE plot
* `--word-window-size`: Specifies the window size used for the model (default: 10)
* `--use_edge_weights`: Defines wether edge weights should be used 

Other configuration options can be set in `config.py`.

### Dependencies
The code runs with `Python 3.6`.
All dependencies can be installed automatically with this command (tested on `macOS` only): 
 ```
 sh install_dependencies.sh
```
###### Note: The script requires `python3.6` and `pip` installed. It is recommended to install all dependencies into a separate Python environment.

These dependencies will be installed:
* `torch==1.6.0`
* `torchvision==0.7.0`
* `torch-cluster==1.5.7`
* `torch-scatter==2.0.5`
* `torch-sparse==0.6.7`
* `torch-spline-conv==1.2.0`
* `torch-geometric==1.6.1`
* `klepto==0.1.9`
* `sklearn`, `matplotlib`, `pytz`, `pandas`

### Base Paper
> Graph Convolutional Networks for Text Classification. 
> Liang Yao, Chengsheng Mao, Yuan Luo.
> AAAI, 2019. [\(Paper\)](https://arxiv.org/abs/1809.05679)


