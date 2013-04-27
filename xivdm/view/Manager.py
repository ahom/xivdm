from xivdm.language import get_language_id
from xivdm.view.mapping import *
from xivdm.view.strings import StringConverter

class Manager:
    def __init__(self, exd_manager):
        self._exd_manager = exd_manager
        self._mappings = {
            'action_categories': simple_mapping('ActionCategory', action_categories),
            'actions': simple_mapping('Action', actions),
            'addons': simple_mapping('Addon', addons),
            'attack_types': simple_mapping('AttackType', attack_types),
            'bnpc_names': simple_mapping('BNpcName', bnpc_names),
            'class_jobs': simple_mapping('ClassJob', class_jobs),
            'class_job_categories': simple_mapping('ClassJobCategory', class_job_categories),
            'companions': simple_mapping('Companion', companions),
            'completions': simple_mapping('Completion', completions),
            'emotes': simple_mapping('Emote', emotes),
            'enpc_bases': simple_mapping('ENpcBase', enpc_bases),
            'eobjs': simple_mapping('EObj', eobjs),
            'fates': simple_mapping('Fate', fates),
            'gcrank_gridania_female_texts': simple_mapping('GCRankGridaniaFemaleText', gcrank), 
            'gcrank_gridania_male_texts': simple_mapping('GCRankGridaniaMaleText', gcrank), 
            'gcrank_limsa_female_texts': simple_mapping('GCRankLimsaFemaleText', gcrank), 
            'gcrank_limsa_male_texts': simple_mapping('GCRankLimsaMaleText', gcrank), 
            'gcrank_uldah_female_texts': simple_mapping('GCRankUldahFemaleText', gcrank), 
            'gcrank_uldah_male_texts': simple_mapping('GCRankUldahMaleText', gcrank), 
            'general_actions': simple_mapping('GeneralAction', general_actions), 
            'grand_companies': simple_mapping('GrandCompany', grand_companies), 
            'guardian_deities': simple_mapping('GuardianDeity', guardian_deities), 
            'item_categories': simple_mapping('ItemCategory', item_categories), 
            'item_foods': simple_mapping('ItemFood', item_foods), 
            'item_search_categories': simple_mapping('ItemSearchCategory', item_search_categories), 
            'item_search_class_filters': simple_mapping('ItemSearchClassFilter', item_search_class_filters), 
            'item_ui_categories': simple_mapping('ItemUICategory', item_ui_categories), 
            'items': simple_mapping('Item', items), 
            'maps': simple_mapping('Map', maps), 
            'parameters': simple_mapping('Parameter', parameters), 
            'place_names': simple_mapping('PlaceName', place_names), 
            'statuses': simple_mapping('Status', statuses), 
            'traits': simple_mapping('Trait', traits)
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
            return StringConverter(self._exd_manager, get_language_id(key)).convert(memoryview(value))
        return None

    def _parse_view_refs(self, key, value):
        if type(value) == dict:
            if 'type' in value:
                dict_type = value['type']
                if dict_type in ['view_ref', 'full_view_ref']:
                    is_full = dict_type == 'full_view_ref'
                    view_ref = value.get('view')
                    id = value.get('id')
                    if view_ref and id is not None and id != -1:
                        id_json = self.get_json(view_ref)[id]
                        if not is_full:
                            if 'name' in id_json:
                                value['value'] = id_json['name']['en']
                                return value
                        else:
                            value['value'] = id_json
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
        