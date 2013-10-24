import logging
import re

from xivdm.language import get_language_name

def simple_mapping(exd_name, mapping_function):
    def generated_function(exd_manager):
        data = exd_manager.get_category(exd_name).get_data()
        data_ln = data[list(data.keys())[0]]
        return {
            id: mapping_function(data, id, v) for id, v in data_ln.items()
        }
    return generated_function

def string(data, id, member_id, enable_conditions = False):
    return {
        'enable_conditions': enable_conditions,
        'type': 'string',
        'ln': {
            get_language_name(language): data[language][id][member_id] for language in data.keys()
        }
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

def name_ref(view_name, value):
    return {
        'type': 'view_name_ref',
        'view': view_name,
        'name': value
    }

def unmapped(index_list, v):
    return {
        index: repr(v[index]) for index in index_list
    }

def food_stat(stat_type, percent_value, max_value):
    return {
        'stat': ref('base_params', stat_type),
        'percent_value': percent_value,
        'max_value': max_value
    }

def stat(stat_type, stat_value):
    return {
        'stat': ref('base_params', stat_type),
        'value': stat_value
    }

def hq_stat(stat_type, stat_value, hq_stat_value):
    return_value = stat(stat_type, stat_value)
    return_value.update({
        'hq_value': stat_value + hq_stat_value
    })
    return return_value

def mat(item_id, quantity):
    return {
        'item': ref('items', item_id),
        'quantity': quantity
    }

def crystals(crystal, amount):
    return {
        'crystal':     full_ref('craft_crystal_type', crystal),
        'amount':      amount
    }

def leve_stuff_range(return_dict, value):
    view_name = None

    if value == 0:
        pass
    elif value >= 917504:
        view_name = 'craft_leves'
    elif value >= 196608:
        view_name = 'company_leves'
    elif value >= 131072:
        view_name = 'gathering_leves'
    elif value >= 65536:
        view_name = 'battle_leves'
    elif value > 0:
        raise Exception('Unmapped id range: %d' % value)
    if view_name:
        return_dict[view_name] = ref(view_name, value)

def npc_stuff_range(return_dict, value):
    view_name = None

    if value == 0:
        pass
    elif value == 1835009:
        pass
    elif value > 1769484:
        raise Exception('Unmapped id range: %d' % value)
    elif value >= 1769472:
        view_name = 'special_shops'
    elif value >= 1703936:
        view_name = 'stories'
    elif value == 1638401:
        logging.info('Unmapped id range: %d' % value)
    elif value >= 1572864:
        view_name = 'guild_order_officers'
    elif value >= 1507328:
        view_name = 'guild_order_guides'
    elif value >= 1441792:
        view_name = 'gcshops'
    elif value >= 1179648:
        view_name = 'chocobo_taxi_stands'
    elif value >= 917504:
        view_name = 'craft_leves'
    elif value >= 720896:
        view_name = 'custom_talks'
    elif value >= 589824:
        view_name = 'default_talks'
    elif value >= 393216:
        view_name = 'guildleve_assignments'
    elif value >= 262144:
        view_name = 'shops'
    elif value >= 131072:
        view_name = 'gathering_leves'
    elif value >= 65536:
        #view_name = 'quests'
        pass #ignoring quests as it's too big
    elif value > 0:
        raise Exception('Unmapped id range: %d' % value)
    if view_name:
        return_dict.setdefault(view_name, []).append(full_ref(view_name, value))

def level_stuff_range(return_dict, value):
    view_name = None

    if value == 5000000:
        logging.info('Unmapped id range: %d' % value)
    elif value >= 2000000:
        view_name = 'eobjs'
    elif value >= 1000000:
        view_name = 'enpc_residents'
    elif value >= 30000:
        view_name = 'gathering_points'
    elif 30000 >= value > 0:
        logging.info('Unmapped id range BGMSituation: %d' % value)
    elif value > 0:
        raise Exception('Unmapped id range: %d' % value)

    if view_name:
        return_dict[view_name] = full_ref(view_name, value)

def gathering_items_range(return_dict, value):
    view_name = None

    if value < 2000000:
         view_name = 'items'
    elif value >= 2000000:
         view_name = 'event_items'
    elif value >= 3000000:
        raise Exception('Unmapped id range: %d' % value)

    if view_name:
        return_dict[view_name] = ref(view_name, value)

#### MAPPINGS ####
def achievements(data, id, v):
    return {
        'name':         string(data, id, 0),
        'description':  string(data, id, 1),
        'item':         ref('items', v[2]),
        'icon':         v[13],
        'category':     ref('achievement_categories', v[15]),


        'title':        ref('titles', v[12]),


        'points':       v[16],

        'unmapped_values':      unmapped(
            list(range(4, 12))
            + list(range(13, 16))
            + [17, 18], v)
    }

def achievement_categories(data, id, v):
    return {
        'name':     string(data, id, 0),
        'kind':     ref('achievement_kinds', v[1])
    }

def achievement_kinds(data, id, v):
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
        'description':          string(data, id, 1, enable_conditions = True),
        'icon':                 v[2],

        'resource_value':       v[5],

        'cast':                 v[8],
        'recast':               v[9],

        'category':             ref('action_categories', v[12]),

        'level':                v[15],
        'radius':               v[16],

        'resource_type':        v[18],

        'class_job_category':   ref('class_job_categories', v[25]),
        'class_job':            ref('class_jobs', v[27]),
        'range':                v[28],
        'attack_type':          ref('attack_types', v[29]),

        'unmapped_values':      unmapped(
            [3, 5, 6, 7, 10, 11, 13, 14]
            + list(range(18, 24))
            + [25]
            + list(range(29, 46)), v)
    }

