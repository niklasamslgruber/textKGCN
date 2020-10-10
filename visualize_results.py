import matplotlib.pyplot as plt
from helper import file_utils as file, io_utils as io


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
