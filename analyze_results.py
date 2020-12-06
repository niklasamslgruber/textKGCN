import seaborn as sns
import matplotlib.pyplot as plt
from config import FLAGS
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
    fig.savefig(f"{io.get_root_path()}/plots/edge_thresholds.png")


# RESULTS
def plot_metric(dataset, metric="accuracy"):
    results = file.get_eval_logs(dataset)
    base = results[(results["wiki_enabled"] == False) & (results["window_size"] == 15)][metric]
    base_mean = base.mean()
    base_std = base.std()

    results = results[results["wiki_enabled"] == True]
    if "r8" in dataset or "r52" in dataset:
        order = ["count", "idf", "idf_wiki", "count_old", "idf_old", "idf_old_wiki"]
        g = sns.FacetGrid(data=results, col="raw_count", col_wrap=3, col_order=order, sharex=False, sharey=False)
    else:
        g = sns.FacetGrid(data=results, col="raw_count", col_wrap=3, sharex=False, sharey=False)
    g.map(sns.lineplot, "threshold", metric, ci="sd", err_style="bars", markers=True, dashes=False, color="black")
    g.set_titles(row_template='{row_name}1', col_template='{col_name}')

    color = "black"
    for x in range(0, len(g.axes)):
        ax = g.axes[x]
        ax.axhline(y=base_mean, color=color, linewidth=1, alpha=.3, ls="--")
        ax.axhline(y=base_mean + base_std, color=color, linewidth=1, alpha=.3, ls="--")
        ax.axhline(y=base_mean - base_std, color=color, linewidth=1, alpha=.3, ls="--")

    g.savefig(f"{io.get_basic_plots_path(dataset)}/{dataset}_{metric}.png")


def plot_edge_density(dataset):
    edges = file.get_base_edges(dataset)

    # Plot histogram for each edge type
    g = sns.FacetGrid(data=edges, col="edge_type", sharey=False, sharex=False)
    g.map_dataframe(sns.histplot, x="weight", color="black", linewidth=0, discrete=True)
    g.set_axis_labels("edge weight", "count")
    g.set_titles(col_template="{col_name}", row_template="{row_name}")
    for ax in g.fig.get_axes():
        ax.set_yscale("log")
    # g.fig.subplots_adjust(top=0.8)
    # g.fig.suptitle(f"distribution of edge type weights in {dataset}", fontsize=16)

    g.savefig(f"{io.get_basic_plots_path(dataset)}/{dataset}_density.png")


def plot_all(metric="accuracy", density=False):
    for dataset in available_datasets:
        plot_metric(dataset, metric)
        if density:
            plot_edge_density(dataset)


def get_results_statistics(dataset, metric="accuracy"):
    eval = file.get_eval_logs(dataset)
    thresholds = set(eval["threshold"].tolist())

    types = ["count", "idf", "idf_wiki", "count_old", "idf_old", "idf_old_wiki"]
    data_array = []
    for t in thresholds:
        for r in types:
            eval_filter = eval[
                (eval["wiki_enabled"] == True) & (eval["window_size"] == 15) & (eval["threshold"] == t) & (
                        eval["raw_count"] == r)][metric]
            data_array.append([t, r, eval_filter.shape[0], eval_filter.mean(), eval_filter.std()])

    eval_filter = eval[(eval["wiki_enabled"] == False) & (eval["window_size"] == 15)][metric]
    data_array.append([0, "base", eval_filter.shape[0], eval_filter.mean(), eval_filter.std()])
    result = pd.DataFrame(data_array).dropna().round(4)
    result.columns = ["threshold", "edge_type", "count", "mean", "std_dev"]

    # Latex configuration
    data = result.replace(r"_", r"\_", regex=True)
    header = data.columns[:-1]

    all_values = []
    for index, row in data.iterrows():
        row_values = [row["threshold"], row["edge_type"], row["count"], "$" + str(row["mean"]) + " \pm " + str(row["std_dev"]) + "$"]
        all_values.append(row_values)

    # Return LaTex code for the results dataframe
    get_latex_code(header, all_values, "llll", f"{dataset}_{metric}_table.txt", dataset, "Classification accuracy R8 dataset", "Accuracy on text classification for the r8 dataset for differet thresholds and edge types")


def get_latex_code(header, rows, justification, filename, dataset, caption="EMPTY CAP", desc="EMPTY DESC"):
    assert len(justification) == len(header), f"You must provide the same number of justification symbols {len(justification)} as the header length {len(header)}"

    header = " & ".join(header).replace(r"_", r"\_")

    new_rows = []
    for row in rows:
        new_row = " & ".join([str(val) for val in row])
        new_rows.append(new_row)
    items = r" \\" + "\n   "
    rows_latex = items.join(new_rows)

    code = "" \
           r"\begin{center}" + "\n" \
           r"\begin{table}[htbp]" + "\n" \
           "\n" \
           r"{" + "\n" \
           r"   \small" + "\n" \
           r"   \begin{center}" + "\n" \
           r"   \begin{tabular}[center]{" + f"{justification}" + "}\n" \
           r"   \toprule" + "\n" \
           rf"   {header} \\" + "\n\n" \
           r"   \midrule" + "\n" \
           rf"   {rows_latex} \\" + "\n\n" \
           r"   \bottomrule" + "\n" \
           r"   \end{tabular}" + "\n" \
           r"   \end{center}" + "\n" \
           r"}" + "\n\n" \
           rf"\caption[{caption}]" + "{" + f"{desc}" + "\n" \
           r"\label{tab:CommonParameterSettings}}" + "\n" \
           r"\end{table}" + "\n" \
           r"\end{center}"

    assert filename.endswith(".txt")
    filename = filename.replace(".txt", f"_{FLAGS.version}.txt")
    write_latex_code(code, filename, dataset)


def write_latex_code(data, filename, dataset):
    assert filename.endswith(".txt")
    file = open(f"{io.get_latex_path(dataset)}/{filename}", "w")
    file.writelines(data)
    file.close()


if __name__ == '__main__':
    # plot_all(density=False)
    get_results_statistics("r8")
    # plot_edge_numbers()
