"""
Create doc-doc edges

Steps:
1. Load all entities with their relations
2. Load relevant relations
3. Create adjacency matrix for word-word relations
4. Count number of relation between two documents
5. Weight relations and set a doc-doc edge weight
"""
from os.path import join
from config import FLAGS
from match_kg_data import read_json_file, entities_path, write_csv, entity2id_path
from analyze_properties import read_csv, filtered_relations_path
from utils import get_corpus_path, get_kg_data_path
from wiki_api import get_safely


# Data loader
def get_all_entities():
    return read_json_file(entities_path)


def get_relevant_relations():
    return read_csv(filtered_relations_path)


def get_entity2id():
    return read_csv(entity2id_path)


def get_documents():
    docs = []
    clean_text_path = join(get_corpus_path(), FLAGS.dataset + '_sentences_clean.txt')
    file = open(clean_text_path, 'rb')
    for line in file.readlines():
        docs.append(line.strip().decode().split(" "))
    file.close()
    return docs


# Create triple documents
def create_triples():
    triples = []
    all_entities = get_all_entities()
    for entity in all_entities.keys():
        for relation in get_safely(all_entities, [entity, "relations"]).keys():
            for relation_value in get_safely(all_entities, [entity, "relations", relation]).keys():
                result = get_safely(all_entities, [entity, "relations", relation, relation_value])
                if not isinstance(result, dict) or result.get("id") is None:
                    continue
                else:
                    triple = [all_entities[entity]["id"], relation, result.get("id")]
                    triples.append(triple)

    path = f"{get_kg_data_path()}/data/{FLAGS.dataset}_triples.csv"
    write_csv(path, triples)
    return triples


if __name__ == '__main__':
    create_triples()
