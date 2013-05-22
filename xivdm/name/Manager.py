from os import path, makedirs
import logging
import pickle
import gzip

from xivdm.dat.Manager import get_hash

class HashMap:
    def __init__(self, name):
        self._hash_map = {}
        self._name = name

    def get_name(self):
        return self._name

    def get_entry(self, entry_hash):
        if entry_hash in self._hash_map:
            return self._hash_map[entry_hash]
        else:
            return None

    def add_entry(self, entry, obj=None):
        if not obj:
            obj = entry
        entry_hash = get_hash(entry)

        if entry_hash in self._hash_map:
            logging.error('CRC32 collision: %s - %s', entry, self._hash_map[entry_hash])
        else:
            self._hash_map[entry_hash] = obj

def gen_hash_table(dat_manager, name, gen):
    cache_path = 'cache/%s.gz' % name

    if path.exists(cache_path):
        with gzip.open(cache_path, 'rb') as file_handle:
            return pickle.load(file_handle)

    logging.warn('Generating names for %s, this may take a while...' % name)

    if not path.exists(path.dirname(cache_path)):
        makedirs(path.dirname(cache_path))

    cat_hash_map = HashMap(name)
    for dir_path, file_gen in gen(dat_manager):
        if dat_manager.check_dir_existence('%s/' % dir_path):
            dir_hash_map = HashMap(dir_path)
            for file_path in file_gen():
                if dat_manager.check_file_existence('%s/%s' % (dir_path, file_path)):
                    dir_hash_map.add_entry(file_path)
            cat_hash_map.add_entry(dir_path, dir_hash_map)

    with gzip.open(cache_path, 'wb') as file_handle:
        pickle.dump(cat_hash_map, file_handle)

    return cat_hash_map

class Manager:
    def __init__(self, dat_manager):
        self._dat_manager = dat_manager
        self._categories = {
            'ui': ui,
            'chara': chara
        }
        self._hash_maps = {}

    def get_categories(self):
        return self._categories.keys()

    def get_hash_table(self, name):
        if not name in self._hash_maps:
            self._hash_maps[name] = gen_hash_table(self._dat_manager, name, self._categories[name])
        return self._hash_maps[name]

    def get_dir_name(self, name, dir_hash):
        dir_hash_map = self.get_hash_table(name).get_entry(dir_hash)
        if dir_hash_map:
            return dir_hash_map.get_name()
        return '%0.8X' % dir_hash

    def get_file_name(self, name, dir_hash, file_hash):
        dir_hash_map = self.get_hash_table(name).get_entry(dir_hash)
        if dir_hash_map:
            file_entry = dir_hash_map.get_entry(file_hash)
            if file_entry:
                return file_entry
        return '%0.8X' % file_hash

def get_mod_range():
    for x in range(10):
        for y in range(100):
            yield x + y * 1000

def ui(dat_manager):
    base_folder_path = 'ui/'

    # skins
    def files():
        yield ''
    yield '%sskin' % base_folder_path, files

    # icons
    for i in range(1000):
        folder = i * 1000
        folder_path = '%sicon/%0.6d' % (base_folder_path, folder)
        def files():
            for j in range(1000):
                yield '%0.6d.dds' % (folder + j)
        yield folder_path, files

        if dat_manager.check_dir_existence('%s/en/' % (folder_path)):
            for ln in ['en', 'ja', 'fr', 'de']:
                ln_folder_path = '%s/%s' % (folder_path, ln)
                def files():
                    for j in range(1000):
                        yield '%0.6d.dds' % (folder + j)
                yield ln_folder_path, files

    # maps
    for a in map(chr, range(ord('a'), ord('z') + 1)):
        for i in range(10):
            for b in map(chr, range(ord('a'), ord('z') + 1)):
                for j in range(10):
                    basename = '%s%d%s%d' % (a, i, b, j)
                    map_folder_path = '%smap/%s' % (base_folder_path, basename)

                    for k in range(100):
                        num = '%0.2d' % k
                        data_folder_path = '%s/%s' % (map_folder_path, num)

                        if not dat_manager.check_dir_existence('%s/' % data_folder_path):
                            break
                        else:
                            def files():
                                yield '%s%sm.dds' % (basename, num)
                                for x in range(16):
                                    for y in range(16):
                                        yield '%s%s_%d_%d.dds' % (basename, num, x, y)
                            yield data_folder_path, files
                        

def chara(dat_manager):
    base_folder_path = 'chara/'

    # weapons/monsters
    for resource_type in ['weapon', 'monster']:
        for r in range(10000):
            resource_name = '%s%0.4d' % (resource_type[0], r)
            resource_folder_path = '%s%s/%s/' % (base_folder_path, resource_type, resource_name)
            for b in range(1, 10000):
                base_name = 'b%0.4d' % b
                if not dat_manager.check_dir_existence('%sobj/body/%s/model/' % (resource_folder_path, base_name)):
                    break
                else:
                    # model
                    def files():
                        yield '%s%s.mdl' % (resource_name, base_name)
                    yield '%sobj/body/%s/model' % (resource_folder_path, base_name), files

    # accessories/equipments
    for resource_type in ['accessory', 'equipment']:
        for r in range(10000):
            resource_name = '%s%0.4d' % (resource_type[0], r)
            resource_folder_path = '%s%s/%s/' % (base_folder_path, resource_type, resource_name)

            def files():
                for c in get_mod_range():
                    base_name = 'c%0.4d' % c
                    for suffix in ['ril', 'rir', 'wrs', 'nek', 'ear', 'sho', 'dwn', 'glv', 'top', 'met']:
                        yield '%s%s_%s.mdl' % (base_name, resource_name, suffix)
            yield '%smodel' % (resource_folder_path), files

    # human
    for c in range(10000):
        resource_folder_path = '%shuman/%0.4d/' % (base_folder_path, resource_type, resource_name)

        if not dat_manager.check_dir_existence('%sobj/body/b0001/model/' % (resource_folder_path)):
            continue
        else:
            for b in range(1, 10000):
                base_name = 'b%0.4d' % b
                if not dat_manager.check_dir_existence('%sobj/body/b0001/model/' % (resource_folder_path)):
                    break
            for part, suffix in [('face', 'fac'), ('hair', 'hir'), ('tail', 'til'), ('body', 'top')]:


        def files():
            for x in range(10):
                for y in range(100):
                    base_name = 'c%0.2d0%0.1d' % (y, x)
                    for suffix in ['ril', 'rir', 'wrs', 'nek', 'ear', 'sho', 'dwn', 'glv', 'top', 'met']:
                        yield '%s%s_%s.mdl' % (base_name, resource_name, suffix)
        yield '%smodel' % (resource_folder_path), files

                base_folder_path = 'chara/human/c%0.4d/obj/' % i
            for j in range(10000):
                for s in [('face', 'fac'), ('hair', 'hir'), ('tail', 'til'), ('body', 'top')]:
                    folder_path = '%s%s/%s%0.4d/model/' % (base_folder_path, s[0], s[0][0], j)
                    def files():
                        yield '%sc%0.4d%s%0.4d_%s.mdl' % (folder_path, i, s[0][0], j, s[1])
                    yield folder_path, files
