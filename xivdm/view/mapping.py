from xivdm.language import get_language_name

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
        get_language_name(language): data[language][id][member_id] for language in data.keys()
    }

def ref(view_name, value):
    return {
        'type': 'view_ref',
        'view': view_name,
        'id': value
    }

def full_ref(view_name, value):
    return {
        'type': 'full_view_ref',
        'view': view_name,
        'id': value
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

def mat(item_id, quantity):
    return {
        'item': ref('items', item_id),
        'quantity': quantity
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
        'icon':                 v[2],
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

def balloons(data, id, v):
    return {
        'text': string(data, id, 1),

        'unmapped_values':  unmapped(
            [0], v)
    }

def behest_rewards(data, id, v):
    return {
        'items': [ref('items', v[i]) for i in range(1, 4)],

        'level': v[6],

        'unmapped_values':      unmapped(
            list(range(0, 1))
            + list(range(4, 6)), v) 
    }

def bnpc_names(data, id, v):
    return {
        'name':                 string(data, id, 0),

        'plural_name':          string(data, id, 2),

        'unmapped_values':      unmapped(
            list(range(1, 2))
            + list(range(3, 8)), v)
    }

def chain_bonuses(data, id, v):
    return {
        'exp_percent':  v[0],
        'timer':        v[1]
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

def complete_journals(data, id, v):
    return {
        'header_image':     v[3],

        'name':             string(data, id, 5),

        'unmapped_values':      unmapped(
            list(range(0, 3))
            + list(range(4, 5)), v)
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
        'icon':                 v[14],

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

def errors(data, id, v):
    return {
        'name':                 string(data, id, 0)
    }

def event_items(data, id, v):
    return {
        'name':                 string(data, id, 0),

        'name_plural':          string(data, id, 2),

        'description':          string(data, id, 8),
        'description_bis':      string(data, id, 9),

        'quest':                ref('quests', v[13]),

        'unmapped_values':          unmapped(
            list(range(1, 2))
            + list(range(3, 8))
            + list(range(10, 13))
            + list(range(14, 15)), v)
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

def gcrank(data, id, v):
    return {
        'name':                 string(data, id, 0),

        'plural':               string(data, id, 2),

        'unmapped_values':          unmapped(
            list(range(1, 2))
            + list(range(3, 10)), v)
    }

def gcshop_item_categories(data, id, v):
    return {
        'name':                 string(data, id, 0)
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

def grand_company_ranks(data, id, v):
    return {
        'rank':                 v[0],
        'max_seals':            v[1],

        'unmapped_values':      unmapped(
            list(range(2, 6)), v)
    }

def grand_company_seal_shop_items(data, id, v):
    return {
        'item':                 ref('items', v[0]),
        
        'seal_cost':            v[3],
        'category':             ref('gcshop_item_categories', v[4]),
        'name':                 string(data, id, 5),

        'unmapped_values':      unmapped(
            list(range(1, 3)), v)
    }

def guardian_deities(data, id, v):
    return {
        'name':                 string(data, id, 0),
        'description':          string(data, id, 1),
        'icon':                 v[2],
    }

def instance_contents(data, id, v):
    return {
        'name':                 string(data, id, 1),  

        'unmapped_values':          unmapped(
            list(range(0, 1))
            + list(range(2, 6)), v)
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
        'icon': v[1],

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
        'icon': v[1]
    }

def items(data, id, v):
    return {
        'noon':                     string(data, id, 0),

        'plural_noon':              string(data, id, 2),

        'description':              string(data, id, 8),
        'name':                     string(data, id, 9),
        'icon':                     v[10],
        'item_level':               v[11],
        'class_job_level':          v[12],

        'number_per_stack':         v[14],
        'item_category':            ref('item_categories',              v[15]),
        'item_ui_category':         ref('item_ui_categories',           v[16]),
        'item_search_category':     ref('item_search_categories',       v[17]),
        'rarity':                   v[18],

        'stats':                    [stat(v[i], v[i+1]) for i in range(31, 43, 2)],

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

        'item_food':                full_ref('item_foods',                   v[71]),
        'effet_duration':           v[72],

        'is_unique':                v[74],
        'is_untradable':            v[75],

        'buy_price':                v[78],

        'race_restrictions':        [v[i] for i in range(82, 87)],
        'gender_restrictions':      [v[i] for i in range(87, 89)],
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
            + list(range(76, 78))
            + list(range(79, 82))
            + list(range(90, 91))
            + list(range(92, 93)), v)
    }

def leves(data, id, v):
    return {
        'name':                 string(data, id, 0),
        'description':          string(data, id, 1),
        'client':               ref('leve_clients', v[2]),

        'unmapped_values':      unmapped(
            list(range(3, 28)), v)
    }

def leve_clients(data, id, v):
    return {
        'name':                 string(data, id, 0)
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

def markers(data, id, v):
    return {
        'icon':                 v[0],
        'name':                 string(data, id, 1)
    }

def monster_notes(data, id, v):
    return {
        'npcs':                 [ref('bnpc_names', v[i]) for i in range(0, 3)],

        'npc_quantities':       [v[i] for i in range(4, 7)],

        'exp':                  v[8],
        'name':                 string(data, id, 9),

        'icons':                [v[i] for i in range(14, 17)],
        
        'unmapped_values':      unmapped(
            list(range(3, 4))
            + list(range(7, 8))
            + list(range(10, 14))
            + list(range(17, 18)), v)
    }

def npc_yells(data, id, v):
    return {
        'name':                 string(data, id, 0),
        
        'unmapped_values':      unmapped(
            list(range(1, 5)), v)
    }


def online_statuses(data, id, v):
    return {
        'name':                 string(data, id, 0),
        'icon':                 v[1]
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

def quests(data, id , v):
    return {
        'name':                 string(data, id, 0),

        'unmapped_values':      unmapped(
            list(range(1, 778)), v)
    }

def roles(data, id , v):
    return {
        'name':                 string(data, id, 0),
        'abbr':                 string(data, id, 1),

        'unmapped_values':      unmapped(
            list(range(2, 3)), v)
    }

def shops(data, id , v):
    return {
        'icon':                 v[1],
        'items':                [ref('shop_items', v[i]) for i in range(2, 42)],

        'name':                 string(data, id, 42),
        'unmapped_values':      unmapped(
            list(range(0, 1)), v)
    }

def shop_items(data, id , v):
    return {
        'unmapped_values':      unmapped(
            list(range(0, 6)), v)
    }

def statuses(data, id, v):
    return {
        'name':         string(data, id, 0),
        'description':  string(data, id, 1),
        'icon':         v[2],

        'unmapped_values':      unmapped(
            list(range(3, 15)), v)
    }

def recipes(data, id, v):
    return {
        'level':        v[1],
        'result':       mat(v[2], v[3]),
        'mats':         [mat(v[i], v[i+1]) for i in range(4, 20, 2)],

        'unmapped_values':      unmapped(
            list(range(20, 31)), v)
    }

def text_commands(data, id , v):
    return {
        'name':                 string(data, id, 5),
        'small_name':           string(data, id, 6),
        'description':          string(data, id, 7),

        'unmapped_values':      unmapped(
            list(range(0, 5))
            + list(range(8, 10)), v)
    }

def titles(data, id , v):
    return {
        'name':                 string(data, id, 0),
        'plural_name':          string(data, id, 1),
        'unmapped_values':      unmapped(
            list(range(2, 3)), v)
    }

def towns(data, id , v):
    return {
        'name':            string(data, id, 0),
        'screen':          v[1],

        'unmapped_values':      unmapped(
            list(range(2, 4)), v)
    }

def traits(data, id, v):
    return {
        'name':         string(data, id, 0),
        'description':  string(data, id, 1),
        'icon':         v[2],
        'class_job':    ref('class_jobs', v[3]),
        'level':        v[4],

        'unmapped_values':      unmapped(
            list(range(5, 7)), v)
    }

def weathers(data, id , v):
    return {
        'icon':          v[0],
        'name':          string(data, id, 1)
    }

def worlds(data, id , v):
    return {
        'name':            string(data, id, 0),
        'message':         string(data, id, 1)
    }

