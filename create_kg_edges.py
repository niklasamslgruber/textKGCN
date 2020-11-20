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
from helper import file_utils as file, io_utils as io
from loader.wiki_api import get_safely
from os.path import exists


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
        triples_in = filtered_triples[filtered_triples["entity2"].isin(doc_ids)]
        triples_in.columns = ["entity2", "relations", "entity1"]
        triples_total = pd.concat([triples_out, triples_in])

        all_outgoing_relations = triples_total["relations"].tolist()
        if len(all_outgoing_relations) == 0:
            all_outgoing_relations = "-"
        relations_array.append(all_outgoing_relations)

    file.save_doc2relations([" ".join(elem) for elem in relations_array])


# Adjacency matrices
def create_doc2doc_edges():
    # if exists(io.get_document_triples_path()):
    #     print("Document triples pickle file adready exists, will not be created again")
    #     generate_idf_scores()
    #     apply_idf()
    #     return
    generate_doc2relations()
    generate_idf_scores()
    doc_nouns_norm = file.get_normalized_nouns()  # Array with all nouns per doc // must be split
    filtered_triples = get_triples(filtered=True)  # Triples
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
            assert len(doc_ids) <= len(doc.split(" ")), f"{len(doc.split(' '))} vs. {len(doc_ids)}"

            # Graph edges pointing to other entities
            triples_out = filtered_triples[filtered_triples["entity1"].isin(doc_ids)]
            triples_in = filtered_triples[filtered_triples["entity2"].isin(doc_ids)]
            triples_in.columns = ["entity2", "relations", "entity1"]

            triples_total = pd.concat([triples_out, triples_in])

            doc_pointers = {}
            for index, row in triples_total.iterrows():
                entity1 = row["entity1"]
                relation = row["relations"]
                entity2 = row["entity2"]
                # Look in which documents entity2 appears
                pointer = ids[ids["wikiID"] == entity2]["doc"].tolist()
                assert entity1 in doc_ids

                for doc_id in pointer:
                    # Ignore doc2doc edges to doc itself
                    if doc_id <= doc_index:
                        continue

                    if doc_id in doc_pointers:
                        doc_pointers[doc_id].append(relation)
                    else:
                        doc_pointers[doc_id] = [relation]

            for key in doc_pointers.keys():
                # Filter out all docs with length below 2
                if len(doc_pointers[key]) > 1:
                    triples.append([doc_index, key, len(doc_pointers[key]), "+".join(doc_pointers[key])])

            bar.update(1)

    data = pd.DataFrame(triples)
    data.columns = ["doc1", "doc2", "relations", "detail"]
    print(f"Highest number of relations between two docs: {max(data['relations'])}")
    print(f"Created {len(triples)} doc2doc edges (filtered by threshold: {filtered_out_items})")
    file.save_document_triples(data)
    apply_idf()


def generate_idf_scores():
    print("Generate IDF scores...")
    doc_relations = file.get_doc2relations()
    num_docs = len(doc_relations)
    doc_word_freq = defaultdict(int)
    relation_doc_freq = {}
    relation_doc_freq_wiki = {}
    relations_in_docs = defaultdict(set)
    row = []
    col = []
    weight = []
    weight_wiki = []

    for i, rels in enumerate(doc_relations):
        relations = rels.split()
        for rel in relations:
            relations_in_docs[rel].add(i)
            doc_word_str = (i, rel)
            doc_word_freq[doc_word_str] += 1

    all_relations = file.get_all_relations()

    for rel, doc_list in relations_in_docs.items():
        count = all_relations[all_relations["ID"] == rel]["count"].tolist()
        assert len(count) <= 1, (count, rel)
        if len(count) == 1:
            relation_doc_freq_wiki[rel] = count[0]
        else:
            relation_doc_freq_wiki[rel] = 0
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
            # TODO: Query current number of entities on WikiData
            # Source: https://www.wikidata.org/wiki/Wikidata:Statistics on 30.10.2020 at 11:41
            idf_wiki = log(1.0 * 90450399 / relation_doc_freq[rel])

            weight.append(freq * idf)
            weight_wiki.append(freq * idf_wiki)
            doc_rel_set.add(rel)

    data = pd.DataFrame({"doc": row, "relation": col, "idf": weight, "idf_wiki": weight_wiki})
    file.save_doc2idf(data)


def apply_idf():
    print("Applying IDF...")
    doc_triples = file.get_document_triples()
    idf = file.get_doc2idf()
    data = []
    with tqdm(total=doc_triples.shape[0]) as bar:
        for index, row in doc_triples.iterrows():
            doc1 = row["doc1"]
            doc2 = row["doc2"]
            relations = row["detail"].split("+")
            score = 0
            wiki_score = 0
            for rel in relations:
                scores = idf[(idf["relation"] == rel) & (idf["doc"] == doc1)][["idf", "idf_wiki"]]
                idf_score = scores["idf"].tolist()
                idf_wiki_score = scores["idf_wiki"].tolist()
                assert len(idf_score) == 1 and len(idf_wiki_score) == 1
                score += idf_score[0]
                wiki_score += idf_wiki_score[0]
            data.append([doc1, doc2, len(relations), score, wiki_score])
            bar.update(1)

    dataframe = pd.DataFrame(data)
    dataframe.columns = ["doc1", "doc2", "count", "idf", "idf_wiki"]
    file.save_document_triples_metrics(dataframe)


if __name__ == '__main__':
    create_doc2doc_edges()
