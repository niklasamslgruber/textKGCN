import json
from itertools import chain

from utils import get_corpus_path, get_kg_data_path
from wiki_api import download_by_title, get_safely, download_by_id

# TODO:
# * Move cache checker to WikiAPI
# * Create StatsCollector which tracks unsuccesful, cache and API calls



def create_vocabulary_entities(overwrite=False):
    print("Starting to download from Wikidata API...")
    json_dict = {}
    path = f'{get_corpus_path()}/twitter_asian_prejudice_small_vocab.txt'

    file = open(path, 'rb')
    entities = []
    for line in file.readlines():
        entities.append(line.strip().decode())
    file.close()

    # Stats
    already_downloaded_counter = 0
    api_call_counter = 0

    entities = entities[1:2]
    for entity_name in entities:
        # Check if entity already included in JSON to reduce API calls
        if not overwrite:
            json_data = get_entity(entity_name)
            if bool(json_data):
                json_dict[entity_name] = json_data
                already_downloaded_counter += 1
                continue

        # Make API call if not already saved
        print(f"API call for `{entity_name}`")
        items = download_by_title(title=entity_name)
        api_call_counter += 1

        for item in items:
            json_dict[entity_name] = item.to_json()

    # Write to JSON file
    with open(f"{get_kg_data_path()}/graphs/vocab_entities.json", "w") as output:
        json.dump(json_dict, output, indent=4)
    output.close()

    print(f"Wrote JSON with {len(json_dict.keys())} elements "
          f"(cached: {already_downloaded_counter}, "
          f"API calls: {api_call_counter})")


def load_entity_json():
    with open(f"{get_kg_data_path()}/graphs/vocab_entities.json", "r") as output:
        json_dict = json.load(output)
    output.close()
    return json_dict


def load_relation_json():
    with open(f"{get_kg_data_path()}/graphs/vocab_relations.json", "r") as output:
        json_dict = json.load(output)
    output.close()
    return json_dict


def get_entity(word):
    json_dict = load_entity_json()
    return json_dict.get(word, {})


def get_relation(word):
    json_dict = load_relation_json()
    return json_dict.get(word, {})


def get_all_relations(overwrite=False):
    relations = []
    json_dict = load_entity_json()
    for identifier in json_dict.values():
        value = get_safely(identifier, ["relations"]).keys()
        relations.append(value)

    # Convert 2D array to 1D array of unique relations
    relations = list(set(list(chain.from_iterable(relations))))
    relation_dict = {}
    already_downloaded_counter = 0
    api_call_counter = 0

    for relation_id in relations:

        if not overwrite:
            json_data = get_relation(relation_id)
            if bool(json_data):
                relation_dict[relation_id] = json_data
                already_downloaded_counter += 1
                continue
        items = download_by_id(relation_id)
        api_call_counter += 1
        for item in items:
            relation_dict[relation_id] = item.to_json()

    with open(f"{get_kg_data_path()}/graphs/vocab_relations.json", "w") as output:
        json.dump(relation_dict, output, indent=4)
    output.close()

    print(f"Wrote Relation JSON with {len(relation_dict.keys())} elements "
          f"(cached: {already_downloaded_counter}, "
          f"API calls: {api_call_counter})")


def main():
    create_vocabulary_entities()


if __name__ == '__main__':
    main()
    get_all_relations()