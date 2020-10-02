from itertools import chain
from tqdm import tqdm
from loader.wiki_api import download_by_title, get_safely, download_by_id
from helper import file_utils as file


class APIStatsCollector:

    def __init__(self):
        self.api_calls = 0
        self.cached_items = 0
        self.failed_calls = 0

    def api_call(self):
        # Tracks number of all API calls
        self.api_calls += 1

    def failed(self):
        # Tracks all failed API calls
        self.failed_calls += 1

    def cached(self):
        # Tracks all prevented API calls due to cached data
        self.cached_items += 1

    def get_output(self):
        # Outputs statistics as string
        return f"(API calls: {self.api_calls}, " \
               f"failed: {self.failed_calls}, " \
               f"cached: {self.cached_items})"


# Vocab Processing

def create_json(iterable, download_function, json_writer):
    data_dict = {}
    stats_collector = APIStatsCollector()

    with tqdm(total=len(iterable)) as bar:
        for identifier in iterable:
            item = download_function(identifier, stats_collector)
            data_dict[identifier] = item
            bar.update(1)

    # Write to JSON file
    json_writer(data_dict)
    print(f"Wrote JSON with {len(data_dict.keys())} elements {stats_collector.get_output()}")


def create_vocabulary_entities():
    print("Creating entities for vocabulary...")

    # Load all words from vocabulary
    entities = file.get_vocab()
    create_json(entities, download_entity, file.save_vocab_entities)
    print("Entity downloading finished")
    # Create JSON with all relations from previously initialized entities
    create_vocabulary_relations()


def create_vocabulary_relations():
    print("Creating relations for vocabulary...")

    # Load all relations
    relations = get_all_relations()
    create_json(relations, download_relation, file.save_vocab_relations)


# API Downloader

def download_entity(entity_name, stats_collector):
    return download(entity_name, find_entity, download_by_title, stats_collector)


def download_relation(relation_id, stats_collector):
    return download(relation_id, find_relation, download_by_id, stats_collector)


def download(search_word, lookup_function, download_function, stats_collector):
    data = lookup_function(search_word)
    if len(data) == 0:
        stats_collector.api_call()
        entity = download_function(search_word)[0]
        if entity.identifier == "-1":
            stats_collector.failed()
        data = entity.to_json()
    else:
        stats_collector.cached()
    return data


# JSON Reader

# Dictionary from JSON to avoid reading multiple times
entity_dict = {}
relation_dict = {}


def get_all_relations():
    # Gets all relations for current vocabulary
    all_relations = []
    entities = file.get_vocab_entities()

    for entity in entities.values():
        relations = get_safely(entity, ["relations"]).keys()
        all_relations.append(relations)

    unique_relations = list(dict.fromkeys(chain.from_iterable(all_relations)))
    return unique_relations


# JSON Lookups

def find_entity(entity_name):
    # Searches for given `entity_name` in JSON file
    global entity_dict
    if len(entity_dict) > 0:
        json_dict = entity_dict
    else:
        json_dict = file.get_vocab_entities()
        entity_dict = json_dict
    return json_dict.get(entity_name, {})


def find_relation(relation_id):
    # Searches for given `relation_id` in JSON file
    global relation_dict
    if len(relation_dict) > 0:
        json_dict = relation_dict
    else:
        json_dict = file.get_vocab_relations()
        relation_dict = json_dict
    return json_dict.get(relation_id, {})


# Entity Mappings

def create_entity_mappings():
    all_entities = file.get_vocab_entities()
    mappings = []
    for entity in all_entities.keys():
        mappings.append([entity, all_entities[entity]["id"]])

    file.save_entity2id(mappings)


def create_wiki_mappings():
    # Creates files with all entities and their relations from dataset
    create_vocabulary_entities()
    create_entity_mappings()


if __name__ == '__main__':
    create_wiki_mappings()
