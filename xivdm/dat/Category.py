from os import path

from xivdm.dat.index import extract_hash_table 
from xivdm.dat.dat import extract_file

class Category:
    INDEX_NAME = '%s.index'
    DAT_NAME = '%s.dat%d'

    def __init__(self, sqpack_path, sqpack_base_name):
        self._path = sqpack_path
        self._base_name = sqpack_base_name
        self._base_path = path.join(self._path, self._base_name)

        with open(self._get_index_path(), 'rb') as index_file_handle:
            self._hash_table = extract_hash_table(index_file_handle)

        self._dat_file_handles = {}

    def get_name(self):
        return self._base_name

    def check_dir_existence(self, dir_hash):
        return dir_hash in self._hash_table

    def check_file_existence(self, dir_hash, file_hash):
        return self.check_dir_existence(dir_hash) and file_hash in self.get_dir_hash_table(dir_hash)

    def get_file(self, dir_hash, file_hash):
        file_infos = self.get_dir_hash_table(dir_hash)[file_hash]
        dat_file_handle = self._get_dat_file_handle(file_infos.dat_nb)
        dat_file_handle.seek(file_infos.dat_offset)
        return extract_file(dat_file_handle)

    def get_hash_table(self):
        return self._hash_table

    def get_dir_hash_table(self, dir_hash):
        return self._hash_table[dir_hash]


    def _get_index_path(self):
        return Category.INDEX_NAME % (self._base_path)

    def _get_dat_path(self, dat_nb):
        return Category.DAT_NAME % (self._base_path, dat_nb)

    def _get_dat_file_handle(self, dat_nb):
        if not dat_nb in self._dat_file_handles:
            self._dat_file_handles[dat_nb] = open(self._get_dat_path(dat_nb), 'rb')
        return self._dat_file_handles[dat_nb]