import logging

from xivdm.language import get_language_name, is_language_valid
from xivdm.exd.exh import extract_header
from xivdm.exd.exd import extract_data

class Category:
    EXH_NAME = 'exd/%s.exh'
    EXD_NAME = 'exd/%s_%d%s.exd'

    def __init__(self, dat_manager, category_name):
        self._dat_manager = dat_manager
        self._name = category_name
        self._header = None
        self._data = None

    def get_name(self):
        return self._name

    def get_header(self):
        if not self._header:
            self._extract_header()
        return self._header

    def get_data(self):
        if not self._data:
            self._extract_data()
        return self._data

    def get_ln_data(self, language):
        return self.get_data()[language]

    def get_ln_id_data(self, language, id):
        return self.get_ln_data(language)[id]

    def get_ln_id_mem_data(self, language, id, member):
        return self.get_ln_id_data(language, id)[member]

    def get_csv(self):
        header = self.get_header()
        data = self.get_data()
        return_dict = dict()
        for language in header.languages:
            if is_language_valid(language):
                return_dict[language] = [
                    '%d, %s' % (id, ', '.join([repr(value) for value in values])) for id, values in data[language].items()
                ]
        return return_dict

    def _extract_header(self):
        self._header = extract_header(self._dat_manager.get_file(Category.EXH_NAME % (self._name)))

    def _extract_data(self):
        header = self.get_header()
        self._data = {}
        for language in header.languages:
            if is_language_valid(language):
                language_name = get_language_name(language)
                if language_name != '':
                    language_name = '_%s' % language_name
                self._data[language] = {}
                for exd_file in header.exds:
                    language_name = get_language_name(language)
                    if language_name != '':
                        language_name = '_%s' % language_name
                    self._data[language].update(extract_data(
                            self._dat_manager.get_file(Category.EXD_NAME % (self._name, exd_file, language_name)),
                            header))
