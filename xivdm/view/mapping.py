def simple_mapping(exd_name, mapping_function):
    def generated_function(exd_manager):
        data = exd_manager.get_category(exd_name).get_data()
        data_ln = data[list(data.keys())[0]]
        return {
            id: mapping_function(data, id, v) for id, v in data_ln.items()
        }
    return generated_function

def string(data, id, member_id):
    return {
        language: data[language][id][member_id] for language in data.keys()
    }

def ref(view_name, value):
    return {
        'type': 'view_ref',
        'view': view_name,
        'value': value
    }

def icon(value):
    return {
        'type': 'icon',
        'value': value
    }

def unmapped(index_list, v):
    return {
        index: repr(v[index]) for index in index_list
    }

#### MAPPINGS ####

def class_jobs(data, id, v):
    return {
        'name':             string(data, id, 0),
        'acronym':          string(data, id, 1),

        'base_class':       ref('class_jobs', v[19]),
        'is_job':           v[20],
        'caps_name':        string(data, id, 21),

        'caps_full_name':   string(data, id, 25),

        'unmapped_values':  unmapped(
            list(range(2, 19))
            + list(range(22, 25))
            + list(range(26, 28)), v)
    }

def class_job_categories(data, id, v):
    return {
        'name':                     string(data, id, 0),
        'class_job_restrictions':   [v[index] for index in range(1, 30)]
    }

def attack_types(data, id, v):
    return {
        'name': string(data, id, 0)
    }

def action_categories(data, id, v):
    return {
        'name': string(data, id, 0)
    }

def actions(data, id, v):
    return {
        'name':                 string(data, id, 0),
        'description':          string(data, id, 1),
        'icon':                 icon(v[2]),
        'category':             ref('action_categories', v[3]),

        'class_job':            ref('class_jobs', v[9]),
        'level':                v[10],
        'range':                v[11],

        'radius':               v[23],

        'resource_type':        v[32],
        'resource_value':       v[33],

        'cast':                 v[44],

        'recast':               v[46],

        'attack_type':          ref('attack_types', v[49]),

        'class_job_category':   ref('class_job_categories', v[58]),

        'unmapped_values':      unmapped(
            list(range(4, 9))
            + list(range(12, 23))
            + list(range(24, 32))
            + list(range(34, 44))
            + list(range(45, 46))
            + list(range(47, 49))
            + list(range(50, 58)), v)
    }