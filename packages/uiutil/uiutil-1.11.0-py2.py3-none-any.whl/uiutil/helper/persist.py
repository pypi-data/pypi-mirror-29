# encoding: utf-8

import logging_helper
import os
import json
import codecs
from stateutil.persist import Persist

from conversionutil.dx import dx
from conversionutil.ex import ex

logging = logging_helper.setup_logging()

global_ui_persistence_store = None


class UIPersistentStore(object):
    def __init__(self,
                 persistent_store):
        """

        :param persistent_store: class that implements __getitem__ and __setitem__.
        """
        self.persistent_store = persistent_store

    @staticmethod
    def key(key):
        """
        Override if the key must be modified to access the store
        :param key: key into the store
        :return: modifier key
        """
        return key


class JSONPersistentStore(object):
    def __init__(self,
                 root_folder):
        self.root_folder = root_folder
        logging_helper.ensure_path_exists(root_folder)

    def filename(self,
                 key):
        parts = key.split(u'/')[:-1]

        if len(parts) > 1:
            logging_helper.ensure_path_exists(os.path.join(self.root_folder, *parts[:-1]))

        if len(parts) == 0:
            return u'{p}.json'.format(p=self.root_folder)
        else:
            return u'{p}.json'.format(p=os.path.join(self.root_folder, *parts))

    @staticmethod
    def read_data(filepath):
        with codecs.open(filepath, 'r', 'utf-8') as data_file:
            return json.load(data_file)

    @staticmethod
    def write_data(filepath,
                   data):
        with codecs.open(filepath, 'w', "utf-8") as data_file:
            json.dump(data,
                      data_file,
                      indent=4)

    @staticmethod
    def _key(key):
        return key.split(u'/')[-1]

    def __setitem__(self,
                    key,
                    value):
        filename = self.filename(key)
        try:
            data = self.read_data(filename)
        except IOError:
            data = {}
        data[self._key(key)] = value
        self.write_data(filename, data)

    def __getitem__(self,
                    key):
        try:
            return self.read_data(self.filename(key))[self._key(key)]
        except IOError:
            raise KeyError(key)


def json_persistent_store_factory(root_folder):
    return UIPersistentStore(
               JSONPersistentStore(
                   root_folder=root_folder))


def set_global_ui_persistence_store(store):
    global global_ui_persistence_store
    global_ui_persistence_store = store


def get_global_ui_persistence_store():
    global global_ui_persistence_store
    if not global_ui_persistence_store:
        raise ValueError(u'set_global_ui_persistence_store has not been called.')
    return global_ui_persistence_store


class PersistentField(Persist):

    def __init__(self,
                 key,
                 store=None,
                 *args,
                 **kwargs):
        if store is None:
            store = get_global_ui_persistence_store()
            key = store.key(key)
        super(PersistentField, self).__init__(persistent_store=store.persistent_store,
                                              key=key,
                                              *args,
                                              **kwargs)


class ObscuredPersistentField(PersistentField):
    """
    Used instead of PersistentField if you want
    the value stored with some noddy encoding
    """
    @staticmethod
    def encode(value):
        return ex(value)

    @staticmethod
    def decode(value):
        return dx(value)
