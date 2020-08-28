from visualize_tsne import visualize, reduce_dimensions
import numpy as np


def plot(model):
    i = 0
    for layer in model.layers:
        embeddings = layer.acted_embeddings
        reduced_emb = reduce_dimensions(embeddings)
        labels = generate_labels(embeddings)
        visualize(reduced_emb, filename=f'plots/gcn/layer_{i}.png', labels=labels)
        i += 1


def generate_labels(embeddings):
    # Node gets the highest dimension as label (assumption from paper)
    max_indices = []
    for emb in embeddings:
        array = np.array(emb)
        max_index = array.argmax()
        max_indices.append(max_index)

    print(f'Number of labels: {len(set(max_indices))}')

    return max_indices
