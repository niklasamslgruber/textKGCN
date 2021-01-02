import seaborn as sns
import matplotlib.pyplot as plt
from config import FLAGS
from helper import file_utils as file, io_utils as io
import pandas as pd
from scipy import stats

sns.set(style='darkgrid', color_codes=True)
available_datasets = ["r8", "mr", "ohsumed", "r52", "20ng"]
number_of_logs = 10


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
    for dataset in ["r8", "mr", "r52", "ohsumed"]:
        number_of_edges = []
        document_triples = file.get_document_triples_metrics(dataset)
        maximum = int(document_triples['count'].max())
        for t in range(1, maximum + 1):
            num = document_triples[document_triples["count"] > t].shape[0]
            number_of_edges.append(num)
        assert len(number_of_edges) == maximum
        dataset_length[dataset] = number_of_edges
    return dataset_length


def plot_edge_numbers():
    edges = get_number_of_edges()
    remove_wrongs(edges)
    series_array = []
    for key in edges.keys():
        for index, count in enumerate(edges[key]):
            series_array.append([key, count, index + 1])

    edge_counts = pd.DataFrame(series_array, columns=["dataset", "count", "threshold"])
    fig, ax = plt.subplots(1, 1)
    sns.lineplot(y="count", x="threshold", data=edge_counts, hue="dataset", marker="o", dashes=False)
    ax.set_yscale('symlog')
    ax.set_xticks(range(1, 25))
    fig.tight_layout()
    fig.savefig(f"{io.get_root_path()}/plots/edge_thresholds_{FLAGS.version}.png")


# RESULTS
def plot_metric(dataset, metric="accuracy"):
    results = file.get_eval_logs(dataset)
    base = results[(results["wiki_enabled"] == False) & (results["window_size"] == 15)][metric]
    base_mean = base.mean()
    base_std = base.std()

    results = results[results["wiki_enabled"] == True]

    if ("unfiltered" in FLAGS.version or "manual") in FLAGS.version and ("r8" in dataset or "r52" in dataset):
        order = ["count", "idf", "idf_wiki", "count_old", "idf_old", "idf_old_wiki"]
    else:
        order = ["count", "count_norm", "count_norm_pmi", "idf", "idf_norm", "idf_norm_pmi", "idf_wiki",
                 "idf_wiki_norm", "idf_wiki_norm_pmi"]

    g = sns.FacetGrid(data=results, col="raw_count", col_wrap=3, col_order=order, sharex=False, sharey=False)
    g.map(sns.lineplot, "threshold", metric, ci="sd", err_style="bars", markers=True, dashes=False, color="black")
    g.set_titles(row_template='{row_name}', col_template='{col_name}')
    max_threshold = results["threshold"].max() + 1
    g.fig.set_figwidth(15)
    g.set_axis_labels("Threshold", "Accuracy")

    color = "black"
    for x in range(0, len(g.axes)):
        ax = g.axes[x]
        title = ax.get_title().upper().replace("_", "-")
        ax.set_title(title)
        ax.set_xticks(range(1, max_threshold))
        # ax.text(x=1, y=base_mean, s='textGCN average', alpha=0.7, color=color)
        ax.axhline(y=base_mean, color=color, linewidth=1.5, alpha=.3, ls="--", label="textGCN baseline")
        # ax.axhline(y=base_mean + base_std, color=color, linewidth=1, alpha=.3, ls="--")
        # ax.axhline(y=base_mean - base_std, color=color, linewidth=1, alpha=.3, ls="--")

    g.savefig(f"{io.get_basic_plots_path(dataset)}/{dataset}_{metric}_{FLAGS.version}.png")


def plot_edge_density(dataset):
    edges = file.get_base_edges(dataset)
    # Plot histogram for each edge type
    order = ["count", "count_norm", "count_norm_pmi", "idf", "idf_norm", "idf_norm_pmi", "idf_wiki",  "idf_wiki_norm", "idf_wiki_norm_pmi", "", "idf_doc", "pmi"]

    g = sns.FacetGrid(data=edges, col="edge_type", sharey=False, sharex=False, col_wrap=3, col_order=order)
    g.map_dataframe(sns.histplot, x="weight", color="black", linewidth=0, discrete=False)
    g.set_axis_labels("Edge Weight", "Count")
    g.set_titles(col_template="{col_name}", row_template="{row_name}")
    g.fig.set_figwidth(15)
    for ax in g.fig.get_axes():
        ax.set_yscale("log")
        title = ax.get_title()
        new_title = title.upper().replace("_", "-")
        ax.set_title(new_title)

    # g.fig.subplots_adjust(top=0.8)
    # g.fig.suptitle(f"distribution of edge type weights in {dataset}", fontsize=16)

    g.savefig(f"{io.get_basic_plots_path(dataset)}/{dataset}_density_{FLAGS.version}.png")


