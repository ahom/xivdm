from xivdm.gen.generators import *

class Manager:
    def __init__(self):
        self._generators = {
            'icons': icons(),
            'maps': maps()
        }

    def get_generators(self):
        return self._generators.keys()

    def get_generator(self, name):
        return self._generators[name]()