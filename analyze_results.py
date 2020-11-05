import csv
import os
from collections import Counter, OrderedDict

import matplotlib.pyplot as plt
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
                results.append(meta + filtered_data.mean().tolist())

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

    colors = ["g", "b", "y", "m"]
    counter = 0
    for key in data_dict:
        value = data_dict[key]
        name = key
        color = colors[counter]
        if key == "no_wiki":
            if len(value) > 0:
                tmp = [value[int(t)] for t in value]
                assert len(tmp) == 1
                metrics = tmp * len(thresholds)
                name = "textGCN"
                color = "r"
                labels = thresholds
        else:
            labels = list(value.keys())
            metrics = [value[t] for t in value]
        assert len(metrics) == len(labels)
        ax.plot(labels, metrics, color, label=f"{name} ({len(metrics)})", linewidth=2)
        counter += 1

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
    plt.savefig(f"{io.get_basic_plots_path()}/dataset_results_{metric}.png")
    plt.close(fig)


def get_number_of_edges():
    dataset_length = {}
    for dataset in available_datasets:
        number_of_edges = []
        document_triples = file.get_document_triples_metrics(dataset)
        maximum = document_triples['count'].max()
        print(f"{dataset} max: {maximum}")
        for t in range(1, maximum + 1):
            num = document_triples[document_triples["count"] > t].shape[0]
            number_of_edges.append(num)
        assert len(number_of_edges) == maximum
        dataset_length[dataset] = number_of_edges
    return dataset_length


def plot_number_of_edges():
    ticks = range(1, 85)
    dataset_length = get_number_of_edges()

    fig, ax = plt.subplots(figsize=(30, 15))
    fig.suptitle(f"Number of doc2doc edges for threshold")
    plt.xlabel("Threshold")
    plt.ylabel("Count")
    plt.xticks(ticks)
    plt.yscale("log")
    counter = 0
    colors = ["r", "g", "b", "y", "c", "m"]

    for key in dataset_length:
        value = dataset_length[key]
        plt.plot(range(1, len(value) + 1), value, colors[counter], label=key, linewidth=4)
        counter += 1

    plt.legend()
    fig.tight_layout()
    plt.savefig(f"{io.get_basic_plots_path()}/edge_thresholds.png")
    plt.close(fig)

def test():
    all_rels = file.get_all_relations()
    filtered = file.get_filtered_relations()

    test = all_rels[all_rels["ID"].isin(filtered)]

    test.to_csv("test.csv")
    big_counter = Counter()
    for dataset in available_datasets:
        all = []
        relations = file.get_document_triples(dataset)["detail"].tolist()
        for x in relations:
            rels = x.split("+")
            for r in rels:
                all.append(r)

        big_counter += Counter(all)
    with open('dict.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in OrderedDict(big_counter.most_common()).items():
            desc = all_rels[all_rels["ID"] == key]["description"].tolist()
            label = all_rels[all_rels["ID"] == key]["label"].tolist()
            assert len(desc) == 1
            writer.writerow([key, value, label[0], desc[0]])



if __name__ == '__main__':
    # plot_number_of_edges()
    # plot_all()
    # plot_all("f1_macro")
    # plot_all("f1_micro")
    test()
