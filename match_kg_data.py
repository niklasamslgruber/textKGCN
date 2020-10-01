import json
from itertools import chain
from os.path import isfile
import pandas as pd
from tqdm import tqdm
import io_utils as io
from config import FLAGS
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
    write_json(path, data_dict, stats_collector)


def create_vocabulary_entities():
    print("Creating entities for vocabulary...")

    # Load all words from vocabulary
    entities = get_all_vocab_words()
    create_json(entities, download_entity, io.get_vocab_entities_path(FLAGS.dataset))
    print("Entity downloading finished")
    # Create JSON with all relations from previously initialized entities
    create_vocabulary_relations()


def create_vocabulary_relations():
    print("Creating relations for vocabulary...")

    # Load all relations
    relations = get_all_relations()
    create_json(relations, download_relation, io.get_vocab_relations_path(FLAGS.dataset))


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
    entities = read_json_file(io.get_vocab_entities_path(FLAGS.dataset))
    for entity in entities.values():
        relations = get_safely(entity, ["relations"]).keys()
        all_relations.append(relations)

    unique_relations = list(dict.fromkeys(chain.from_iterable(all_relations)))
    return unique_relations


def get_all_vocab_words():
    # Gets all words in the vocabulary
    return read_txt_file(io.get_vocab_path(FLAGS.dataset))


# JSON Lookups

def find_entity(entity_name):
    # Searches for given `entity_name` in JSON file
    global entity_dict
    if len(entity_dict) > 0:
        json_dict = entity_dict
    else:
        json_dict = read_json_file(io.get_vocab_entities_path(FLAGS.dataset))
        entity_dict = json_dict
    return json_dict.get(entity_name, {})


def find_relation(relation_id):
    # Searches for given `relation_id` in JSON file
    global relation_dict
    if len(relation_dict) > 0:
        json_dict = relation_dict
    else:
        json_dict = read_json_file(io.get_vocab_relations_path(FLAGS.dataset))
        relation_dict = json_dict
    return json_dict.get(relation_id, {})


# Entity Mappings

def create_entity_mappings():
    all_entities = read_json_file(io.get_vocab_entities_path(FLAGS.dataset))
    mappings = []
    for entity in all_entities.keys():
        mappings.append([entity, all_entities[entity]["id"]])

    write_csv(io.get_entity2id_path(FLAGS.dataset), mappings)


# File reader / writer

def write_json(path, data, stats_collector):
    # Write to .json file
    with open(path, "w") as output:
        json.dump(data, output, indent=4)
    output.close()

    print(f"Wrote JSON with {len(data.keys())} elements {stats_collector.get_output()}")


def write_csv(path, array):
    data = pd.DataFrame(array)
    data.to_csv(path, index=False, header=False, sep=",")


def read_txt_file(path):
    # Read .txt file
    data = []
    if isfile(path):
        file = open(path, "rb")
        for line in file.readlines():
            data.append(line.strip().decode())
        file.close()
    return data


def read_json_file(path):
    # Read .json file
    json_dict = {}
    if isfile(path):
        with open(path, "r") as output:
            json_dict = json.load(output)
        output.close()
    return json_dict


def create_wiki_mappings():
    # Creates files with all entities and their relations from dataset
    create_vocabulary_entities()
    create_entity_mappings()


if __name__ == '__main__':
    create_wiki_mappings()
