import seaborn as sns
import matplotlib.pyplot as plt
from helper import file_utils as file, io_utils as io
import pandas as pd

sns.set(style='darkgrid', color_codes=True)
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


def get_number_of_edges():
    dataset_length = {}
    for dataset in available_datasets:
        number_of_edges = []
        document_triples = file.get_document_triples_metrics(dataset)
        maximum = document_triples['count'].max()
        for t in range(1, maximum + 1):
            num = document_triples[document_triples["count"] > t].shape[0]
            number_of_edges.append(num)
        assert len(number_of_edges) == maximum
        dataset_length[dataset] = number_of_edges
    return dataset_length


def plot_edge_numbers():
    edges = get_number_of_edges()
    series_array = []
    for key in edges.keys():
        for index, count in enumerate(edges[key]):
            series_array.append([key, count, index + 1])

    edge_counts = pd.DataFrame(series_array, columns=["dataset", "count", "threshold"])
    fig, ax = plt.subplots(1, 1)
    sns.lineplot(y="count", x="threshold", data=edge_counts, hue="dataset", markers=None)
    ax.set_yscale('log')
    fig.tight_layout()
    fig.savefig(f"{io.get_basic_plots_path()}/edge_thresholds.png")


# RESULTS
def plot_metric(dataset, metric="accuracy"):
    results = file.get_eval_logs(dataset)
    base = results[results["wiki_enabled"] == False][metric]
    base_mean = base.mean()
    base_min = base.min()
    base_max = base.max()

    results = results[results["wiki_enabled"] == True]
    if "r8" in dataset or "r52" in dataset:
        order = ["count", "idf", "idf_wiki", "count_old", "idf_old", "idf_old_wiki"]
        g = sns.FacetGrid(data=results, col="raw_count", col_wrap=3, col_order=order)
    else:
        g = sns.FacetGrid(data=results, col="raw_count", col_wrap=3)
    g.map(sns.lineplot, "threshold", metric, ci="sd", err_style="bars", markers=True, dashes=False)
    g.set_titles(row_template='{row_name}', col_template='{col_name}')

    color = "blue"
    for x in range(0, len(g.axes)):
        ax = g.axes[x]
        ax.axhline(y=base_mean, color=color, linewidth=1, alpha=.3, ls="--")
        ax.axhline(y=base_max, color=color, linewidth=1, alpha=.3, ls="--")
        ax.axhline(y=base_min, color=color, linewidth=1, alpha=.3, ls="--")
        # ax.text(y=base_mean * 1.001, x=2*0.98, s="mean", size=7, alpha=.4, color=color)
        # ax.text(y=base_min * 1.001, x=2*0.98, s="min", size=7, alpha=.4, color=color)
        # ax.text(y=base_max * 1.001, x=2*0.98, s="max", size=7, alpha=.4, color=color)

    g.savefig(f"{io.get_basic_plots_path(dataset)}/{dataset}_{metric}.png")


def plot_all(metric="accuracy", density=False):
    for dataset in available_datasets:
        plot_metric(dataset, metric)
        if density:
            plot_edge_counts(dataset)


def plot_edge_counts(dataset):
    metrics = file.get_document_triples_metrics(dataset)

    f, axes = plt.subplots(1, 3)
    sns.kdeplot(metrics["count"], log_scale=True, ax=axes[0])
    sns.kdeplot(metrics["idf"], log_scale=True, ax=axes[1])
    sns.kdeplot(metrics["idf_wiki"], log_scale=True, ax=axes[2])
    f.tight_layout()
    f.savefig(f"{io.get_basic_plots_path(dataset)}/{dataset}_density.png")


if __name__ == '__main__':
    # plot_number_of_edges()
    # plot_all(density=True)
    plot_edge_numbers()