def addons(data, id, v):
    return {
        'name': string(data, id, 0)
    }

def attack_types(data, id, v):
    return {
        'name': string(data, id, 0)
    }

def battle_leves(data, id, v):
    return {
        'mob': v[8],
        'mob_count': v[9],

        'unmapped_values':  unmapped(
            list(range(0, 8))
            + list(range(10, 183)), v)
    }


def balloons(data, id, v):
    return {
        'text': string(data, id, 0),

        'unmapped_values':  unmapped(
            [1], v)
    }

def base_params(data, id, v):
    return {
        'name'          : string(data, id, 0),
        'description'   : string(data, id, 1),
        'unmapped_values':      unmapped(
            list(range(1, 32)), v)
    }

def behest_rewards(data, id, v):
    return {
        'items': [ref('items', v[i]) for i in range(1, 4)],

        'level': v[5],

        'unmapped_values':      unmapped(
            [0]
            + [4]
            + [6], v)
    }

def bnpc_names(exd_manager):
    data = exd_manager.get_category('BNpcName').get_data()
    data_ln = data[list(data.keys())[0]]

    bnb_data = exd_manager.get_category('BNpcBase').get_data()
    bnpc_bases = bnb_data[list(bnb_data.keys())[0]]

    return_dict = {}
    for id, v in data_ln.items():
        return_dict[id] = {
            'name':                 string(data, id, 0),
            'plural_name':          string(data, id, 1),
            'unmapped_values':      unmapped(
            list(range(2, 8)), v)
        }
        if id in bnpc_bases:
            return_dict[id].update({
                'infos':                full_ref('bnpc_bases', id)
            })
    return return_dict

def bnpc_bases(data, id, v):
    return {
        'model':                full_ref('model_chara', v[3]),
        'unmapped_values':      unmapped(
            list(range(0, 3))
                + list(range(4,13)), v)
    }
def chain_bonuses(data, id, v):
    return {
        'exp_percent':  v[0],
        'timer':        v[1]
    }

def chocobo_taxi_stands(data, id, v):
    return {
        'name':                 string(data, id, 0),

        'unmapped_values':      unmapped(
            list(range(1, 9)), v)
    }

def class_job_categories(data, id, v):
    return {
        'name':                     string(data, id, 0),
        'class_job_restrictions':   [v[index] for index in range(1, 30)]
    }

