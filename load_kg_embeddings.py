from enum import Enum
import numpy as np
from visualize_tsne import reduce_dimensions, visualize
from utils import get_kg_data_path


class GraphType(Enum):
    ENTITIES = "entity"
    RELATIONS = "relation"


def get_embeddings(node_type: GraphType, dimension: int = 50):
    # Downloaded from OpenKE http://139.129.163.161/index/toolkits
    if dimension != 50 and dimension != 100:
        print("[ERROR] - Only dimensions of 50 or 100 are currently supported!")
        return

    number_of_items = get_number_of_items(node_type)

    path = f'{get_kg_data_path()}/embeddings/dimension_{dimension}/transe/{node_type.value}2vec.bin'
    vec = np.memmap(path, dtype='float32', mode='r', shape=(number_of_items, dimension))
    print(f'Loaded {len(vec)} embeddings')
    return vec


def get_number_of_items(node_type: GraphType):
    with open(f'{get_kg_data_path()}/mappings/{node_type.value}2id.txt') as file:
        return int(file.readline().strip())


def main():
    # Load binary files
    entity_embeddings = get_embeddings(node_type=GraphType.ENTITIES, dimension=50)
    embeddings = reduce_dimensions(entity_embeddings, fraction=0.00005)
    visualize(embeddings)


if __name__ == "__main__":
    main()
