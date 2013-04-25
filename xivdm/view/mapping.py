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

def food_stat(stat_type, percent_value, max_value):
    return {
        'stat': ref('parameters', stat_type),
        'percent_value': percent_value,
        'max_value': max_value
    }

def stat(stat_type, stat_value):
    return {
        'stat': ref('parameters', stat_type),
        'value': stat_value
    }

#### MAPPINGS ####
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

def addons(data, id, v):
    return {
        'name': string(data, id, 0)
    }

def attack_types(data, id, v):
    return {
        'name': string(data, id, 0)
    }

def bnpc_names(data, id, v):
    return {
        'name':                 string(data, id, 0),

        'plural_name':          string(data, id, 2),

        'unmapped_values':      unmapped(
            list(range(1, 2))
            + list(range(3, 8)), v)
    }


def class_job_categories(data, id, v):
    return {
        'name':                     string(data, id, 0),
        'class_job_restrictions':   [v[index] for index in range(1, 30)]
    }

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

def companions(data, id, v):
    return {
        'name':                 string(data, id, 0),

        'plural_name':          string(data, id, 2),

        'unmapped_values':      unmapped(
            list(range(1, 2))
            + list(range(3, 13)), v)
    }

def completions(data, id, v):
    return {
        'name':                 string(data, id, 2),

        'unmapped_values':      unmapped(
            list(range(0, 2))
            + list(range(3, 4)), v)
    }

def emotes(data, id, v):
    return {
        'name':                 string(data, id, 13),
        'icon':                 icon(14),

        'unmapped_values':      unmapped(
            list(range(0, 13))
            + list(range(15, 17)), v)
    }

def enpc_bases(data, id, v):
    return {
        'name':                 string(data, id, 0),

        'name_bis':             string(data, id, 2),

        'title':                string(data, id, 8),
        
        'unmapped_values':          unmapped(
            list(range(1, 2))
            + list(range(3, 8))
            + list(range(9, 102)), v)
    }

def eobjs(data, id, v):
    return {
        'name':                 string(data, id, 0),

        'description':          string(data, id, 2),

        'unmapped_values':          unmapped(
            list(range(1, 2))
            + list(range(3, 16)), v)
    }

def fates(data, id, v):
    return {
        'level':                v[0],

        'name':                 string(data, id, 8),
        'description':          string(data, id, 9),
        'special_text_1':       string(data, id, 10),
        'special_text_2':       string(data, id, 11),
        'special_text_3':       string(data, id, 12),
        'special_text_4':       string(data, id, 13),

        'unmapped_values':          unmapped(
            list(range(1, 8))
            + list(range(15, 19)), v)
    }

def gcrank_gridania_female_texts(data, id, v):
    return {
        'name':                 string(data, id, 0),

        'plural':               string(data, id, 2),

        'unmapped_values':          unmapped(
            list(range(1, 2))
            + list(range(3, 10)), v)
    }

def gcrank_gridania_male_texts(data, id, v):
    return {
        'name':                 string(data, id, 0),

        'plural':               string(data, id, 2),

        'unmapped_values':          unmapped(
            list(range(1, 2))
            + list(range(3, 10)), v)
    }

def gcrank_limsa_female_texts(data, id, v):
    return {
        'name':                 string(data, id, 0),

        'plural':               string(data, id, 2),

        'unmapped_values':          unmapped(
            list(range(1, 2))
            + list(range(3, 10)), v)
    }

def gcrank_limsa_male_texts(data, id, v):
    return {
        'name':                 string(data, id, 0),

        'plural':               string(data, id, 2),

        'unmapped_values':          unmapped(
            list(range(1, 2))
            + list(range(3, 10)), v)
    }

def gcrank_uldah_female_texts(data, id, v):
    return {
        'name':                 string(data, id, 0),

        'plural':               string(data, id, 2),

        'unmapped_values':          unmapped(
            list(range(1, 2))
            + list(range(3, 10)), v)
    }

def gcrank_uldah_male_texts(data, id, v):
    return {
        'name':                 string(data, id, 0),

        'plural':               string(data, id, 2),

        'unmapped_values':          unmapped(
            list(range(1, 2))
            + list(range(3, 10)), v)
    }

def general_actions(data, id, v):
    return {
        'name':                 string(data, id, 0),
        'description':          string(data, id, 1),

        'unmapped_values':      unmapped(
            list(range(2, 3)), v)
    }

def grand_companies(data, id, v):
    return {
        'name':                 string(data, id, 0),

        'unmapped_values':      unmapped(
            list(range(1, 2)), v)
    }

