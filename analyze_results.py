import os

import matplotlib.pyplot as plt
from config import FLAGS
from helper import file_utils as file, io_utils as io
import pandas as pd

available_datasets = ["r8", "mr", "ohsumed", "r52", "20ng"]


def visualize_loss(loss_array, loss):
    number_epochs = len(loss_array)
    fig, ax = plt.subplots(figsize=(15, 15))
    fig.suptitle(f"Validation loss for {number_epochs} epochs")
    fig.tight_layout()
    plt.plot(range(0, number_epochs), loss_array, label="Validation loss")
    plt.plot(range(0, len(loss)), loss, label="Loss")
    plt.legend()
    plt.savefig(io.get_eval_loss_plot_path())
    plt.close(fig)


def analyze_results(dataset):
    if not os.path.isfile(io.get_eval_log_path(dataset)):
        return None
    data = file.get_eval_logs(dataset)
    window_size = set(data["window_size"].tolist())
    raw_count = set(data["raw_count"].tolist())
    threshold = set(data["threshold"].tolist())

    results = []
    references = []

    for w in window_size:
        reference = data[(data["wiki_enabled"] == False) & (data["window_size"] == w)].iloc[:, 5:]
        count = reference.shape[0]
        references.append([count, False, w, "NaN", "NaN"] + reference.mean().tolist())
        for t in threshold:
            for r in raw_count:
                filtered_data = data[
                    (data["window_size"] == w) &
                    (data["threshold"] == t) &
                    (data["raw_count"] == r) &
                    (data["wiki_enabled"] == True)
                    ].iloc[:, 5:]
                count = filtered_data.shape[0]
                meta = [count, True, w, r, t]
                results.append(meta + filtered_data.max().tolist())

    total = references + results
    results_df = pd.DataFrame(total)
    results_df.columns = ["count"] + data.columns[1:].tolist()
    results_df = results_df.sort_values(by=["window_size", "threshold"]).reset_index(drop=True)
    results_df = results_df.dropna()
    return results_df


def plot_results(data, ax, metric, dataset):
    raw_count = set(data["raw_count"].tolist())
    if "NaN" in raw_count:
        raw_count.remove("NaN")
    thresholds = list(set(data["threshold"].tolist()))
    if "NaN" in thresholds:
        thresholds.remove("NaN")

    wiki_cond = data["wiki_enabled"] == True
    window_cond = data["window_size"] == 15

    # Split into separate dataframes based
    data_dict = {}
    for r in raw_count:
        raw_cond = data["raw_count"] == r
        metric_data = data[raw_cond & window_cond & wiki_cond][[metric, "threshold"]]
        metric_data = metric_data.set_index("threshold")
        metric_dict = metric_data.to_dict()[metric]
        data_dict[r] = metric_dict

    base = data[(data["wiki_enabled"] == False) & window_cond][metric].tolist()
    assert len(base) <= 1
    data_dict["no_wiki"] = base

    ax.set_xlabel("threshold")
    ax.set_ylabel(metric)
    ax.title.set_text(dataset)
    ax.set_xticks(thresholds)

    assert len(data_dict.keys()) == 3
    for key in data_dict:
        value = data_dict[key]
        name = "Raw" if key else "IDF"
        color = "b" if key else "g"
        if key == "no_wiki":
            if len(value) > 0:
                tmp = [value[int(t)] for t in value]
                assert len(tmp) == 1
                metrics = tmp * len(thresholds)
                name = "textGCN"
                color = "r"
        else:
            metrics = [value[t] for t in value]
        assert len(metrics) == len(thresholds)
        ax.plot(thresholds, metrics, color, label=name, linewidth=2)

    ax.legend()


def plot_all(metric="accuracy"):
    number_subplots = len(available_datasets)
    fig, ax = plt.subplots(number_subplots, figsize=(15, 15))
    fig.suptitle(f"Results by threshold (metric: accuracy)")

    data_dict = {}
    for index, dataset in enumerate(available_datasets):
        results_df = analyze_results(dataset)
        data_dict[dataset] = results_df
        if results_df is not None:
            plot_results(results_df, ax[index], metric, dataset)
    assert len(data_dict.keys()) == number_subplots

    plt.tight_layout()
    plt.savefig(f"{io.get_basic_plots_path()}/dataset_results.png")
    plt.close(fig)


def plot_number_of_edges():
    thresholds = range(1, 85)
    dataset_length = {}
    for dataset in available_datasets:
        number_of_edges = []
        document_triples = file.get_document_triples_metrics(dataset)
        for t in thresholds:
            num = document_triples[document_triples["count"] > t].shape[0]
            number_of_edges.append(num)
        assert len(number_of_edges) == len(thresholds)
        dataset_length[dataset] = number_of_edges

    print(dataset_length)
    fig, ax = plt.subplots(figsize=(30, 15))
    fig.suptitle(f"Number of doc2doc edges for threshold")
    plt.xlabel("Threshold")
    plt.ylabel("Count")
    plt.xticks(thresholds)
    plt.yscale("log")
    counter = 0
    colors = ["r", "g", "b", "y", "c", "m"]

    for key in dataset_length:
        value = dataset_length[key]
        plt.plot(thresholds, value, colors[counter], label=key, linewidth=4)
        counter += 1

    plt.legend()
    fig.tight_layout()
    plt.savefig(f"{io.get_basic_plots_path()}/edge_thresholds.png")
    plt.close(fig)


if __name__ == '__main__':
    # analyze_results()
    plot_all()
