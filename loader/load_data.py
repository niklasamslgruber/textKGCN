import gc
from os.path import join
import io_utils as io
from config import FLAGS
from loader.dataset import TextDataset
from model.build_graph import build_text_graph_dataset
from utils import load, save
import file_utils as file


def load_data():
    dir = join(io.get_cache_path(), 'split')
    dataset_name = FLAGS.dataset
    train_ratio = int(FLAGS.tvt_ratio[0] * 100)
    val_ratio = int(FLAGS.tvt_ratio[1] * 100)
    test_ratio = 100 - train_ratio - val_ratio
    if 'presplit' not in dataset_name:
        save_fn = '{}_train_{}_val_{}_test_{}_seed_{}_window_size_{}'.format(dataset_name, train_ratio,
                                                                             val_ratio, test_ratio,
                                                                             FLAGS.random_seed, FLAGS.word_window_size)
    else:
        save_fn = '{}_train_val_test_{}_window_size_{}'.format(dataset_name, FLAGS.random_seed, FLAGS.word_window_size)
    path = join(dir, save_fn)
    rtn = load(path)
    if rtn:
        train_data, val_data, test_data = rtn['train_data'], rtn['val_data'], rtn['test_data']
    else:
        train_data, val_data, test_data = _load_tvt_data_helper()
        save({'train_data': train_data, 'val_data': val_data, 'test_data': test_data}, path)

    raw_doc_list = file.get_sentences(dataset_name)

    return train_data, val_data, test_data, raw_doc_list


def _load_tvt_data_helper():
    dir = join(io.get_cache_path(), 'all')
    path = join(dir, FLAGS.dataset + '_all_window_' + str(FLAGS.word_window_size))
    rtn = load(path)
    if rtn:
        dataset = TextDataset(None, None, None, None, None, None, rtn)
    else:
        dataset = build_text_graph_dataset(FLAGS.dataset, FLAGS.word_window_size)
        gc.collect()
        save(dataset.__dict__, path)

    train_dataset, val_dataset, test_dataset = dataset.tvt_split(FLAGS.tvt_ratio[:2], FLAGS.tvt_list, FLAGS.random_seed)
    return train_dataset, val_dataset, test_dataset
