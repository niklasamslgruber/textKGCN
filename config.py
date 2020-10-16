import argparse
import torch
from helper.utils import get_host, get_user

parser = argparse.ArgumentParser()

"""
Arguments
"""
# Evaluation output
parser.add_argument('--show_eval', default=False, action='store_true', help="show evaluation metrics")

# Plotting
parser.add_argument('--plot', default=False, action='store_true', help="save model output as plots")

# Sampling
word_window_size = 15
parser.add_argument('--word_window_size', default=word_window_size, type=int, help=f"set window size (default: {word_window_size})", metavar='')

# Edge Weights
parser.add_argument('--use_edge_weights', default=True, action='store_true', help="use edge weights for model")

# doc2doc edges weight
parser.add_argument('--raw_count', default=False, action='store_true', help="use number of relations as doc2doc weight instead of idf")

# relation threshold
relation_count_threshold = 2
parser.add_argument('--threshold', default=relation_count_threshold, type=int, help=f"set filter threshold for doc2doc edges (default: {relation_count_threshold})", metavar='')

# debug
debug = False
parser.add_argument('--debug', default=debug, action='store_true', help="use edge weights for model")

# wikidata usage
parser.add_argument('--no_wiki', default=False, action='store_true', help="disable doc2doc edges")

# dataset
available_datasets = ["r8_presplit", "r8_small", "ag_presplit", "20ng_presplit", "mr_presplit", "ohsumed_presplit", "r52_presplit"]
parser.add_argument('--dataset', default=available_datasets[2], type=str, help=f"select dataset ({', '.join(available_datasets)})", metavar='')


# Set FLAGS from command line
FLAGS = parser.parse_args()
assert FLAGS.dataset in available_datasets, "Dataset not available"

""" 
Dataset
"""

if 'ag' in FLAGS.dataset:
    num_labels = 4
elif 'r8' in FLAGS.dataset:
    num_labels = 8

FLAGS.use_wikidata = not FLAGS.no_wiki
FLAGS.use_cache = False

"""
Model
"""
pred_type = 'softmax'
node_embd_type = 'gcn'
layer_dim_list = [200, num_labels]  # Layer dimensions, (0): 200, (1): 4
num_layers = len(layer_dim_list)  # 2 Layers
class_weights = True
dropout = True
s = 'textKGCN:pred_type={},node_embd_type={},num_layers={},layer_dim_list={},act={},' \
        'dropout={},class_weights={}'.format(
        pred_type, node_embd_type, num_layers, "_".join([str(i) for i in layer_dim_list]), 'relu', dropout, class_weights)

model_params = {
    'dataset': FLAGS.dataset,
    'wiki_enabled': FLAGS.use_wikidata,
    'pred_type': pred_type,
    'node_embd':  node_embd_type,
    'layer_dims': layer_dim_list,
    'class_weights': class_weights,
    'dropout': dropout
}

print("{}: {}\n".format("textKGCN", model_params))
FLAGS.model = s


"""
Validation
"""
FLAGS.use_best_val_model_for_inference = True
FLAGS.validation_window_size = FLAGS.word_window_size
FLAGS.validation_metric = 'accuracy'  # Choices: ["f1_weighted", "accuracy", "loss"]


"""
Evaluation
"""
FLAGS.tvt_ratio = [0.8, 0.1, 0.1]
FLAGS.tvt_list = ["train", "test", "val"]


"""
Optimization
"""
FLAGS.lr = 2e-2
FLAGS.random_seed = 3
FLAGS.num_epochs = 2 if FLAGS.debug else 400


"""
Other
"""
FLAGS.user = get_user()
FLAGS.hostname = get_host()

gpu = 0
FLAGS.device = str('cuda:{}'.format(gpu) if torch.cuda.is_available() else 'cpu')
