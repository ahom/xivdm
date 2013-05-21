from os import path, makedirs
import pickle

from xivdm.dat.Manager import get_hash

class HashMap:
    def __init__(self, name):
        self._hash_map = {}
        self._name = name

    def get_name(self):
        return self._name

    def add_entry(self, entry, obj=None):
        if not obj:
            obj = entry
        entry_hash = get_hash(entry)

        if entry_hash in self._hash_map:
            logging.error('CRC32 collision: %s - %s', entry, self._hash_map[entry_hash])

        self._hash_map[entry_hash] = obj

    def __repr__(self):
        return '<name=%s - value=%s>' % (self._name, self._hash_map)

def gen_hash_table(dat_manager, name, gen):
    cache_path = 'cache/%s.dump' % name

    if path.exists(cache_path):
        with open(cache_path, 'rb') as file_handle:
            return pickle.load(file_handle)

    if not path.exists(path.dirname(cache_path)):
        makedirs(path.dirname(cache_path))

    cat_hash_map = HashMap(name)
    for dir_path, file_gen in gen():
        if dat_manager.check_dir_existence(dir_path):
            dir_hash_map = HashMap(dir_path)
            for file_path in file_gen():
                if dat_manager.check_file_existence('%s%s' % (dir_path, file_path)):
                    dir_hash_map.add_entry(file_path)
            cat_hash_map.add_entry(dir_path, dir_hash_map)

    with open(cache_path, 'wb') as file_handle:
        pickle.dump(cat_hash_map, file_handle)

    return cat_hash_map

class Manager:
    def __init__(self, dat_manager):
        self._dat_manager = dat_manager
        self._categories = {
            'ui': ui
        }

    def get_categories(self):
        return self._categories.keys()

    def get_category(self, name):
        return gen_hash_table(self._dat_manager, name, self._categories[name])

def ui():
    base_folder_path = 'ui/'

    # icons
    for i in range(1000):
        folder = i * 1000
        folder_path = '%sicon/%0.6d/' % (base_folder_path, folder)
        def files():
            for j in range(1000):
                yield '%0.6d.dds' % (folder + j)
        yield folder_path, files

    # maps
    for a in map(chr, range(ord('a'), ord('z') + 1)):
        for i in range(10):
            for b in map(chr, range(ord('a'), ord('z') + 1)):
                for j in range(10):
                    for k in range(100):
                        basename = '%s%d%s%d' % (a, i, b, j)
                        num = '%0.2d' % k
                        map_folder_path = '%smap/%s/%s/' % (base_folder_path, basename, num)
                        def files():
                            yield '%s%sm.dds' % (basename, num)
                            for x in range(16):
                                for y in range(16):
                                    yield '%s%s_%d_%d.dds' % (basename, num, x, y)
                        yield map_folder_path, files