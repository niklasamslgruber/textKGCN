import glob
from os.path import join, getctime
import torch
from helper import io_utils as io
from config import FLAGS
from model.model_factory import create_model
from helper.utils import create_dir_if_not_exists, sorted_nicely


class Saver(object):
    def __init__(self):
        self.logdir = io.get_logs_path()
        create_dir_if_not_exists(self.logdir)
        self.model_info_f = self._open('model_info.txt')
        self._log_model_info()

        print('Logging to {}'.format(self.logdir))

    def _log_model_info(self):
        s = get_model_info_as_str()
        c = get_model_info_as_command()
        self.model_info_f.write(s)
        self.model_info_f.write('\n\n')
        self.model_info_f.write(c)
        self.model_info_f.write('\n\n')

    def save_trained_model(self, trained_model, epoch=None):
        epoch = "_epoch_{}".format(epoch) if epoch is not None else ""
        p = join(self.logdir, 'trained_model{}.pt'.format(epoch))
        torch.save(trained_model.state_dict(), p)
        # print('Trained model saved to {}'.format(p))

    def load_trained_model(self, train_data):
        p = join(self.logdir, 'trained_model*')
        files = glob.glob(p)
        best_trained_model_path = max(files, key=getctime)
        trained_model = create_model(train_data)
        trained_model.load_state_dict(
            torch.load(best_trained_model_path, map_location=FLAGS.device))
        trained_model.to(FLAGS.device)
        return trained_model

    def _open(self, f):
        return open(join(self.logdir, f), 'w')


def get_model_info_as_str():
    rtn = []
    d = vars(FLAGS)
    for k in sorted_nicely(d.keys()):
        v = d[k]
        s = '{0:26} : {1}'.format(k, v)
        rtn.append(s)
    rtn.append('{0:26} : {1}'.format('ts', io.get_ts()))
    return '\n'.join(rtn)


def get_model_info_as_command():
    rtn = []
    d = vars(FLAGS)
    for k in sorted_nicely(d.keys()):
        v = d[k]
        s = '--{}={}'.format(k, v)
        rtn.append(s)
    return 'python {} {}'.format(join(io.get_root_path(), 'main.py'), '  '.join(rtn))
