import re
from collections import OrderedDict
from os import environ, makedirs
from os.path import dirname, expanduser, isfile, exists
from socket import gethostname
import klepto


def load(filepath, print_msg=True):
    fp = proc_filepath(filepath)
    if isfile(fp):
        return load_klepto(fp, print_msg)
    elif print_msg:
        print('Trying to load but no file {}'.format(fp))


def load_klepto(filepath, print_msg):
    rtn = klepto.archives.file_archive(filepath)
    rtn.load()
    if print_msg:
        print('Loaded from {}'.format(filepath))
    return rtn


def save(obj, filepath, print_msg=True):
    if type(obj) is not dict and type(obj) is not OrderedDict:
        raise ValueError('Can only _cache a dict or OrderedDict'
                         ' NOT {}'.format(type(obj)))
    fp = proc_filepath(filepath, ext='.klepto')
    create_dir_if_not_exists(dirname(filepath))
    save_klepto(obj, fp, print_msg)


def create_dir_if_not_exists(dir):
    if not exists(dir):
        makedirs(dir)


def save_klepto(dic, filepath, print_msg):
    if print_msg:
        print('Saving to {}'.format(filepath))
    klepto.archives.file_archive(filepath, dict=dic).dump()


def proc_filepath(filepath, ext='.klepto'):
    if type(filepath) is not str:
        raise RuntimeError('Did you pass a file path to this function?')
    return append_ext_to_filepath(ext, filepath)


def append_ext_to_filepath(ext, fp):
    if not fp.endswith(ext):
        fp += ext
    return fp


def parse_as_int_list(il):
    rtn = []
    for x in il.split('_'):
        x = int(x)
        rtn.append(x)
    return rtn


def get_user():
    try:
        home_user = expanduser("~").split('/')[-1]
    except:
        home_user = 'user'
    return home_user


def get_host():
    host = environ.get('HOSTNAME')
    if host is not None:
        return host
    return gethostname()


def sorted_nicely(l, reverse=False):
    def tryint(s):
        try:
            return int(s)
        except:
            return s

    def alphanum_key(s):
        if type(s) is not str:
            raise ValueError('{} must be a string in l: {}'.format(s, l))
        return [tryint(c) for c in re.split('([0-9]+)', s)]

    rtn = sorted(l, key=alphanum_key)
    if reverse:
        rtn = reversed(rtn)
    return rtn
