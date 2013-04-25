from xivdm.view.mapping import *
from xivdm.view.strings import StringConverter

class Manager:
    def __init__(self, exd_manager):
        self._exd_manager = exd_manager
        self._mappings = {
            'actions': simple_mapping('Action', actions),
            'action_categories': simple_mapping('ActionCategory', action_categories),
            'attack_types': simple_mapping('AttackType', attack_types),
            'class_jobs': simple_mapping('ClassJob', class_jobs),
            'class_job_categories': simple_mapping('ClassJobCategory', class_job_categories)            
        }
        self._jsons = {}

    def get_mappings(self):
        return self._mappings.keys()

    def get_json(self, name):
        if not name in self._jsons:
            self._create_json(name)
        return self._jsons[name]
    
    def _create_json(self, name):
        self._jsons[name] = self._mappings[name](self._exd_manager)
        self._walk_json(self._jsons[name], self._parse_string)
        self._walk_json(self._jsons[name], self._parse_view_refs)

    def _parse_string(self, key, value):
        if type(value) == bytes:
            return StringConverter(self._exd_manager, key).convert(memoryview(value))
        return None

    def _parse_view_refs(self, key, value):
        if type(value) == dict and value.get('type') == 'view_ref':
            view_ref = value.get('view')
            id = value.get('value')
            if view_ref and id is not None and id != -1:
                id_json = self.get_json(view_ref)[id]
                if 'name' in id_json:
                    value['name'] = id_json['name'][2] # english == 2
                    return value
        return None

    def _walk_json(self, node, process_function):
        keys, values = self._get_keys_values(node)
        if keys and values:
            for index, value in enumerate(values):
                new_value = process_function(keys[index], value)
                if new_value is not None:
                    node[keys[index]] = new_value
                else:
                    self._walk_json(value, process_function)


    def _get_keys_values(self, node):
        if type(node) == dict:
            return list(node.keys()), list(node.values())
        elif type(node) == list:
            return list(range(len(node))), node
        else:
            return None, None
        