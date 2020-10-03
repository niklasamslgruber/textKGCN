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

from config import FLAGS
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
    # Make sure to add the WHOLE matrix to the model graph
    setup_triples()
    vocab_ids = file.get_entity2id()
    filtered_triples = get_triples(filtered=True)
    docs = get_documents()

    sizes = []
    triples = []

    current_document = 0
    with tqdm(total=sum(range(1, len(docs)))) as bar:
        for doc in docs:

            # Get Id's of every word in document
            ids = vocab_ids[vocab_ids["word"].isin(doc)]["wikiID"].to_numpy()
            assert len(set(doc)) == len(ids)
            current_triples = filtered_triples["entity1"].isin(ids)
            current_triples2 = filtered_triples["entity2"].isin(ids)

            # Helper variables
            current_sub_doc = 0

            for sub_doc in docs:
                # Skip relations to itself and docs already covered (matrix is symmetric)
                if current_sub_doc <= current_document:
                    current_sub_doc += 1
                    continue
                # Get ID's of other document
                sub_ids = vocab_ids[vocab_ids["word"].isin(sub_doc)]["wikiID"].to_numpy()
                # Check if there are any relation between doc and sub_doc
                relation_to_subdoc = filtered_triples[current_triples & filtered_triples["entity2"].isin(sub_ids)]
                # Check if there are any relations between sub_doc and doc
                relation_to_subdoc2 = filtered_triples[current_triples2 & filtered_triples["entity1"].isin(sub_ids)]

                number_of_relations = relation_to_subdoc.shape[0] + relation_to_subdoc2.shape[0]
                sizes.append(number_of_relations)

                # Add non-zero triples to document triple
                if not number_of_relations == 0:
                    triple = [current_document, current_sub_doc, int(number_of_relations), relation_to_subdoc["relation"].tolist(), relation_to_subdoc2["relation"].tolist()]
                    triples.append(triple)

                current_sub_doc += 1
                bar.update(1)

            # Next document
            current_document += 1

    assert len(sizes) == sum(range(1, current_document))

    print(f"Highest number of relations between two docs: {max(sizes)}")
    print(f"Created {2 * len(triples)} doc2doc edges")

    data = pd.DataFrame(triples)
    data.to_pickle(f"{FLAGS.dataset}_document_triples.pickle")

    save_full_matrix(data)


def save_full_matrix(dataframe):
    # Mirrors the generated half adjacency matrix to a full symmetrical adjacency matrix
    columns = dataframe.columns.tolist()
    new_columns = [columns[1], columns[0], columns[2], columns[4], columns[3]]
    mirrored_frame = dataframe.copy()
    mirrored_frame.columns = new_columns

    full_adj = dataframe.append(mirrored_frame)
    assert full_adj.shape == (2 * dataframe.shape[0], dataframe.shape[1])
    file.save_document_triples(full_adj)


if __name__ == '__main__':
    create_doc2doc_edges()