def class_jobs(data, id, v):
    return {
        'name':                 string(data, id, 0),
        'acronym':              string(data, id, 1),

        'caps_name':            string(data, id, 3),
        'class_job_category':   ref('class_job_categories', v[4]),

        'base_class':           ref('class_jobs', v[24]),
        'is_job':               v[31],


        'unmapped_values':  unmapped(
            [2]
            + list(range(6, 25))
            + list(range(26, 31)), v)
    }

def companions(data, id, v):
    return {
        'name':                 string(data, id, 0),
        'plural_name':          string(data, id, 1),

        'icon':                 v[10],

        'unmapped_values':      unmapped(
            list(range(2, 10))
            + list(range(11, 15)), v)
    }

def complete_journals(data, id, v):
    return {
        'name':             string(data, id, 0),

        'header_image':     v[3],

        'unmapped_values':      unmapped(
            [1, 2]
            + list(range(4, 6)), v)
    }

def completions(data, id, v):
    return {
        'name':                 string(data, id, 0),

        'unmapped_values':      unmapped(
            list(range(1, 4)), v)
    }

def company_leves(data, id, v):
    return {
        'unmapped_values':  unmapped(
            list(range(0, 178)), v)
    }

def craft_crystal_type(data, id, v):
    return {
        'item':                 ref('items', v[0])
    }

def craft_leves(data, id, v):
    return {
        'unmapped_values':      unmapped(
            list(range(0, 15)), v)
    }

def craft_action(data, id, v):
    return {
        'name':             string(data, id, 0),
        'description':      string(data, id, 1),

        'icon':             v[4],
        'class_job':        ref('class_jobs', v[8]),
        'class_job_category':   ref('class_job_categories', v[5]),
        'level':            v[6],
        'cp':               v[7],

        'unmapped_values':      unmapped(
            [2, 3], v)
    }

def craft_types(data, id, v):
    return {
        'name':                 string(data, id, 0),

        'unmapped_values':      unmapped(
            [1, 2], v)
    }

def custom_talks(data, id, v):
    return {
        'unmapped_values':      unmapped(
            list(range(0, 68)), v)
    }

def default_talks(data, id, v):
    return {
        'unmapped_values':      unmapped(
            list(range(0, 21)), v)
    }

def emotes(data, id, v):
    return {
        'name':         string(data, id, 0),
        'icon':         v[8],

        'unmapped_values':      unmapped(
            list(range(1, 8))
            + list(range(9, 19)), v)
    }

def enpc_residents(data, id, v):
    return {
        'name':                 string(data, id, 0),
        'name_bis':             string(data, id, 1),
        'title':                string(data, id, 2),

        'infos':                full_ref('enpc_bases', id),

        'unmapped_values':      unmapped(
            list(range(3, 10)), v)
    }

def enpc_bases(data, id, v):
    return_dict = {
        'model':            v[32],
        'unmapped_values':      unmapped(
            [30, 31]
            + list(range(33, 63))
            + list(range(65, 93)), v)
    }
    for i in range(30):
        npc_stuff_range(return_dict, v[i])
    return return_dict

def eobjs(data, id, v):
    return {
        'name':                 string(data, id, 0),
        'description':          string(data, id, 1),

        'unmapped_values':          unmapped(
            list(range(2, 14)), v)
    }

def errors(data, id, v):
    return {
        'name':                 string(data, id, 0)
    }

def event_items(data, id, v):
    return {
        'name':                 string(data, id, 0),
        'name_plural':          string(data, id, 1),
        'description':          string(data, id, 2),
        'description_bis':      string(data, id, 3),

        'quest':                ref('quests', v[10]),


        'unmapped_values':          unmapped(
            list(range(4, 10))
            + list(range(11, 15)), v)
    }

def fates(data, id, v):
    return {
        'name':                 string(data, id, 0),
        'description':          string(data, id, 1),
        'special_text':         [string(data, id, i) for i in range(2, 5)],

        'position':             full_ref('levels', v[8]),

        'icon':                 v[10],

        'level':                v[18],

        'unmapped_values':          unmapped(
            list(range(5, 9))
            + [10]
            + list(range(12, 18))
            + list(range(19, 24)), v)
    }


def gathering_type(data, id, v):
    return {
        'name':          string(data, id, 0),
        'unmapped_values':          unmapped(
            [1], v)
    }

