# textKGCN 
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Licsense: MIT](https://img.shields.io/static/v1?label=Python&message=3.6&color=blue)](https://opensource.org/licenses/MIT)

This repository extends [Ken Gu's](https://github.com/codeKgu/Text-GCN) PyTorch implementation of "Graph Convolutional Networks for Text Classification." ([AAAI 2019](https://arxiv.org/abs/1809.05679)) by integrating knowledge graphs into the word document graph.

### Dependencies
The code runs with `Python 3.6` and uses different dependency version than the base implementation.
 
* `torch==1.6.0`
* `torchvision==0.7.0`
* `torch-cluster==1.5.7`
* `torch-scatter==2.0.5`
* `torch-sparse==0.6.7`
* `torch-spline-conv==1.2.0`
* `torch-geometric==1.6.1`
* `klepto==0.1.9`

 It is recommended to install all dependencies in a separate Anaconda environment.

### Running the project
 ```
$ python main.py
```

### Base Paper
> Graph Convolutional Networks for Text Classification. 
> Liang Yao, Chengsheng Mao, Yuan Luo.
> AAAI, 2019. [\(Paper\)](https://arxiv.org/abs/1809.05679)