def guardian_deities(data, id, v):
    return {
        'name':                 string(data, id, 0),
        'description':          string(data, id, 1),
        'icon':                 string(data, id, 2),
    }

def item_categories(data, id, v):
    return {
        'name': string(data, id, 0)
    }

def item_foods(data, id, v):
    return {
        'stats': [                  food_stat(v[0], v[2], v[3]),
                                    food_stat(v[6], v[8], v[9]),
                                    food_stat(v[12], v[14], v[15])],

        'unmapped_values':          unmapped(
            list(range(1, 2))
            + list(range(4, 6))
            + list(range(7, 8))
            + list(range(10, 12))
            + list(range(13, 14)), v)
    }

def item_search_categories(data, id, v):
    return {
        'name': string(data, id, 0),
        'icon': icon(1),

        'unmapped_values':  unmapped(
            list(range(2, 5)), v)
    }

def item_search_class_filters(data, id, v):
    return {
        'name': string(data, id, 0),

        'unmapped_values':  unmapped(
            list(range(1, 2)), v)
    }

def item_ui_categories(data, id, v):
    return {
        'name': string(data, id, 0),
        'icon': icon(1)
    }

def items(data, id, v):
    return {
        'noon':                     string(data, id, 0),

        'plural_noon':              string(data, id, 2),

        'description':              string(data, id, 8),
        'name':                     string(data, id, 9),
        'icon':                     icon(10),
        'item_level':               v[11],
        'class_job_level':          v[12],

        'number_per_stack':         v[14],
        'item_category':            ref('item_categories',              v[15]),
        'item_ui_category':         ref('item_ui_categories',           v[16]),
        'item_search_category':     ref('item_search_categories',       v[17]),
        'rarity':                   v[18],

        'stats': [                  stat(v[31], v[32]),
                                    stat(v[33], v[34]),
                                    stat(v[35], v[36]),
                                    stat(v[37], v[38]),
                                    stat(v[39], v[40]),
                                    stat(v[41], v[42])],

        'repair_class_job':         ref('class_jobs',                   v[56]),
        'repair_material':          ref('items',                        v[57]),
        'item_search_class_filter': ref('item_search_class_filters',    v[58]),
    
        'base_stats': [             stat(12, v[60]),  # physical_damage
                                    stat(13, v[61]),  # magic_damage
                                    stat(14, v[62]),  # delay

                                    stat(18, v[64]),  # block
                                    stat(17, v[65]),  # block_rate
                                    stat(21, v[66]),  # defense
                                    stat(24, v[67])], # magic_defense

        'item_food':                ref('item_foods',                   v[71]),
        'effet_duration':           v[72],

        'is_unique':                v[74],
        'is_untradable':            v[75],

        'race_restrictions': [      v[82],
                                    v[83],
                                    v[84],
                                    v[85],
                                    v[86]],
        'gender_restrictions': [    v[87],
                                    v[88]],
        'class_job_category':       ref('class_job_categories',         v[89]),

        'grand_company':            ref('grand_companies',              v[91]),

        'unmapped_values':          unmapped(
            list(range(1, 2))
            + list(range(3, 8))
            + list(range(13, 14))
            + list(range(19, 31))
            + list(range(43, 56))
            + list(range(59, 60))
            + list(range(63, 64))
            + list(range(68, 71))
            + list(range(73, 74))
            + list(range(76, 82))
            + list(range(90, 91))
            + list(range(92, 93)), v)
    }

def maps(data, id, v):
    return {
        'name':                 string(data, id, 3),

        'zone':                 ref('place_names', v[6]),
        'region':               ref('place_names', v[7]),

        'unmapped_values':      unmapped(
            list(range(0, 3))
            + list(range(4, 6))
            + list(range(8, 10)), v)
    }

def parameters(data, id, v):
    return {
        'name': string(data, id, 1),

        'unmapped_values':      unmapped(
            list(range(0, 1)), v)
    }

def place_names(data, id, v):
    return {
        'name':                 string(data, id, 0),

        'unmapped_values':      unmapped(
            list(range(1, 10)), v)
    }

def statuses(data, id, v):
    return {
        'name':         string(data, id, 0),
        'description':  string(data, id, 1),
        'icon':         icon(2),

        'unmapped_values':      unmapped(
            list(range(3, 15)), v)
    }

def traits(data, id, v):
    return {
        'name':         string(data, id, 0),
        'description':  string(data, id, 1),
        'icon':         icon(2),
        'class_job':    ref('class_jobs', v[3]),
        'level':        v[4],

        'unmapped_values':      unmapped(
            list(range(5, 7)), v)
    }

