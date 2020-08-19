import matplotlib.pyplot as plt
import numpy as np
from sklearn.manifold import TSNE
from load_embeddings import get_embeddings, GraphType


def reduce_dimensionality(embeddings, fraction=None):
    # Source: https://www.kaggle.com/ferdzso/knowledge-graph-analysis-with-node2vec
    # Dimensionality reduction with t-SNE
    number_of_embeddings = len(embeddings)

    if fraction is not None:
        idx = np.random.randint(number_of_embeddings, size=int(number_of_embeddings * fraction))
        x = embeddings[idx, :]
        print(f'Number of embeddings: {len(idx)} (fractioned)')

    else:
        x = embeddings
        print(f'Number of embeddings: {N}')

    # Perform 2D t-SNE dimensionality reduction
    x_embedded = TSNE(n_components=2).fit_transform(x)
    print(f't-SNE object was trained with {x.shape[0]} items')

    return x_embedded


def visualize(embeddings, filename=None, labels=None, colors=['r', 'b']):
    if labels is not None:
        label_map = {}
        for i, l in enumerate(labels):
            if l not in label_map:
                label_map[l] = []
            label_map[l].append(i)
        fig, ax = plt.subplots(figsize=(15, 15))
        for i, lab in enumerate(label_map.keys()):
            idx = label_map[lab]
            x = list(embeddings[idx, 0])
            y = list(embeddings[idx, 1])
            ax.scatter(x, y, c=colors[i], label=lab, alpha=0.5, edgecolors='none')
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
        plt.savefig(f'knowledge_graphs/plots/{filename}')


def main():
    # Load binary files
    entity_embeddings = get_embeddings(node_type=GraphType.ENTITIES, dimension=50)

    embeddings = reduce_dimensionality(entity_embeddings, fraction=0.00005)
    visualize(embeddings)


if __name__ == "__main__":
    main()
