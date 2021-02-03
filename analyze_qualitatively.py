from collections import Counter
from tqdm import tqdm
from analyze_results import get_latex_code
from helper import file_utils as file
import pandas as pd


def get_detailed_relations(id1, id2, dataset):
    filtered_triples = file.get_filtered_triples(dataset)  # Triples
    all_entities = file.get_entity2id(dataset)
    all_relations = file.get_all_relations()
    ids = file.get_doc2id(dataset)

    doc_nouns_norm = file.get_normalized_nouns(dataset)  # Array with all nouns per doc // must be split
    nouns1 = doc_nouns_norm[id1]
    nouns2 = doc_nouns_norm[id2]
    all_nouns = [nouns1, nouns2]

    triples = []
    triples_detail = []
    indices = [id1, id2]
    for noun_index, doc in enumerate(all_nouns):
        doc_index = indices[noun_index]
        if doc == "":
            continue

        # All ID's of the normalized nouns in the current document
        doc_ids = ids[ids["doc"] == doc_index]["wikiID"].tolist()
        assert len(doc_ids) <= len(doc.split(" ")), f"{len(doc.split(' '))} vs. {len(doc_ids)} in {dataset}"

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

                if not (doc_id == id2 and doc_index == id1):
                    continue

                triples_detail.append([entity1, relation, entity2, doc_index, doc_id])

                if doc_id in doc_pointers:
                    doc_pointers[doc_id].append(relation)
                else:
                    doc_pointers[doc_id] = [relation]

        for key in doc_pointers.keys():
            # Filter out all docs with length below 2
            if len(doc_pointers[key]) > 1:
                triples.append([doc_index, key, len(doc_pointers[key]), "+".join(doc_pointers[key])])

    assert len(triples) == 1
    triples = triples[0]
    doc1 = triples[0]
    doc2 = triples[1]

    check = file.get_document_triples(dataset)
    selected = check[(check["doc1"] == doc1) & (check["doc2"] == doc2)]

    detailed_results = pd.DataFrame(triples_detail, columns=["entity1", "relation", "entity2", "doc1", "doc2"])

    assert detailed_results.shape[0] == selected["relations"].tolist()[0]
    assert detailed_results["relation"].tolist() == selected["detail"].tolist()[0].split("+")

    triples_readable = []
    for index, row in detailed_results.iterrows():
        assert row["doc1"] == id1 and row["doc2"] == id2

        word1 = all_entities[all_entities["wikiID"] == row["entity1"]]["word"].tolist()
        assert len(word1) > 0

        word2 = all_entities[all_entities["wikiID"] == row["entity2"]]["word"].tolist()
        assert len(word2) > 0

        relation_detail = all_relations[all_relations["ID"] == row["relation"]]["label"].tolist()
        assert len(relation_detail) == 1
        relation_detail = relation_detail[0]

        triples_readable.append([", ".join(word1), relation_detail, ", ".join(word2)])

    readable_triples = pd.DataFrame(triples_readable, columns=["entity1", "relation", "entity2"])

    is_equal, stats = get_relation_statistics(id1, id2, readable_triples, detailed_results, dataset)
    return is_equal, stats


def get_relation_statistics(id1, id2, readable_triples, detailed_triples, dataset):
    labels = file.get_labels(dataset)
    label1 = labels[id1].split("\t")[2]
    label2 = labels[id2].split("\t")[2]

    relation_stats = Counter(detailed_triples["relation"])
    # print(label1, label2)
    return label1 == label2, relation_stats


def analyze_all(n, edge_type, dataset):
    # metrics = file.get_document_triples_metrics(dataset)
    # subset = metrics.nlargest(1000, edge_type)  # Include all with sme count with `keep='all'`
    # largest = subset.sort_values(by=[edge_type], ascending=False)

    # if not exists(io.get_ordered_document_triples_metrics_path(edge_type, dataset)):
    save_ordered_file(dataset, edge_type)

    largest = file.get_ordered_document_triples_metrics(edge_type, dataset)

    true_dict = {}
    false_dict = {}
    equality = []
    all_stats = []
    true_counter = 0
    false_counter = 0
    for index, row in largest.iterrows():
        id1 = int(row["doc1"])
        id2 = int(row["doc2"])

        is_equal, stats = get_detailed_relations(id1=id1, id2=id2, dataset=dataset)

        if is_equal and true_counter < n:
            true_dict = sum_counters(true_dict, stats)
            equality.append(is_equal)
            true_counter += 1

        elif not is_equal and false_counter < n:
            false_dict = sum_counters(false_dict, stats)
            equality.append(is_equal)
            false_counter += 1

        elif true_counter == n and false_counter == n:
            break
        else:
            continue

        all_stats.append([is_equal, stats])

    assert true_counter == n and false_counter == n, f"True:{true_counter}, False: {false_counter}"
    assert len(equality) == 2*n
    result = Counter(equality)
    total = ((result[True]) / ((result[False]) + (result[True]))) * 100
    print(f"Correct for {edge_type} in {dataset}: {total}% of {(result[False]) + (result[True])}")

    header = ["relation", "count"]
    all_true_rows = [[key, true_dict[key]] for key in true_dict.keys()]
    get_latex_code(header, all_true_rows, "lc", f"{dataset}_{edge_type}_true_relations.txt", dataset,
                   desc=f"Most common WikiData relations between documents with same label in the {dataset} dataset")

    all_false_rows = [[key, false_dict[key]] for key in false_dict.keys()]
    get_latex_code(header, all_false_rows, "lc", f"{dataset}_{edge_type}_false_relations.txt", dataset,
                   desc=f"Most common WikiData relations between documents with different label in the {dataset} dataset")

    return all_true_rows, all_false_rows


