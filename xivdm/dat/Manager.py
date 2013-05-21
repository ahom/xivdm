import zlib
from os import path
import logging

from xivdm.dat.Category import Category

class Manager:
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
                path.join(game_path, 'game/sqpack/ffxiv'),
                '%0.6x.win32' % (index << 0x10)
            ) for category_name, index in Manager.CATEGORIES.items()
        }

    def get_categories(self):
        return self._categories.keys()

    def get_category(self, name):
        return self._categories[name]

    def get_file(self, name):
        logging.info('%s', name)
        dir_hash, file_hash = get_hashes(name)
        return self.get_category_from_filename(name).get_file(dir_hash, file_hash)

    def check_dir_existence(self, name):
        (dir_hash, _) = get_hashes(name)
        return self.get_category_from_filename(name).check_dir_existence(dir_hash)

    def check_file_existence(self, name):
        (dir_hash, file_hash) = get_hashes(name)
        return self.get_category_from_filename(name).check_file_existence(dir_hash, file_hash)


    def get_category_from_filename(self, name):
        return self.get_category(name.split('/', 1)[0].lower())

def get_hashes(name):
    dir_part, file_part = name.lower().rsplit('/', 1)
    return get_hash(dir_part), get_hash(file_part)

def get_hash(string):
    return zlib.crc32(bytes(string, 'ascii')) ^ 0xFFFFFFFF

    