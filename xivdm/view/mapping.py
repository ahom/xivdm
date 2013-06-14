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
        'stat': ref('base_params', stat_type),
        'percent_value': percent_value,
        'max_value': max_value
    }

def stat(stat_type, stat_value):
    return {
        'stat': ref('base_params', stat_type),
        'value': stat_value
    }

def mat(item_id, quantity):
    return {
        'item': ref('items', item_id),
        'quantity': quantity
    }

def npc_stuff_range(return_dict, value):
    view_name = None

    if value == 0:
        pass
    elif value > 1703937:
        raise Exception('Unmapped id range: %d' % value)
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
        view_name = 'quests'
    elif value > 0:
        raise Exception('Unmapped id range: %d' % value)
    if view_name:
        return_dict.setdefault(view_name, []).append(ref(view_name, value))

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

        'radius':               v[22],

        'resource_type':        v[24],
        'resource_value':       v[25],

        'cast':                 v[30],
        'recast':               v[31],

        'attack_type':          ref('attack_types', v[33]),

        'class_job_category':   ref('class_job_categories', v[41])
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

def chocobo_taxi_stands(data, id, v):
    return {
        'name':                 string(data, id, 8),

        'unmapped_values':      unmapped(
            list(range(0, 8)), v)
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

        'class_job_category':   ref('class_job_categories', v[3]),

        'base_class':           ref('class_jobs', v[19]),
        'is_job':               v[20],
        'caps_name':            string(data, id, 21),

        'caps_full_name':       string(data, id, 25),

        'unmapped_values':  unmapped(
            list(range(2, 3))
            + list(range(4, 19))
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

def craft_leves(data, id, v):
    return {
        'unmapped_values':      unmapped(
            list(range(0, 15)), v)
    }

def craft_types(data, id, v):
    return {
        'name':                 string(data, id, 2),

        'unmapped_values':      unmapped(
            list(range(0, 2)), v)
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
        'icon':         v[15],
        'name':         string(data, id, 14),

        'unmapped_values':      unmapped(
            list(range(1, 14))
            + list(range(15, 19)), v)
    }

def enpc_residents(data, id, v):
    return {
        'name':                 string(data, id, 0),

        'name_bis':             string(data, id, 2),

        'title':                string(data, id, 8),

        'infos':                full_ref('enpc_bases', id),
    }

def enpc_bases(data, id, v):
    return_dict = {}
    for i in range(2, 32):
        npc_stuff_range(return_dict, v[i])
    return return_dict

def eobjs(data, id, v):
    return {
        'name':                 string(data, id, 0),

        'description':          string(data, id, 2),

        'unmapped_values':          unmapped(
            list(range(1, 2))
            + list(range(3, 14)), v)
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
        #'level':                v[7],
		#'icon':                	v[18],
		
        'name':                 string(data, id, 17),
        'description':          string(data, id, 18),
        'special_text_1':       string(data, id, 19),
        'special_text_2':       string(data, id, 20),
        'special_text_3':       string(data, id, 21),
        'special_text_4':       string(data, id, 22),

        'unmapped_values':          unmapped(
            list(range(0, 17)), v)
    }

def gathering_leves(data, id, v):
    return {
        'unmapped_values':          unmapped(
            list(range(0, 19)), v)
    }    

def gcrank(data, id, v):
    return {
        'name':                 string(data, id, 0),

        'plural':               string(data, id, 2),

        'unmapped_values':          unmapped(
            list(range(1, 2))
            + list(range(3, 10)), v)
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

        'unmapped_values':      unmapped(
            list(range(1, 3)), v)
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
            list(range(0, 3)), v)
    }

#def guildleve_offers(data, id, v):
#    return {
#        'unmapped_values':      unmapped(
#            list(range(0, 2)), v)
#    }

def instance_contents(data, id, v):
    return {
        'name':                 string(data, id, 1),  

        'unmapped_values':          unmapped(
            list(range(0, 1))
            + list(range(2, 6)), v)
    }

def item_actions(data, id, v):
    action_type = v[4]
    if action_type in [48, 49]:
        return {
            'item_food':    full_ref('item_foods', v[5]),
            'duration':     v[6],
        }
    else:
        return {
            'unmapped_values': unmapped(list(range(0, 22)), v)
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
            'item_ui_category':         ref('item_ui_categories',              v[17]),

            'rarity':                   v[19],

            'stats':                    [stat(v[i], v[i+1]) for i in range(32, 44, 2)],

            'repair_class_job':         ref('class_jobs',                   v[57]),
            'repair_material':          ref('items',                        v[58]),
            'item_search_class_filter': ref('item_search_class_filters',    v[59]),
        
            'base_stats': [             stat(12, v[61]),  # physical_damage
                                        stat(13, v[62]),  # magic_damage
                                        stat(14, v[63]),  # delay

                                        stat(18, v[65]),  # block
                                        stat(17, v[66]),  # block_rate
                                        stat(21, v[67]),  # defense
                                        stat(24, v[68])], # magic_defense

            'item_action':              full_ref('item_actions',                   v[71]),

            'is_unique':                v[73],
            'is_untradable':            v[74],

            'buy_price':                v[76],

            'race_restrictions':        [v[i] for i in range(81, 86)],
            'gender_restrictions':      [v[i] for i in range(86, 88)],
            'class_job_category':       ref('class_job_categories',         v[88]),

            'grand_company':            ref('grand_companies',              v[90]),

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
        
        'unmapped_values':      unmapped(
            list(range(3, 4))
            + list(range(7, 8)), v)
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

def base_params(data, id, v):
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

    for id, v in data_ln.items():
        return_dict[id] = {
            'name':                 string(data, id, 0),

            'level':                v[3],

            'class':                v[14],

            'chain_quests':         [ref('quests', v[i]) for i in range(8, 11)],

            #'npcs':                 [ref('enpc_residents', v[17]),
            #                         ref('enpc_residents', v[18])],    

            'steps':                quest_steps(v[24:74], v[74:124]),

            'gil_reward':           v[1134],

            #'main_reward':          mat(v[728], v[729]),
            
            #'optional_rewards':     [mat(v[i], v[i+1]) for i in range(750, 766, 3)],
        }

        if v[1] != b'':
            quest_base_exd_name = v[1].decode('utf-8')
            quest_exd_name = 'quest/%s/%s' % (quest_base_exd_name[10:13], quest_base_exd_name)
            quest_exd_data = exd_manager.get_category(quest_exd_name).get_data()
            quest_exd_data_ln = quest_exd_data[list(quest_exd_data.keys())[0]]
            return_dict[id].update({
                'text_ids':         [
                    quest_exd_data_ln[quest_exd_id][0].decode('utf-8') for quest_exd_id in sorted(quest_exd_data_ln.keys())
                ],
                'texts': {
                    get_language_name(language): [
                        quest_exd_data[language][quest_exd_id][1] for quest_exd_id in sorted(quest_exd_data_ln.keys())
                    ] for language in quest_exd_data.keys()
                }  
            })
        
    return return_dict

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
        'items':                [full_ref('shop_items', v[i]) for i in range(2, 42)],

        'name':                 string(data, id, 42),
        'unmapped_values':      unmapped(
            list(range(0, 1)), v)
    }

def shop_items(data, id , v):
    return {
        'item':                 ref('items', v[0]),

        'unmapped_values':      unmapped(
            list(range(1, 6)), v)
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
        'craft_type':   ref('craft_types', v[0]),
        'level':        v[1],
        'result':       mat(v[2], v[3]),
        'mats':         [mat(v[i], v[i+1]) for i in range(4, 20, 2)],

        'unmapped_values':      unmapped(
            list(range(20, 31)), v)
    }

def stories(data, id, v):
    return {
        'story_name':                 string(data, id, 0)
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
        'screen':          v[1]
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

