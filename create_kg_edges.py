"""
Create doc-doc edges

Steps:
1. Load all entities with their relations
2. Load relevant relations
3. Create adjacency matrix for word-word relations
4. Count number of relation between two documents
5. Weight relations and set a doc-doc edge weight
"""
from collections import defaultdict
from math import log
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


def generate_doc2relations():
    setup_triples()
    doc_nouns_norm = file.get_normalized_nouns()  # Array with all nouns per doc // must be split
    relations_array = []
    ids = file.get_doc2id()
    filtered_triples = get_triples(filtered=True)  # Triples

    for doc_index, doc in enumerate(doc_nouns_norm):
        if doc == "":
            relations_array.append("-")
            continue
        # All ID's of the normalized nouns in the current document
        doc_ids = ids[ids["doc"] == doc_index]["wikiID"].tolist()

        # Graph edges pointing to other entities
        triples_out = filtered_triples[filtered_triples["entity1"].isin(doc_ids)]
        all_outgoing_relations = triples_out["relations"].tolist()
        if len(all_outgoing_relations) == 0:
            all_outgoing_relations = "-"
        relations_array.append(all_outgoing_relations)

    file.save_doc2relations([" ".join(elem) for elem in relations_array])
    generate_idf_scores()


# Adjacency matrices
def create_doc2doc_edges():
    generate_doc2relations()
    doc_nouns_norm = file.get_normalized_nouns()  # Array with all nouns per doc // must be split
    filtered_triples = get_triples(filtered=True)  # Triples
    idf = file.get_doc2idf()
    ids = file.get_doc2id()
    triples = []
    filtered_out_items = 0
    with tqdm(total=len(doc_nouns_norm)) as bar:
        for doc_index, doc in enumerate(doc_nouns_norm):
            if doc == "":
                bar.update(1)
                continue

            # All ID's of the normalized nouns in the current document
            doc_ids = ids[ids["doc"] == doc_index]["wikiID"].tolist()

            # Graph edges pointing to other entities
            triples_out = filtered_triples[filtered_triples["entity1"].isin(doc_ids)]

            doc_pointers = {}
            for index, row in triples_out.iterrows():
                relation = row["relations"]
                entity2 = row["entity2"]
                pointer = ids[ids["wikiID"] == entity2]["doc"].tolist()
                for doc_id in pointer:
                    if doc_id in doc_pointers:
                        doc_pointers[doc_id].append(relation)
                    else:
                        doc_pointers[doc_id] = [relation]

            for key in doc_pointers:
                relations = doc_pointers[key]
                count = len(relations)
                score = 0
                for rel in relations:
                    idf_score = idf[(idf["relation"] == rel) & (idf["doc"] == doc_index)]["idf"].tolist()
                    assert len(idf_score) == 1
                    score += idf_score[0]
                triples.append([doc_index, key, count, "+".join(relations), score])
            bar.update(1)

    data = pd.DataFrame(triples)
    data.columns = ["doc1", "doc2", "relations", "detail", "idf"]
    print(f"Highest number of relations between two docs: {max(data['relations'])}")
    print(f"Created {len(triples)} doc2doc edges (filtered by threshold: {filtered_out_items})")
    file.save_document_triples(data)


def generate_idf_scores():
    print("Generate IDF scores...")
    doc_relations = file.get_doc2relations()
    num_docs = len(doc_relations)
    doc_word_freq = defaultdict(int)
    relation_doc_freq = {}
    relations_in_docs = defaultdict(set)
    row = []
    col = []
    weight = []

    for i, rels in enumerate(doc_relations):
        relations = rels.split()
        for rel in relations:
            relations_in_docs[rel].add(i)
            doc_word_str = (i, rel)
            doc_word_freq[doc_word_str] += 1

    for rel, doc_list in relations_in_docs.items():
        relation_doc_freq[rel] = len(doc_list)

    for i, rels in enumerate(doc_relations):
        relations = rels.split()
        doc_rel_set = set()
        for rel in relations:
            if rel in doc_rel_set or rel == "-":
                continue
            freq = doc_word_freq[(i, rel)]
            row.append(i)
            col.append(rel)
            idf = log(1.0 * num_docs / relation_doc_freq[rel])
            weight.append(freq * idf)
            doc_rel_set.add(rel)

    data = pd.DataFrame({"doc": row, "relation": col, "idf": weight})
    file.save_doc2idf(data)


if __name__ == '__main__':
    create_doc2doc_edges()