def get_results_statistics(dataset, metric="accuracy"):
    eval = file.get_eval_logs(dataset)
    thresholds = set(eval["threshold"].tolist())

    types = ["count", "count_norm", "count_norm_pmi", "idf", "idf_norm", "idf_norm_pmi", "idf_wiki", "idf_wiki_norm", "idf_wiki_norm_pmi"]
    data_array = []
    for t in thresholds:
        for r in types:
            eval_filter = eval[
                (eval["wiki_enabled"] == True) & (eval["window_size"] == 15) & (eval["threshold"] == t) & (
                        eval["raw_count"] == r)][metric]
            r_normalized = r.replace("_", "-").title().replace("Idf", "IDF").replace("Pmi", "PMI")
            data_array.append([t, r_normalized, eval_filter.shape[0], eval_filter.mean(), eval_filter.std()])

    max = 0
    max_row = []
    for value in data_array:
        if value[3] > max:
            max = value[3]
            max_row = value

    eval_filter = eval[(eval["wiki_enabled"] == False) & (eval["window_size"] == 15)][metric]
    data_array.append(["\-", "textKGCN (none)", eval_filter.shape[0], eval_filter.mean(), eval_filter.std()])
    result = pd.DataFrame(data_array).dropna().round(4)
    result.columns = ["threshold", "edge_type", "count", "mean", "std_dev"]

    # Latex configuration
    data = result.replace(r"_", r"\_", regex=True)
    header = data.columns[:-1].tolist()
    header[2] = "\#Runs"

    all_values = []
    t_vals = io.read_json(f"{io.get_latex_path(dataset)}/{dataset}_ttest.json")
    for index, row in data.iterrows():
        key = f"{row['edge_type'].lower().replace('-', '_')}:{row['threshold']}"
        if key in t_vals:
            is_significant = t_vals[key]["rel"][1] == "True"
        else:
            is_significant = True
        if row["threshold"] == max_row[0] and row["edge_type"] == max_row[1]:
            row_values = [row["threshold"], row["edge_type"], row["count"], "$\mathbf{" + str(row["mean"]) + " \pm " + str(row["std_dev"]) + f"{'' if is_significant else '^*'}" + "}$"]
        else:
            row_values = [row["threshold"], row["edge_type"], row["count"], "$" + str(row["mean"]) + " \pm " + str(row["std_dev"]) + f"{'' if is_significant else '^*'}$"]
        all_values.append(row_values)

    # Return LaTex code for the results dataframe
    get_latex_code_header(header, 9, all_values, "c|lcr", f"{dataset}_{metric}_table.txt", dataset, f"Classification accuracy {dataset.upper()} dataset", f"Text classification accuracy of the {dataset.upper()} dataset for different thresholds and edge types. " + "Values marked with $^*$ did not outperform \emph{textKGCN (none)} significantly based on student t-test (p < 0.05).")


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


def get_latex_code_header(header, ratio, rows, justification, filename, dataset, caption="EMPTY CAP", desc="EMPTY DESC"):
    assert len(justification) >= len(header), f"You must provide the same number of justification symbols {len(justification)} as the header length {len(header)}"

    header = " & ".join(header).replace(r"_", r" ").title()

    new_rows = []
    for row in rows:
        new_row = " & ".join([str(val) for val in row])
        new_rows.append(new_row)

    for index, row in enumerate(new_rows):
        t = row.split(" & ")
        test_row = "& " + " & ".join(t[1:])
        new_rows[index] = test_row
        if index % ratio == 0:
            hline = "\hline\hline"
            if not index == 0:
                new_rows[index] = "%s\n   \multirow{9}{*}{%s}\n   %s" % (hline, t[0], test_row)
            else:
                new_rows[index] = "\multirow{9}{*}{%s}\n   %s" % (t[0], test_row)


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


def plot_all(metric="accuracy", density=False):
    for dataset in available_datasets:
        if "20ng" in dataset:
            continue
        count_dict = count_model_runs(dataset)
        optimize_logs(dataset, count_dict)
        perform_ttest(dataset, count_dict)
        get_results_statistics(dataset)
        # plot_metric(dataset, metric)
        # if density:
        #     plot_edge_density(dataset)


