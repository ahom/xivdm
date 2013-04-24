from xivdm.view.mapping import *

class Manager:
    def __init__(self, exd_manager):
        self._exd_manager = exd_manager
        self._mappings = {
            'actions': simple_mapping('Action', actions),
            'action_categories': simple_mapping('ActionCategory', action_categories),
            'attack_types': simple_mapping('AttackType', attack_types),
            'class_jobs': simple_mapping('ClassJob', class_jobs),
            'class_jobs_categories': simple_mapping('ClassJobCategory', class_job_categories)            
        }

        self._jsons = {}

    def get_mappings(self):
        return self._mappings.keys()

    def get_json(self, name):
        if not name in self._jsons:
            self._create_json(name)
        return self._jsons[name]
    
    def _create_json(self, name):
        raw_json = self._mappings[name](self._exd_manager)

        # Parse strings

        # Parse refs

        self._jsons[name] = raw_json
        