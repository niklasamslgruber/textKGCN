import matplotlib.pyplot as plt
import numpy as np
from sklearn.manifold import TSNE


def reduce_dimensions(embeddings, fraction=None):
    # Dimensionality reduction with t-SNE
    # Source: https://www.kaggle.com/ferdzso/knowledge-graph-analysis-with-node2vec
    number_of_embeddings = len(embeddings)

    if fraction is not None:
        idx = np.random.randint(number_of_embeddings, size=int(number_of_embeddings * fraction))
        x = embeddings[idx, :]
        print(f'Number of embeddings: {len(idx)} (fractioned by factor {fraction})')

    else:
        x = embeddings
        print(f'Number of embeddings: {len(x)}')

    # Perform 2D t-SNE dimensionality reduction
    x_embedded = TSNE(n_components=2, random_state=1).fit_transform(x)
    print(f't-SNE object was trained with {x.shape[0]} items')

    return x_embedded


def visualize(embeddings, filename=None, labels=None):
    if labels is not None:
        # Generate random colors for each label
        show_legend = False
        if len(set(labels)) == 4:
            colors = ["r", "b", "g", "y"]
            show_legend = True
        if len(set(labels)) == 8:
            colors = ["r", "b", "g", "y", "c", "m", "k", "burlywood"]
            show_legend = True
        else:
            colors = np.random.rand(len(set(labels)), 3)

        label_map = {}
        for i, l in enumerate(labels):
            if l not in label_map:
                label_map[l] = []
            label_map[l].append(i)
        fig, ax = plt.subplots(figsize=(15, 15))

        # Layout
        fig.suptitle(f'Number of labels: {len(set(labels))}')
        fig.tight_layout()

        for i, lab in enumerate(label_map.keys()):
            idx = label_map[lab]
            x = list(embeddings[idx, 0])
            y = list(embeddings[idx, 1])
            ax.scatter(x, y, s=150, color=colors[i], label=lab, alpha=0.5, edgecolors='none')

        if show_legend:
            plt.legend()

    else:
        plt.figure(figsize=(15, 15))
        x = list(embeddings[:, 0])
        y = list(embeddings[:, 1])
        plt.scatter(x, y, alpha=0.5)

    # Save or show graph
    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)


def visualize_highlight(embeddings, id1, id2, label, filename=None, labels=None, colors=None):
    if labels is not None:
        # Generate random colors for each label
        show_legend = False
        if colors is None:
            colors = np.random.rand(len(set(labels)), 3)

        label_map = {}
        for i, l in enumerate(labels):
            if l not in label_map:
                label_map[l] = []
            label_map[l].append(i)
        fig, ax = plt.subplots(figsize=(15, 15))

        # Layout
        fig.suptitle(f'Number of labels: {len(set(labels))}')
        fig.tight_layout()
        color_index = -1
        for i, lab in enumerate(label_map.keys()):
            idx = label_map[lab]
            color_string = lab == label
            if color_string:
                color_index = i

            x = list(embeddings[idx, 0])
            y = list(embeddings[idx, 1])

            edge_color = "black" if color_string else "none"
            alpha_val = 1 if color_string else 0.5

            ax.scatter(x, y, s=150, color=colors[i], label=lab, alpha=alpha_val, edgecolors=edge_color)

        print(colors)
        plt.legend(loc=2, fontsize=10)
        x_new = list(embeddings[[id1, id2], 0])
        y_new = list(embeddings[[id1, id2], 1])
        ax.scatter(x_new, y_new, s=800, color=colors[color_index], label=label, alpha=1, edgecolors='black')

        # if show_legend:


    else:
        plt.figure(figsize=(15, 15))
        x = list(embeddings[:, 0])
        y = list(embeddings[:, 1])
        plt.scatter(x, y, alpha=0.5)

    # Save or show graph
    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)