def gathering_points(exd_manager):
    data = exd_manager.get_category('GatheringPoint').get_data()
    data_ln = data[list(data.keys())[0]]
    return_dict = {}

    maps_data = exd_manager.get_category('Map').get_data()
    maps_data_in = maps_data[list(maps_data.keys())[0]]

    maps_search_dict = {
        m_data[7]: m_id for m_id, m_data in maps_data_in.items()
    }

    for id, v in data_ln.items():
        return_dict[id] = {
            'base':                 full_ref('gathering_points_base', v[0]),

            'req':                  ref('gathering_condition', v[1]),
            'bonus':                ref('gathering_bonus_type', v[2]),

            'map':                  ref('maps', maps_search_dict[v[3]]),

            'req_max':              v[4],
            'bonus_amount':         v[5],

            'unmapped_values':          unmapped(
                list(range(6, 9)), v)
        }
    return return_dict

def gathering_points_base(data, id, v):
    return {
        'node_name':    full_ref('gathering_type', v[0]),
        'items':        [full_ref('gathering_items', v[i]) for i in range(1, 9)],
        'level':        v[9],

        'unmapped_values':          unmapped(
            list(range(10, 11)), v)
    }

def gathering_items(data, id, v):
    return_dict = {
        'gathering_level': v[1]
    }
    gathering_items_range(return_dict, v[0])
    return return_dict

def gathering_points_name(data, id, v):
    return {
        'name':          string(data, id, 0),
        'unmapped_values':          unmapped(
            list(range(1, 8)), v)
    }

def gathering_leves(data, id, v):
    return {
        'unmapped_values':          unmapped(
            list(range(0, 19)), v)
    }

def gathering_condition(data, id, v):
    return {
        'name':          string(data, id, 0)
    }

def gathering_bonus_type(data, id, v):
    return {
        'name':          string(data, id, 0)
    }

def gcrank(data, id, v):
    return {
        'name':                 string(data, id, 0),
        'plural':               string(data, id, 1),

        'unmapped_values':          unmapped(
            list(range(2, 10)), v)
    }

def gcshops(data, id, v):
    return {
        'unmapped_values':          unmapped(
            list(range(0, 2)), v)
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
            [2], v)
    }

def grand_companies(data, id, v):
    return {
        'name':                 string(data, id, 0),

        'unmapped_values':      unmapped(
            list(range(1, 10)), v)
    }

def grand_company_ranks(data, id, v):
    return {
        'rank':                 v[8],
        'max_seals':            v[9],

        'unmapped_values':      unmapped(
            list(range(0, 8))
            + [10], v)
    }

def grand_company_seal_shop_items(data, id, v):
    return {
        'seal_cost':            v[1],
        'item':                 ref('items', v[2]),

        'category':             ref('gcshop_item_categories', v[4]),

        'unmapped_values':      unmapped(
            [0]
            + [3], v)
    }

def guardian_deities(data, id, v):
    return {
        'name':                 string(data, id, 0),
        'description':          string(data, id, 1),
        'icon':                 v[2],
    }

def guild_order_guides(data, id, v):
    return {
        'unmapped_values':      unmapped(
            list(range(0, 6)), v)
    }

def guild_order_officers(data, id, v):
    return {
        'unmapped_values':      unmapped(
            list(range(0, 6)), v)
    }


def guildleve_assignments(data, id, v):
    return {
        'unmapped_values':      unmapped(
            list(range(0, 7)), v)
    }

def instance_contents(exd_manager):
    data = exd_manager.get_category('InstanceContent').get_data()
    data_ln = data[list(data.keys())[0]]
    return_dict = {}
    for id, v in data_ln.items():
        return_dict[id] = {
            'name':                 string(data, id, 0),
            'lore':                 string(data, id, 1),
            
            'banner':               v[4],
            
            'todo_start':           v[8],
            'todo_end':             v[9],
            
            'time':                 v[10],

            'type':                 full_ref('instance_content_type', v[14]),
            'minlvl':               v[15],
            'synclvl':              v[16],

            'playercount':          v[18],
            
            

            'unmapped_values':      unmapped(
                list(range(1, 10))
                + list(range(11, 13))
                + list(range(17, 20))
                + list(range(21, 27)), v)
        }
        if v[14] > 10000:
            return_dict[id].update({
                'issuenpc': ref('enpc_residents', v[13])
            })
    return return_dict

