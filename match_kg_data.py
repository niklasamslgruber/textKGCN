from itertools import chain
import pandas as pd
from tqdm import tqdm
import io_utils as io
from wiki_api import download_by_title, get_safely, download_by_id


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

def create_json(iterable, download_function, path):
    data_dict = {}
    stats_collector = APIStatsCollector()

    with tqdm(total=len(iterable)) as bar:
        for identifier in iterable:
            item = download_function(identifier, stats_collector)
            data_dict[identifier] = item
            bar.update(1)

    # Write to JSON file
    io.write_json(path, data_dict)
    print(f"Wrote JSON with {len(data_dict.keys())} elements {stats_collector.get_output()}")


def create_vocabulary_entities():
    print("Creating entities for vocabulary...")

    # Load all words from vocabulary
    entities = get_all_vocab_words()
    create_json(entities, download_entity, io.get_vocab_entities_path())
    print("Entity downloading finished")
    # Create JSON with all relations from previously initialized entities
    create_vocabulary_relations()


def create_vocabulary_relations():
    print("Creating relations for vocabulary...")

    # Load all relations
    relations = get_all_relations()
    create_json(relations, download_relation, io.get_vocab_relations_path())


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
    entities = io.read_json(io.get_vocab_entities_path())

    for entity in entities.values():
        relations = get_safely(entity, ["relations"]).keys()
        all_relations.append(relations)

    unique_relations = list(dict.fromkeys(chain.from_iterable(all_relations)))
    return unique_relations


def get_all_vocab_words():
    # Gets all words in the vocabulary
    return io.read_txt(io.get_vocab_path())


# JSON Lookups

def find_entity(entity_name):
    # Searches for given `entity_name` in JSON file
    global entity_dict
    if len(entity_dict) > 0:
        json_dict = entity_dict
    else:
        json_dict = io.read_json(io.get_vocab_entities_path())
        entity_dict = json_dict
    return json_dict.get(entity_name, {})


def find_relation(relation_id):
    # Searches for given `relation_id` in JSON file
    global relation_dict
    if len(relation_dict) > 0:
        json_dict = relation_dict
    else:
        json_dict = io.read_json(io.get_vocab_relations_path())
        relation_dict = json_dict
    return json_dict.get(relation_id, {})


# Entity Mappings

def create_entity_mappings():
    all_entities = io.read_json(io.get_vocab_entities_path())
    mappings = []
    for entity in all_entities.keys():
        mappings.append([entity, all_entities[entity]["id"]])

    write_csv(io.get_entity2id_path(), mappings)


# File reader / writer

def write_csv(path, array):
    data = pd.DataFrame(array)
    data.to_csv(path, index=False, header=False, sep=",")


def create_wiki_mappings():
    # Creates files with all entities and their relations from dataset
    create_vocabulary_entities()
    create_entity_mappings()


if __name__ == '__main__':
    create_wiki_mappings()
