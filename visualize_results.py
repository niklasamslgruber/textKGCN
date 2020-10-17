import matplotlib.pyplot as plt
from helper import file_utils as file, io_utils as io
import pandas as pd


def plot_results(metric="accuracy"):
    logs = file.get_eval_logs()
    if metric not in logs.columns:
        raise ValueError("The metric is not included in the logs")

    wiki_results = logs[logs["wiki_enabled"]]
    non_wiki_results = logs[~logs["wiki_enabled"]]

    fig, ax = plt.subplots(figsize=(15, 15))
    fig.suptitle(f"Classification results based on previous models (metric: {metric})")
    fig.tight_layout()
    plt.plot(range(0, wiki_results.shape[0]), wiki_results[metric], label="WikiData enabled")
    plt.plot(range(0, non_wiki_results.shape[0]), non_wiki_results[metric], label="WikiData disabled")
    plt.legend()

    plt.savefig(io.get_results_plot_path(metric=metric))
    plt.close(fig)


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
    print(f"Average results for {dataset}")
    print(results_df)


if __name__ == '__main__':
    analyze_results("r52")