def instance_content_textdata(data, id, v):
    return {
        'text':               string(data, id, 0)
    }
    
def instance_content_type(data, id, v):
    return {
        'info':                 full_ref('addons', v[0]),
        'icon':                 v[1],

        'unmapped_values':      unmapped(
            list(range(2, 5)), v)
    }

def item_actions(data, id, v):
    action_type = v[1]
    if action_type in [48, 49]:
        return {
            'item_food':    full_ref('item_foods', v[2]),
            'duration':     v[3],
        }
    else:
        return {
            'percentage':    v[1],
            'value_max':     v[2],
         }

def item_categories(data, id, v):
    return {
        'name': string(data, id, 0)
    }

def item_foods(data, id, v):
    return {
        'stats': [                  food_stat(v[0], v[3], v[6]),
                                    food_stat(v[1], v[4], v[7]),
                                    food_stat(v[2], v[5], v[8])],

        'unmapped_values':          unmapped(
            list(range(9, 18)), v)
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
             [1], v)
    }

def item_special_bonuses(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def item_series(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def item_ui_categories(data, id, v):
    return {
        'name': string(data, id, 0),
        'icon': v[1]
    }

def items(data, id, v):
    return {
            'noon':                     string(data, id, 0),
            'plural_noon':              string(data, id, 1),
            'description':              string(data, id, 2),
            'name':                     string(data, id, 3),

            'model':                    v[10],

            'number_per_stack':         v[12],

            'buy_price':                v[15],

            'stats':                    [hq_stat(v[i], v[i+25], v[i+52]) for i in range(19, 23)]
                                        + [stat(v[i], v[i+25]) for i in range(23, 25)],

            'set_stats': {
                                        'special_bonus':    ref('item_special_bonuses', v[59]),
                                        'stats':            [stat(v[i], v[i+44]) for i in range(25, 31)]
            },

            'repair_class_job':         ref('class_jobs',                   v[31]),
            'repair_material':          ref('items',                        v[32]),
            'icon':                     v[33],

            'base_stats': [             hq_stat(12, v[35], v[69]),  # physical_damage
                                        hq_stat(13, v[36], v[70]),  # magic_damage
                                        stat(14, v[37]),  # delay
                                        stat(17, v[38]),  # block_rate
                                        stat(18, v[39]),  # block
                                        hq_stat(21, v[40], v[69]),  # defense
                                        hq_stat(24, v[41], v[70])], # magic_defense

            'item_action':              full_ref('item_actions',                   v[43]),

            'item_level':               v[50],
            'class_job_level':          v[51],

            'item_ui_category':         ref('item_ui_categories',              v[53]),

            'rarity':                   v[55],

            'materia_slots':            v[57],

            'item_search_class_filter': ref('item_search_class_filters',    v[60]),

            'class_job_category':       ref('class_job_categories',         v[64]),
            'grand_company':            ref('grand_companies',              v[65]),

            'set_name':                 ref('item_series',                  v[67]),

            'is_unique':                v[82],
            'is_untradable':            v[83],

            'race_restrictions':        [v[i] for i in range(87, 92)],
            'gender_restrictions':      [v[i] for i in range(92, 94)],



            'unmapped_values':          unmapped(
                list(range(4, 10))
                + [11]
                + [13]
                + [14]
                + list(range(16, 19))
                + [34]
                + [42]
                + [52]
                + [54]
                + [56]
                + [58]
                + list(range(61, 64))
                + [66]
                + [68]
                + list(range(76, 82))
                + list(range(84, 87)), v)
    }

def journal_genre(data, id , v):
    return {
        'name':         string(data, id, 0),
        'icon':         v[1],
        'cat':          ref('journal_cat', v[2])
    }

def journal_cat(data, id , v):
    return {
        'name':         string(data, id, 0)
    }


def leve_reward_item_groups(data, id, v):
    return {
        'items':  [mat(v[i], v[i+8]) for i in range(0, 8)]
    }

def leve_reward_items(data, id, v):
    return {
        'leve_reward_item_groups':  [ref('leve_reward_item_groups', v[i]) for i in range(0, 7)]
    }

def leves(data, id, v):
    return_dict = {
        'name':                 string(data, id, 0),
        'description':          string(data, id, 1),

        'reward_item':          full_ref('leve_reward_items', v[4]),

        'start_npc':            full_ref('levels', v[7]),
        'start_position':       full_ref('levels', v[8]),
        'client':               ref('leve_clients', v[9]),

        'placename':            ref('place_names', v[13]),
        'genre':                v[14],
        
        'guildleve_eorzean':    v[17],
        'guildleve_banner':     v[19],

        'level':                v[20],
        'timelimit':            v[22],
        'leve_fx':              v[24],

        'unmapped_values':      unmapped(
            [2, 3] 
            + [5, 6]
            + list(range(10, 13))
            + list(range(14, 17))
            + [19]
            + [21]
            + list(range(23, 29)), v)
    }
    leve_stuff_range(return_dict, v[18])
    return return_dict

def leves_vfx(data, id , v):
    return {
        'file':         string(data, id, 0),
        'image':        v[1]
    }
    
def levels(data, id, v):
    return_dict = {
        'x':                    v[0],
        'y':                    v[2],

        'map':                  full_ref('maps',v[6]),

        'place_name':           ref('place_names', v[8]),

        'unmapped_values':      unmapped(
            [1]
            + list(range(3, 5))
            + [7]
            + [9], v)
    }
    level_stuff_range(return_dict, v[5])
    return return_dict


def param_grow(data, id, v):
    return {
        'exp':               v[0],

        'unmapped_values':      unmapped(
            list(range(1, 12)), v)
    }

def pet_action(data, id, v):
    return {
        'name':               string(data, id, 0),
        'description':        string(data, id, 1, enable_conditions = True),
        'pet':                v[4], 
        'icon':               v[2], 

        'unmapped_values':      unmapped(
            list(range(3, 7)), v)
    }



def leve_clients(data, id, v):
    return {
        'name':                 string(data, id, 0)
    }

def maps(data, id, v):
    return {
        'id':                   v[0].decode('utf-8'),
        'scale':                v[1],
        'floor':                v[12],

        'zone':                 full_ref('place_names', v[3]),
        'region':               full_ref('place_names', v[4]),

        'pseudo_link':          v[7], #used to link gathering points to maps and maybe others

        'unmapped_values':      unmapped(
            [2]
            + [5, 6]
            + list(range(8, 14)), v)
    }

def markers(data, id, v):
    return {
        'name':                 string(data, id, 0),
        'icon':                 v[1]
    }
def mounts(data, id, v):
    return {
        'name':                 string(data, id, 0),
        'icon':                 v[39]
    }

def model_chara(data, id, v):
    return {
        'm_value':              v[0],
        'b_value':              v[3],
        'unmapped_values':      unmapped(
            list(range(1, 3))
            + list(range(4, 6)), v)
    }

def materias(data, id, v):
    return {
        'mat':                  [{
                                    'item': ref('items', v[i]),
                                    'value': v[i+11]
                                } for i in range(5)],
        'attribute':            ref('base_params', v[10]),

        'unmapped_values':      unmapped(
            list(range(5, 10))
            + list(range(16, 21)), v)
    }

def monster_notes(data, id, v):
    return {
        'name':                 string(data, id, 0),
        'exp':                  v[1],
        'npcs':                 [full_ref('monster_notes_target', v[i]) for i in range(2, 6)],

        'npc_quantities':       [v[i] for i in range(6, 10)],

        'unmapped_values':      unmapped(
            [5]
            + [9], v)
    }

def monster_notes_target(data,id,v):
    return {
        'mob':                 ref('bnpc_names', v[0]),
        'icon':                 v[1],

        'unmapped_values':      unmapped(
            list(range(2, 9)), v)
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

def place_names(data, id, v):
    return {
        'name':                 string(data, id, 0),

        'unmapped_values':      unmapped(
            list(range(1, 10)), v)
    }

QUEST_STEP_RE = re.compile(r'^SEQ_(?P<step_number>\d+)_(?P<step_action>.*)$')
QUEST_ACTOR_RE = re.compile(r'^ACTOR(\d+)$')

def quest_steps(labels, ids):
    result_steps = []
    actor_dict = {}
    for index, label in enumerate(labels):
        label_utf8 = label.decode('utf-8')

        actor_match_result = QUEST_ACTOR_RE.match(label_utf8)
        if actor_match_result:
            if ids[index] >= 10000:
                actor_dict[label_utf8] = ids[index]
        else:
            step_match_result = QUEST_STEP_RE.match(label_utf8)
            if step_match_result:
                step_action = step_match_result.group('step_action')
                actor_match_result = QUEST_ACTOR_RE.match(step_action)
                if actor_match_result:
                    if step_action in actor_dict:
                        result_steps.append({
                            'step': int(step_match_result.group('step_number')),
                            'value': ref('enpc_residents', actor_dict[step_action])
                        })
    return result_steps

def quests(exd_manager):
    data = exd_manager.get_category('Quest').get_data()
    data_ln = data[list(data.keys())[0]]
    return_dict = {}

    param_grow_data = exd_manager.get_category('ParamGrow').get_data()
    param_grow_data_ln = param_grow_data[list(param_grow_data.keys())[0]]

    complete_journal_data = exd_manager.get_category('CompleteJournal').get_data()
    complete_journal_data_in = complete_journal_data[list(complete_journal_data.keys())[0]]

    complete_journal_search_dict = {
        cj_data[0]: cj_id for cj_id, cj_data in complete_journal_data_in.items()
    }


    for id, v in data_ln.items():
        return_dict[id] = {
            'name':                 string(data, id, 0),

            'vars':                 [[v[i].decode('utf-8'), v[i+1]] for i in range(1, 51, 2)],

            'structs':              [v[i:i+15] for i in range(116, 1048, 15)],

            'gil_reward':           v[1301],

            'main_rewards':         [mat(v[i], v[i+25]) for i in range(1302, 1305)],
            'optional_rewards':     [mat(v[i], v[i+31]) for i in range(1308, 1313)],

            'base_exp':             v[1318],

            'prerequisit_quests':   [ref('quests', v[i]) for i in range(1352, 1355)],
            
            'start':                v[1360],
            'end':                  v[1361],
            'banner':               v[1362],

            'level':                (v[1363] if v[1363] != 0xFFFF else 0) + v[1372],

            'class_job':            ref('class_jobs', v[1385]),
            'genre':                v[1386],



 #          'name':                 string(data, id, 0),
 #
 #          'level':                (v[1165] if v[1165] != 0xFFFF else 0) + v[1170],
 #
 #          'class':                v[1176],
 #
 #          'chain_quests':         [ref('quests', v[i]) for i in range(1157, 1160)],
 #
 #          'steps':                quest_steps([v[i] for i in range(1, 100, 2)], [v[i] for i in range(2, 101, 2)]),
 #
 #          'base_exp':             v[1124],
 #          'gil_reward':           v[1109],
 #
 #          'main_rewards':         [mat(v[i], v[i+3]) for i in range(1127, 1130)]
 #                                  + [mat(v[i], v[i+23]) for i in range(1110, 1113)],
 #
 #          'optional_rewards':     [mat(v[i], v[i+32]) for i in range(1113, 1118)],
        }
 #
        return_dict[id].update({
            'exp_reward': (return_dict[id]['base_exp'] * (param_grow_data_ln[return_dict[id]['level']][11] * (45 + 5 * return_dict[id]['level']))) // 100
        })
 #
 #      #Lookup complete journal by name and extract genre id (v[4])
 #      if complete_journal_data_in[complete_journal_search_dict[v[0]]][2] <= 49: #TEMP FIX UNTIL SE FIXES THEIR SHIT
 #          return_dict[id].update({
 #              'quest_genre': ref('journal_genre', complete_journal_data_in[complete_journal_search_dict[v[0]]][2])
 #          })
 #
 #      #Check second class column if first one is empty SERIOUSLY SE FIX YOUR SHIT
 #      if v[1176] == 0:
 #          return_dict[id].update({
 #              'class': v[1179]
 #          })
 #
        if v[1351] != b'':
            quest_base_exd_name = v[1351].decode('utf-8')
            quest_exd_name = 'quest/%s/%s' % (quest_base_exd_name[10:13], quest_base_exd_name)
            quest_exd_data = exd_manager.get_category(quest_exd_name).get_data()
            quest_exd_data_ln = quest_exd_data[list(quest_exd_data.keys())[0]]
            return_dict[id].update({
                'texts': {
                    quest_exd_data_ln[quest_exd_id][0].decode('utf-8'): {
                        'enable_conditions': False,
                        'type': 'string',
                        'ln': {
                            get_language_name(language): quest_exd_data[language][quest_exd_id][1] for language in quest_exd_data.keys()
                        }
                    } for quest_exd_id in sorted(quest_exd_data_ln.keys())
                }
            })
  
    return return_dict

def roles(data, id , v):
    return {
        'name':                 string(data, id, 0),
        'abbr':                 string(data, id, 1),

        'unmapped_values':      unmapped(
            [2], v)
    }

def shops(data, id , v):
    return {
        'name':                 string(data, id, 0),
        'icon':                 v[1],
        'items':                [full_ref('shop_items', v[i]) for i in range(2, 42)],

        'unmapped_values':      unmapped(
            [42], v)
    }

def shop_items(data, id , v):
    return {
        'item':                 ref('items', v[3]),

        'unmapped_values':      unmapped(
            list(range(0, 3))
            + list(range(4, 6)), v)
    }

def special_shops(data, id , v):
    return {
        'name':                 string(data, id, 0),

        'items':                [{
                                    'out': mat(v[i+3], v[i]),
                                    'in': [mat(v[i+5], v[i+1]),
                                           mat(v[i+6], v[i+2])]}
                                           for i in range(1, 1121, 7)]
    }

def statuses(data, id, v):
    return {
        'name':             string(data, id, 0),
        'description':      string(data, id, 1),
        'icon':             v[2],
        'company_action':   v[15],

        'unmapped_values':      unmapped(
            list(range(3, 16)), v)
    }

def recipes(data, id, v):
    return {
        'craft_type':   ref('craft_types', v[0]),
        'result':       mat(v[1], v[20]),

        'mats':         [mat(v[i], v[i+19]) for i in range(2, 10)],
        'crystals':     [crystals(v[i], v[i+19]) for i in range(10, 12)],
        'level':        v[19],
        'required':     v[18],
        'affinity':     v[31],

        'unmapped_values':      unmapped(
            list(range(20, 31)), v)
    }

def stories(data, id, v):
    return {
        'story_name':   v[1310].decode('utf-8')
    }

def text_commands(data, id , v):
    return {
        'description':          string(data, id, 0),

        'name':                 string(data, id, 3),
        'small_name':           string(data, id, 4),

        'unmapped_values':      unmapped(
            list(range(1, 3))
            + list(range(5, 11)), v)
    }

def titles(data, id , v):
    return {
        'name':                 string(data, id, 0),
        'plural_name':          string(data, id, 1),
        'unmapped_values':      unmapped(
            [2], v)
    }

def towns(data, id , v):
    return {
        'name':            string(data, id, 0),
        'screen':          v[1]
    }

def traits(data, id, v):
    return {
        'name':         string(data, id, 0),
        'description':  string(data, id, 1),
        'icon':         v[2],
        'class_job':    ref('class_jobs', v[4]),
        'level':        v[5],

        'unmapped_values':      unmapped(
            [3] + [6], v)
    }

def weathers(data, id , v):
    return {
        'name':          string(data, id, 0),
        'icon':          v[1]
    }

def worlds(data, id , v):
    return {
        'message':         string(data, id, 0),
        'name':            string(data, id, 1)
    }

def warps(data, id , v):
    return {
        'name':            string(data, id, 1),
        'map':             full_ref('levels', v[2])
    }

