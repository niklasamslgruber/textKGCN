"""
Create doc-doc edges

Steps:
1. Load all entities with their relations
2. Load relevant relations
3. Create adjacency matrix for word-word relations
4. Count number of relation between two documents
5. Weight relations and set a doc-doc edge weight
"""
import pandas as pd
from tqdm import tqdm
from helper import file_utils as file
from loader.wiki_api import get_safely


# Data loader
def get_vocab_ids():
    entity2id_df = file.get_entity2id()
    unmapped_entities = entity2id_df[entity2id_df["wikiID"] == "-1"].index
    entity2id_df.drop(unmapped_entities, inplace=True)
    return entity2id_df["wikiID"].to_numpy()


def get_triples(filtered=False):
    return file.get_filtered_triples() if filtered else file.get_all_triples()


def get_documents():
    cleaned_sentences = list(map(lambda doc: doc.split(" "), file.get_cleaned_sentences()))
    return cleaned_sentences


# Create triple documents
def create_triples():
    # Creates triples based on the vocab entities and relations (unfiltered)
    triples = []
    all_entities = file.get_vocab_entities()
    for entity in all_entities.keys():
        for relation in get_safely(all_entities, [entity, "relations"]).keys():
            for relation_value in get_safely(all_entities, [entity, "relations", relation]).keys():
                result = get_safely(all_entities, [entity, "relations", relation, relation_value])
                if not isinstance(result, dict) or result.get("id") is None:
                    continue
                else:
                    triple = [all_entities[entity]["id"], relation, result.get("id")]
                    triples.append(triple)

    file.save_all_triples(triples)
    return triples


def filter_triples():
    # Adjust filters in `analyze_properties` and save them to the filtered_relations.csv
    triples = get_triples()
    relevant_relations = file.get_filtered_relations()
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

    file.save_filtered_triples(triples)
    print(f"Filtered out {old_size - triples.shape[0]} irrelevant triples...")


def setup_triples():
    # Creates a filtered and unfiltered triples CVS file
    create_triples()
    filter_triples()


# Adjacency matrices
def create_doc2doc_edges():
    # Note: Only one half of the adj matrix is generated here to save resources as the matrix is symmetric
    setup_triples()
    doc_nouns_norm = file.get_normalized_nouns()  # Array with all nouns per doc // must be split
    filtered_triples = get_triples(filtered=True)  # Triples

    ids = file.get_doc2id()
    triples = []
    with tqdm(total=len(doc_nouns_norm)) as bar:
        for doc_index, doc in enumerate(doc_nouns_norm):
            if doc == "":
                continue

            # All ID's of the normalized nouns in the current document
            doc_ids = ids[ids["doc"] == doc_index]["wikiID"].tolist()

            # Graph edges pointing to other entities
            triples_out = filtered_triples[filtered_triples["entity1"].isin(doc_ids)]
            # Graph edges pointing to current doc nouns
            triples_in = filtered_triples[filtered_triples["entity2"].isin(doc_ids)]
            triples_in.columns = [triples_out.columns[2], triples_out.columns[1], triples_out.columns[0]]

            # Remove duplicates
            combined_df = triples_out.append(triples_in)
            combined_df.reset_index(inplace=True, drop=True)
            combined_df.drop_duplicates(inplace=True)

            doc_pointers = {}
            for index, row in combined_df.iterrows():
                relation = row["relation"]
                entity2 = row["entity2"]
                pointer = ids[ids["wikiID"] == entity2]["doc"].tolist()
                for doc_id in pointer:
                    if doc_id in doc_pointers:
                        doc_pointers[doc_id].append(relation)
                    else:
                        doc_pointers[doc_id] = [relation]

            for key in doc_pointers:
                relations = doc_pointers[key]
                triples.append([doc_index, key, len(relations), relations])
            bar.update(1)

    data = pd.DataFrame(triples)
    print(f"Highest number of relations between two docs: {max(data[2])}")
    print(f"Created {2 * len(triples)} doc2doc edges")
    save_full_matrix(data)


def save_full_matrix(dataframe):
    # Mirrors the generated half adjacency matrix to a full symmetrical adjacency matrix
    columns = dataframe.columns.tolist()
    new_columns = [columns[1], columns[0], columns[2], columns[3]]
    mirrored_frame = dataframe.copy()
    mirrored_frame.columns = new_columns

    full_adj = dataframe.append(mirrored_frame)
    assert full_adj.shape == (2 * dataframe.shape[0], dataframe.shape[1])
    file.save_document_triples(full_adj)


if __name__ == '__main__':
    create_doc2doc_edges()
