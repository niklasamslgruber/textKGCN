import json
from utils import get_corpus_path, get_kg_data_path
from wiki_api import download_by_title, get_safely


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
    failed_counter = 0
    api_call_counter = 0

    entities = entities[0:5]
    for entity_name in entities:
        # Check if entity already included in JSON to reduce API calls
        if not overwrite:
            identifier, json_data = get_data_of_title(entity_name)
            if bool(json_data):
                json_dict[identifier] = json_data
                already_downloaded_counter += 1
                continue

        # Make API call if not already saved
        print(f"API call for `{entity_name}`")
        items = download_by_title(title=entity_name)
        api_call_counter += 1

        for item in items:
            if item.identifier != "-1":
                json_dict[item.identifier] = item.to_json()
            else:
                # If identifier is "-1" (not found) save search_word as key
                failed_counter += 1
                json_dict[item.search_word] = item.to_json()

    # Write to JSON file
    with open(f"{get_kg_data_path()}/graphs/vocab_entities.json", "w") as output:
        json.dump(json_dict, output, indent=4)
    output.close()

    print(f"Wrote JSON with {len(json_dict.keys())} elements "
          f"(unsuccessful: {failed_counter}, "
          f"cached: {already_downloaded_counter}, "
          f"API calls: {api_call_counter})")


def load_json():
    with open(f"{get_kg_data_path()}/graphs/vocab_entities.json", "r") as output:
        json_dict = json.load(output)
    output.close()
    return json_dict


def get_id_of_title(title):
    json_dict = load_json()
    for entity_id in json_dict:
        value = get_safely(json_dict, [entity_id, "searchword"])
        if value == title:
            return entity_id
    return None


def get_data_of_id(wiki_id):
    json_dict = load_json()
    return json_dict.get(wiki_id, {})


def get_data_of_title(title):
    identifier = get_id_of_title(title)
    return identifier, get_data_of_id(identifier)

def get_all_relations():
    json_dict = load_json()


def main():
    create_vocabulary_entities()


if __name__ == '__main__':
    main()
    # print(find_id("Q48340"))
