from utils import get_host, get_user
import argparse
import torch

parser = argparse.ArgumentParser()

"""
Arguments
"""
# Evaluation output
parser.add_argument('--show_eval', default=False, action='store_true', help="show evaluation metrics")

# Plotting
parser.add_argument('--plot', default=False, action='store_true', help="save model output as plots")

# Sampling
word_window_size = 10
parser.add_argument('--word_window_size', default=word_window_size, type=int, help=f"set window size (default: {word_window_size})", metavar='')

# Edge Weights
parser.add_argument('--use_edge_weights', default=False, action='store_true', help="use edge weights for model")

# Set FLAGS from command line
FLAGS = parser.parse_args()


""" 
Dataset
"""
# dataset = 'twitter_asian_prejudice'
# dataset = 'twitter_asian_prejudice_sentiment'
# dataset = 'r8_presplit'
# dataset = 'ag_presplit'
dataset = 'twitter_asian_prejudice_small'

if 'twitter_asian_prejudice' in dataset:
    if 'sentiment' in dataset:
        num_labels = 2
    else:
        num_labels = 4
elif 'ag' in dataset:
    num_labels = 4
elif 'r8' in dataset:
    num_labels = 8

FLAGS.dataset = dataset


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
FLAGS.validation_window_size = 10
FLAGS.validation_metric = 'accuracy'  # Choices: ["f1_weighted", "accuracy", "loss"]


"""
Evaluation
"""
FLAGS.tvt_ratio = [0.8, 0.1, 0.1]
FLAGS.tvt_list = ["train", "test", "val"]


"""
Optimization
"""
debug = False
FLAGS.lr = 2e-2
FLAGS.random_seed = 3
FLAGS.num_epochs = 2 if debug else 400


"""
Other
"""
FLAGS.user = get_user()
FLAGS.hostname = get_host()

gpu = -1
FLAGS.device = str('cuda:{}'.format(gpu) if torch.cuda.is_available() and gpu != -1 else 'cpu')
