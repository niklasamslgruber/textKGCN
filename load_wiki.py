import requests
from utils import get_corpus_path, get_kg_data_path
import json


class GraphItem:

    def __init__(self, search_word, key, json):
        self.search_word = search_word
        self.key = key
        self.entity = json
        self.description = self.__get_description()
        self.labels = self.__get_labels()
        self.aliases = self.__get_aliases()
        self.properties = self.__get_properties()

    def __str__(self):
        return f"Item for searchword `{self.search_word}`: \n" \
               f"ID: {self.key}\n" \
               f"Description: {self.description} \n" \
               f"Labels: {self.labels} \n" \
               f"Aliases: {self.aliases} \n" \
               f"#Properties: {len(self.properties)}"

    def __get_description(self):
        try:
            return self.entity["descriptions"]["en"]["value"]
        except:
            return "(Empty)"

    def __get_labels(self):
        try:
            return self.entity["labels"]["en"]["value"]
        except:
            return "(Empty)"

    def __get_aliases(self):
        try:
            return list(map(lambda item: item["value"], self.entity["aliases"]["en"]))
        except:
            return []

    def __get_properties(self):
        try:
            return self.entity["claims"]
        except:
            return []


def load_data_for(title):
    # TODO: Check WikiData @IBM tutorial
    url = "https://www.wikidata.org/w/api.php?format=json&action=wbgetentities" \
          "&languages=en" \
          "&normalize=yes" \
          "&sites=enwiki" \
          f"&titles={title}"
    # try:
    request = requests.get(url)

    json_data = request.json()
    entities = json_data["entities"]
    items = list(map(lambda key: GraphItem(title, key, entities[key]), entities.keys()))
    return items


def create_entities_for_vocab():
    print("Starting to download from Wikidata API...")
    json_dict = {}
    path = f'{get_corpus_path()}/twitter_asian_prejudice_small_vocab.txt'

    file = open(path, 'rb')
    entities = []
    for line in file.readlines():
        entities.append(line.strip().decode())
    file.close()

    entities = entities[0:5]
    for entity_name in entities:
        items = load_data_for(entity_name)
        for item in items:
            json_dict[item.key] = item.entity

    with open(f"{get_kg_data_path()}/graphs/vocab_nodes.json", "w") as output:
        json.dump(json_dict, output, indent=4)

    print(f"Wrote JSON for {len(json_dict.keys())} elements (unsuccessful: {(list(json_dict.keys()).count('-1'))})")


def main():
    create_entities_for_vocab()


if __name__ == '__main__':
    main()
