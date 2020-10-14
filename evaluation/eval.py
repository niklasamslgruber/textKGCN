import numpy as np
from sklearn import metrics
import pandas as pd
from config import FLAGS
from helper import file_utils as file, io_utils as io


def eval(preds, dataset, use_wikidata, test=False, save=False):
    y_true = dataset.label_inds[dataset.node_ids]
    y_pred_label = np.asarray([np.argmax(pred) for pred in preds])
    accuracy = metrics.accuracy_score(y_true, y_pred_label)
    f1_weighted = metrics.f1_score(y_true, y_pred_label, average='weighted')
    f1_macro = metrics.f1_score(y_true, y_pred_label, average='macro')
    f1_micro = metrics.f1_score(y_true, y_pred_label, average='micro')
    precision_weighted = metrics.precision_score(y_true, y_pred_label, average='weighted')
    precision_macro = metrics.precision_score(y_true, y_pred_label, average='macro')
    precision_micro = metrics.precision_score(y_true, y_pred_label, average='micro')
    recall_weighted = metrics.recall_score(y_true, y_pred_label, average='weighted')
    recall_macro = metrics.recall_score(y_true, y_pred_label, average='macro')
    recall_micro = metrics.recall_score(y_true, y_pred_label, average='micro')
    results = {"time": io.get_ts(),
               "wiki_enabled": use_wikidata,
               "window_size": FLAGS.word_window_size,
               "raw_count": FLAGS.raw_count,
               "threshold": FLAGS.relation_count_threshold,
               "accuracy": accuracy,
               "f1_weighted": f1_weighted,
               "f1_macro": f1_macro,
               "f1_micro": f1_micro,
               "precision_weighted": precision_weighted,
               "precision_macro": precision_macro,
               "precision_micro": precision_micro,
               "recall_weighted": recall_weighted,
               "recall_macro": recall_macro,
               "recall_micro": recall_micro
               }

    if save:
        save_metrics(results)

    if test:
        one_hot_true = np.zeros((y_true.size, len(dataset.label_dict)))
        one_hot_true[np.arange(y_true.size), y_true] = 1
        results["y_true"] = one_hot_true
        one_hot_pred = np.zeros((y_true.size, len(dataset.label_dict)))
        one_hot_pred[np.arange(y_pred_label.size), y_pred_label] = 1
        results["y_pred"] = one_hot_pred
    return results


def save_metrics(results):
    dataframe = pd.DataFrame.from_dict([results])
    existing_logs = file.get_eval_logs()
    if existing_logs is not None:
        dataframe = pd.concat([existing_logs, dataframe])
    file.save_eval_logs(dataframe)
    file.save_result_log(results)


class MovingAverage(object):
    def __init__(self, window, want_increase=True):
        self.moving_avg = [float('-inf')] if want_increase else [float('inf')]
        self.want_increase = want_increase
        self.results = []
        self.window = window

    def add_to_moving_avg(self, x):
        self.results.append(x)
        if len(self.results) >= self.window:
            next_val = sum(self.results[-self.window:]) / self.window
            self.moving_avg.append(next_val)

    def best_result(self, x):
        if self.want_increase:
            return (x - 1e-7) > max(self.results)
        else:
            return (x + 1e-7) < min(self.results)

    def stop(self):
        if len(self.moving_avg) < 2:
            return False
        if self.want_increase:
            return (self.moving_avg[-1] + 1e-7) < self.moving_avg[-2]
        else:
            return (self.moving_avg[-2] + 1e-7) < self.moving_avg[-1]