def sum_counters(dictionary, counter):
    for key in counter.keys():
        number = counter[key]
        if key in dictionary:
            dictionary[key] += number
        else:
            dictionary[key] = number
    ordered_dict = {k: dictionary[k] for k in sorted(dictionary, key=dictionary.get, reverse=True)}
    return ordered_dict


def get_number_of_relations(dataset):
    triples = file.get_document_triples(dataset)
    all_properties = file.get_all_relations()

    all_relations = []

    with tqdm(total=triples.shape[0]) as bar:
        for index, row in triples.iterrows():
            [all_relations.append(rel) for rel in row["detail"].split("+")]
            bar.update(1)

    counter = Counter(all_relations)

    results = pd.DataFrame.from_dict(counter, orient='index').reset_index()
    results.columns = ["relation", "count"]

    descriptions = []
    for index, row in results.iterrows():
        desc = all_properties[all_properties["ID"] == row["relation"]]["label"].tolist()
        assert len(desc) == 1
        descriptions.append(desc[0].title())

    results["description"] = descriptions
    results = results.sort_values(by="count", ascending=False).reset_index(drop=True).nlargest(15, columns="count")
    header = ["Relation", "Description", "Count"]
    results["count"] = results["count"].apply(lambda x: "{:,}".format(x))
    all_true_rows = [[row["relation"], row["description"], row["count"]] for index, row in results.iterrows()]
    get_latex_code(header, all_true_rows, "lll", f"{dataset}_top_relations.txt", dataset,
                   desc=f"Most common WikiData relations between in the {dataset} dataset")
    return all_true_rows


def get_dataset_statistics(dataset):
    docs = file.get_sentences(dataset)
    labels = file.get_labels(dataset)
    words = len(file.get_vocab(dataset))

    counter = Counter([t.split("\t")[1] for t in labels])
    labels = len(set([t.split("\t")[2] for t in labels]))

    entities = file.get_entity2id(dataset)
    entities = entities[~(entities["wikiID"] == "-1")]

    result = [dataset, len(docs), counter["train"], counter["test"], words, entities.shape[0], labels]
    result = [str(r) for r in result]
    print(" & ".join(result))


result_dict = {}


def perform_all(dataset, n=20):
    global result_dict
    true_count, false_count = analyze_all(n=n, edge_type="count", dataset=dataset)
    true_idf, false_idf = analyze_all(n=n, edge_type="idf", dataset=dataset)
    true_idf_wiki, false_idf_wiki = analyze_all(n=n, edge_type="idf_wiki", dataset=dataset)
    tmp_dict = {
        "count": {True: true_count, False: false_count},
        "idf": {True: true_idf, False: false_idf},
        "idf_wiki": {True: true_idf_wiki, False: false_idf_wiki}
        }
    result_dict[dataset] = tmp_dict


def analyze_results_dict():
    global result_dict
    edge_types = ["count", "idf", "idf_wiki"]
    all_commons = []
    all = []
    for dataset in result_dict.keys():

        filtered_true = list(filter(lambda x: x[1] > 1, result_dict[dataset][edge_types[0]][True]))
        filtered_false = list(filter(lambda x: x[1] > 1, result_dict[dataset][edge_types[0]][False]))

        type_true = set([x[0] for x in filtered_true])
        type_false = set([y[0] for y in filtered_false])

        commons = list(type_true.intersection(type_false))
        print(commons)
        all_commons.append(commons)
        [all.append(x) for x in commons]

    print(list(set(all_commons[0]).intersection(all_commons[1], all_commons[2])))
    print(Counter(all))


def save_ordered_file(dataset, edge_type):
    metrics = file.get_document_triples_metrics(dataset)
    subset = metrics.nlargest(5000, edge_type)  # Include all with sme count with `keep='all'`
    file.save_ordered_document_triples_metrics(subset, edge_type, dataset)


if __name__ == '__main__':
    for dataset in ["r52", "r8", "mr", "ohsumed"]:
        # perform_all(dataset)
        get_number_of_relations(dataset)

    # analyze_results_dict()

