class Patchable:
    def __init__(self, game_path, patchable_name, patch_archive_path):
        self._game_path = game_path
        self._name = patchable_name
        self._patch_archive_path = patch_archive_path

    def get_name(self):
        return self._name

    def get_version(self):
        pass

    def check(self):
        pass

    def download(self):
        pass

    def apply(self):
        pass

    def update(self):
        pass