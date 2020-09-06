import requests


class WikiDataItem:

    # An WikiData item returned from the API (can be entitiy or property)
    def __init__(self, search_word, identifier, json_data):
        self.search_word = search_word
        self.entity = json_data
        self.identifier = identifier

        self.title = self.get(["title"])
        self.wikiId = self.get(["id"])
        self.labels = self.get(["labels", "en", "value"])
        self.description = self.get(["descriptions", "en", "value"])

        self.aliases = self.__get_aliases()
        self.relations = self.__get_relations()

    def __str__(self):
        return f"Item for searchword `{self.search_word}`: \n" \
               f"ID: {self.identifier}\n" \
               f"Labels: {self.labels}\n" \
               f"Description: {self.description}\n" \
               f"Aliases: {self.aliases}\n" \
               f"#Relations: {len(self.relations.keys())}"

    def __get_aliases(self):
        return list(map(lambda item: get_safely(item, ["value"]), self.get(["aliases", "en"])))

    def __get_relations(self):
        rel_dict = {}
        for relation in self.get(["claims"]):
            for item in self.get(["claims", relation]):
                property_id = get_safely(item, ["mainsnak", "property"])
                value = get_safely(item, ["mainsnak", "datavalue", "value"])
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
            "relations": self.relations if self.identifier.startswith("Q") else {}
            }
        return json_dict

    def get(self, path_array):
        return get_safely(self.entity, path_array)


def get_safely(dictionary, path_array):
    # Safely unwrapps a nested dictionary
    value = dictionary
    for path in path_array:
        value = value.get(path, {})
    return value


def download_by_title(title):
    url = "https://www.wikidata.org/w/api.php?format=json&action=wbgetentities" \
          "&languages=en" \
          "&normalize=yes" \
          "&sites=enwiki" \
          f"&titles={title}"
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