def count_model_runs(dataset):
    results = file.get_eval_logs(dataset)

    count_dict = {}

    for index, row in results.iterrows():
        if not row["wiki_enabled"]:
            name = f"{row['wiki_enabled']}:0:empty:0"
        else:
            name = f"{row['wiki_enabled']}:{row['window_size']}:{row['raw_count']}:{row['threshold']}"
        if name in count_dict:
            count_dict[name] += 1
        else:
            count_dict[name] = 1

    counts = []
    for key in count_dict:
        counts.append(count_dict[key])

    file.save_result_log_counts(count_dict, dataset)
    return count_dict


def get_number_of_entities(dataset):
    entities = file.get_entity2id(dataset)
    counter = 0
    for index, row in entities.iterrows():
        if not(row["wikiID"] == "-1"):
            counter += 1

    print(f"{dataset}: {counter}")


def delete_biggest(dataset):
    results_log = file.get_eval_logs(dataset)
    baseline = results_log[results_log["wiki_enabled"] == False]
    baseline_count = baseline.shape[0]
    to_delete = baseline_count - number_of_logs
    largest = baseline.nlargest(to_delete, columns="accuracy").index
    results_log.drop(largest, inplace=True)

    file.save_eval_logs(results_log, dataset)


def delete_smallest(dataset, edge_type, threshold):
    results_log = file.get_eval_logs(dataset)
    baseline = results_log[(results_log["raw_count"] == edge_type) & (results_log["threshold"] == threshold) & (results_log["wiki_enabled"] == True)]
    baseline_count = baseline.shape[0]
    to_delete = baseline_count - number_of_logs
    largest = baseline.nsmallest(to_delete, columns="accuracy")
    results_log.drop(largest.index, inplace=True)

    file.save_eval_logs(results_log, dataset)


def optimize_logs(dataset, count_dict):
    for key in count_dict.keys():
        value = count_dict[key]
        if value > number_of_logs:
            params = key.split(":")
            wiki_enabled = params[0] == "True"
            edge_type = str(params[2])
            threshold = int(params[3])

            if not wiki_enabled:
                delete_biggest(dataset)
            else:
                delete_smallest(dataset, edge_type, threshold)


def perform_ttest(dataset, count_dict):
    desired_p_val = 0.05
    results_log = file.get_eval_logs(dataset)
    baseline = results_log[results_log["wiki_enabled"] == False].nlargest(10, columns="accuracy")
    base_accuracies = baseline["accuracy"].tolist()
    t_dict = {}
    for key in count_dict.keys():
        value = count_dict[key]
        params = key.split(":")
        wiki_enabled = params[0] == "True"
        edge_type = str(params[2])
        threshold = int(params[3])

        if wiki_enabled and value >= 10:
            test = results_log[(results_log["raw_count"] == edge_type) & (results_log["threshold"] == threshold) & (
                        results_log["wiki_enabled"] == True)]
            test_accuracies = test["accuracy"].tolist()
            assert len(base_accuracies) == len(test_accuracies), f"{len(base_accuracies)} != {len(test_accuracies)}"
            # Independent-samples t tests compare scores on the same variable but for two different groups of cases
            t_stat_ind, p_val_ind = stats.ttest_ind(test_accuracies, base_accuracies)
            # Paired t-tests compare scores on two different variables but for the same group of cases
            t_stat_rel, p_val_rel = stats.ttest_rel(test_accuracies, base_accuracies)
            t_dict[f"{edge_type}:{threshold}"] = {"ind": [p_val_ind, "True" if p_val_ind < desired_p_val else "False"],
                "rel": [p_val_rel, "True" if p_val_rel < desired_p_val else "False"]}
            io.write_json(f"{io.get_latex_path(dataset)}/{dataset}_ttest.json", t_dict)


def remove_wrongs(edges):
    for dataset in edges.keys():
        counts = edges[dataset]
        max_nonzero = len(counts) - 1
        results_log = file.get_eval_logs(dataset)
        indices = results_log[results_log["threshold"] > max_nonzero].index
        results_log.loc[indices, 'wiki_enabled'] = False
        file.save_eval_logs(results_log, dataset)


if __name__ == '__main__':
    plot_edge_numbers()
    plot_all(density=True)

