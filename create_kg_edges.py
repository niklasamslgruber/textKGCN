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
import pandas as pd
from tqdm import tqdm

triples_path = f"{get_kg_data_path()}/triples/{FLAGS.dataset}_triples.csv"
filtered_triples_path = f"{get_kg_data_path()}/triples/{FLAGS.dataset}_filtered_triples.csv"
document_triples_path = f"{get_kg_data_path()}/triples/{FLAGS.dataset}_document_triples.csv"


# Data loader
def get_all_entities():
    return read_json_file(entities_path)


def get_relevant_relations():
    return read_csv(filtered_relations_path)


def get_entity2id():
    return pd.read_csv(entity2id_path, index_col=None, header=None, sep=",", names=["name", "id"])


def get_vocab_ids():
    entity2id_df = get_entity2id()
    unmapped_entities = entity2id_df[entity2id_df["id"] == "-1"].index
    entity2id_df.drop(unmapped_entities, inplace=True)
    return entity2id_df["id"].to_numpy()


def get_triples(filtered=False):
    path = filtered_triples_path if filtered else triples_path
    return pd.read_csv(path, index_col=None, header=None, sep=",", names=["entity1", "relation", "entity2"])


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
    # Creates triples based on the vocab entities and relations (unfiltered)
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

    write_csv(triples_path, triples)
    return triples


def filter_triples():
    # Adjust filters in `analyze_properties` and save them to the filtered_relations.csv
    triples = get_triples()
    relevant_relations = get_relevant_relations()["ID"].to_numpy()
    vocab_ids = get_vocab_ids()
    old_size = triples.shape[0]

    # Filter out all triples which are not contained in `filtered_relations.csv`
    irrelevant_triples = triples[~triples["relation"].isin(relevant_relations)].index
    triples.drop(irrelevant_triples, inplace=True)

    # Filter out all triples which don't lead to another word from the node
    unmatched_triples = triples[~triples["entity2"].isin(vocab_ids)].index
    triples.drop(unmatched_triples, inplace=True)

    # Filter out all relation to itself
    self_relations = triples[triples["entity1"] == triples["entity2"]].index
    triples.drop(self_relations, inplace=True)

    # Drop duplicate relations
    triples.drop_duplicates(inplace=True)

    write_csv(filtered_triples_path, triples)
    print(f"Filtered out {old_size - triples.shape[0]} irrelevant triples...")


def setup_triples():
    # Creates a filtered and unfiltered triples CVS file
    create_triples()
    filter_triples()


# Adjacency matrices
def create_adjacency_matrix():
    vocab_ids = get_entity2id()
    filtered_triples = get_triples(filtered=True)
    docs = get_documents()

    sizes = []
    counter = 0
    prev_ids = []
    for doc in docs:
        ids = vocab_ids[vocab_ids["name"].isin(doc)]["id"].to_numpy()

        if counter == 6:
            print(doc)
            print(vocab_ids[vocab_ids["name"].isin(doc)])
            print(ids)
        assert len(set(doc)) == len(ids)
        if len(prev_ids) > 0:
            test = filtered_triples[filtered_triples["entity1"].isin(ids) & filtered_triples["entity2"].isin(prev_ids)]
            sizes.append(test.shape[0])

            if counter == 6:
                print("Hwe")
                print(test)
                print(f"Size is {test.shape[0]}")

        counter += 1
        prev_ids = ids

    print("Statistics")
    print(f"Max: {max(sizes)}")
    print(f"Min: {min(sizes)}")
    listY = list(sizes)
    print(f"Number of O's: {listY.count(0)}")
    print(f"Number of not 0's: {len(listY) - listY.count(0)}")
    # print(listY)
    print(f"Total entries: {len(sizes)}")


def test():
    vocab_ids = get_entity2id()
    filtered_triples = get_triples(filtered=True)
    docs = get_documents()

    sizes = []
    triples = []

    current_document = 0
    with tqdm(total=sum(range(1, len(docs)))) as bar:
        for doc in docs:
            # Get Id's of every word in document
            ids = vocab_ids[vocab_ids["name"].isin(doc)]["id"].to_numpy()
            assert len(set(doc)) == len(ids)
            current_triples = filtered_triples["entity1"].isin(ids)

            # Helper variables
            current_sub_doc = 0

            for sub_doc in docs:
                # Skip relations to itself
                if current_sub_doc <= current_document:
                    # print("Skipped")
                    current_sub_doc += 1
                    continue
                # Get ID's of other document
                sub_ids = vocab_ids[vocab_ids["name"].isin(sub_doc)]["id"].to_numpy()
                # Check if there are any relation between doc and sub_doc
                relation_to_subdoc = filtered_triples[current_triples & filtered_triples["entity2"].isin(sub_ids)]

                number_of_relations = relation_to_subdoc.shape[0]
                sizes.append(number_of_relations)

                # Add non-zero triples to document triple
                if not number_of_relations == 0:
                    triple = [current_document, current_sub_doc, int(relation_to_subdoc.shape[0])]
                    triples.append(triple)

                current_sub_doc += 1
                bar.update(1)

            # Next document
            current_document += 1

    assert len(sizes) == sum(range(1, current_document))

    print("Statistics")
    print(f"Max: {max(sizes)}")
    print(f"Min: {min(sizes)}")
    list_sizes = list(sizes)
    print(f"Number of O's: {list_sizes.count(0)}")
    print(f"Number of not 0's: {len(list_sizes) - list_sizes.count(0)}")
    print(f"Total entries: {len(sizes)}")

    data = pd.DataFrame(triples, columns=["doc1", "doc2", "number_of_relations"])
    data.to_csv(document_triples_path, index=False, header=True, sep=",")


if __name__ == '__main__':
    # setup_triples()
    # create_adjacency_matrix()
    test()
