import json
from utils import get_corpus_path, get_kg_data_path
from wiki_api import download_by_title


def create_vocabulary_entities():
    print("Starting to download from Wikidata API...")
    json_dict = {}
    path = f'{get_corpus_path()}/twitter_asian_prejudice_small_vocab.txt'

    file = open(path, 'rb')
    entities = []
    for line in file.readlines():
        entities.append(line.strip().decode())
    file.close()

    entities = entities[0:1]
    for entity_name in entities:
        items = download_by_title(title=entity_name)
        for item in items:
            json_dict[item.identifier] = item.to_json()

    with open(f"{get_kg_data_path()}/graphs/vocab_entities.json", "w") as output:
        json.dump(json_dict, output, indent=4)

    print(f"Wrote JSON for {len(json_dict.keys())} elements (unsuccessful: {(list(json_dict.keys()).count('-1'))})")


def main():
    create_vocabulary_entities()


if __name__ == '__main__':
    main()
