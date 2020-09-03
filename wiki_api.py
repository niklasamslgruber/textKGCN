import requests
from collections.abc import Mapping


class WikiDataItem:

    def __init__(self, search_word, identifier, json_data):
        self.search_word = search_word
        self.entity = json_data
        self.identifier = identifier
        self.title = "" #self.entity["title"]""
        self.wikiId = "" # self.entity["id"]
        self.labels = self.__get_labels()
        self.description = self.__get_description()
        self.aliases = self.__get_aliases()
        self.relations = self.__get_relations()

    def __str__(self):
        return f"Item for searchword `{self.search_word}`: \n" \
               f"ID: {self.identifier}\n" \
               f"Description: {self.description} \n" \
               f"Labels: {self.labels} \n" \
               f"Aliases: {self.aliases} \n" \
               f"#Properties: {len(self.relations)}"

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

    def __get_relations(self):
        rel_dict = {}
        for relation in self.entity.get("claims", {}):
            for item in self.entity["claims"][relation]:
                property_id = item["mainsnak"]["property"]
                value = item.get("mainsnak", {}).get("datavalue", {}).get("value", {})
                rel_dict[property_id] = value
        return rel_dict

    def to_json(self):
        json_dict = {
            "searchword": self.search_word,
            "id": self.identifier,
            "title": self.title,
            "wikiId": self.wikiId,
            "labels": self.labels,
            "descriptions": self.description,
            "aliases": self.aliases,
            "relations": self.relations
            }
        return json_dict


def download_by_title(title):
    url = "https://www.wikidata.org/w/api.php?format=json&action=wbgetentities" \
          "&languages=en" \
          "&normalize=yes" \
          "&sites=enwiki" \
          f"&titles={title}"
    print(url)
    entities = download_entities(url, title)
    return entities


def download_by_id(key):
    url = "https://www.wikidata.org/w/api.php?format=json&action=wbgetentities" \
          "&languages=en" \
          "&sites=enwiki" \
          f"&ids={key}"
    entities = download_entities(url, key)
    return entities


def download_entities(url, search_word):
    try:
        request = requests.get(url)

        json_data = request.json()
        entities = json_data["entities"]
        items = list(map(lambda key: WikiDataItem(search_word, key, entities[key]), entities.keys()))
        return items
    except requests.exceptions.InvalidSchema:
        print(f"Failed to load data for `{search_word}`")
