from xivdm.gen.generators import *

class Manager:
    def __init__(self, dat_manager):
        self._dat_manager = dat_manager
        self._generators = {
            'icons': icons(self._dat_manager),
            'maps': maps(self._dat_manager),
            'models': models(self._dat_manager)
        }

    def get_generators(self):
        return self._generators.keys()

    def get_generator(self, name):
        return self._generators[name]()