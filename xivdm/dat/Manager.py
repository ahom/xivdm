import zlib
from os import path, makedirs
import logging
import pickle
import gzip

from xivdm.dat.Category import Category

class Manager:
    CACHE_PATH = 'cache/%s.gz'
    CATEGORIES = {
        'common': 0x00,
        'bgcommon': 0x01,
        'bg': 0x02,
        'cut': 0x03,
        'chara': 0x04,
        'shader': 0x05,
        'ui': 0x06,
        'sound': 0x07,
        'vfx': 0x08,
        'ui_script': 0x09,
        'exd': 0x0A,
        'game_script': 0x0B,
        'music': 0x0C
    }

    def __init__(self, game_path):        
        self._categories = {
            category_name: Category(
                category_name,
                path.join(game_path, 'game/sqpack/ffxiv'),
                '%0.6x.win32' % (index << 0x10)
            ) for category_name, index in Manager.CATEGORIES.items()
        }

        self._name_caches = {}

    def get_categories(self):
        return self._categories.keys()

    def get_category(self, name):
        return self._categories[name]

    def get_file(self, name):
        logging.info('%s', name)
        dir_hash, file_hash = get_hashes(name)
        category = self.get_category_from_filename(name)
        file_data = category.get_file(dir_hash, file_hash)
        # here we know extraction is successful so register the name
        self._register_name(category.get_name(), name, dir_hash, file_hash)
        return self.get_category_from_filename(name).get_file(dir_hash, file_hash)

    def check_dir_existence(self, name):
        (dir_hash, _) = get_hashes(name)
        return self.get_category_from_filename(name).check_dir_existence(dir_hash)

    def check_file_existence(self, name):
        (dir_hash, file_hash) = get_hashes(name)
        return self.get_category_from_filename(name).check_file_existence(dir_hash, file_hash)

    def get_category_from_filename(self, name):
        return self.get_category(name.split('/', 1)[0].lower())

    def get_dir_name(self, category_name, dir_hash):
        cache = self._get_cache(category_name)
        if dir_hash in cache:
            return cache[dir_hash]['name']
        return '%0.8X' % dir_hash

    def get_file_name(self, category_name, dir_hash, file_hash):
        cache = self._get_cache(category_name)
        if dir_hash in cache:
            dir_cache = cache[dir_hash]['hashes']
            if file_hash in dir_cache:
                return dir_cache[file_hash]
        return '%0.8X' % file_hash

    def _register_name(self, category_name, name, dir_hash, file_hash):
        cache = self._get_cache(category_name)
        if not dir_hash in cache:
            cache[dir_hash] = {
                'name': name.rsplit('/', 1)[0],
                'hashes': {}
            }

        dir_cache = cache[dir_hash]['hashes']
        if not file_hash in dir_cache:
            dir_cache[file_hash] = name.rsplit('/', 1)[1]

    def _get_cache(self, category_name):
        if not category_name in self._name_caches:
            cache_path = self.CACHE_PATH % category_name

            if not path.exists(path.dirname(cache_path)):
                makedirs(path.dirname(cache_path))

            if path.exists(cache_path):
                with gzip.open(cache_path, 'rb') as file_handle:
                    self._name_caches[category_name] = pickle.load(file_handle)
            else:
                self._name_caches[category_name] = {}
        return self._name_caches[category_name]

    def __del__(self):
        # Saving the caches at destruction time
        for category_name in self._name_caches:
            cache_path = self.CACHE_PATH % category_name

            with gzip.open(cache_path, 'wb') as file_handle:
                pickle.dump(self._name_caches[category_name], file_handle)


def get_hashes(name):
    dir_part, file_part = name.lower().rsplit('/', 1)
    return get_hash(dir_part), get_hash(file_part)

def get_hash(string):
    return zlib.crc32(bytes(string, 'ascii')) ^ 0xFFFFFFFF

    