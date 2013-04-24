class Mapping:
    def __init__(self, exd_manager, mapping_name):
        self._exd_manager = exd_manager
        self._name = mapping_name

    def get_name(self):
        return self._name

    def get_json(self):
        pass