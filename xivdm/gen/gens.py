import logging

from xivdm.crc32_utils import crc_32, rev_crc_32
from xivdm.dat.Manager import get_hash

def icons(dat_manager):
    icons_result_tree = {}
    for i in range(1000):
        folder = i * 1000
        key = '%0.6d' % folder
        folder_path = 'ui/icon/%s/' % key

        children = {}
        if dat_manager.check_dir_existence(folder_path):
            for j in range(1000):
                file_key = '%0.6d' % (folder + j)
                file_path = '%s%s.dds' % (folder_path, file_key)
                if dat_manager.check_file_existence(file_path):
                    children[file_key] = file_path

        for ln in ['en', 'fr', 'de', 'ja']:
            ln_folder_path = '%s%s/' % (folder_path, ln)
            if dat_manager.check_dir_existence(ln_folder_path):
                for j in range(1000):
                    file_key = '%0.6d' % (folder + j)
                    file_path = '%s%s.dds' % (ln_folder_path, file_key)
                    if dat_manager.check_file_existence(file_path):
                        children.setdefault(ln, {})[file_key] = file_path

        if children:
            icons_result_tree[key] = children
    return icons_result_tree

def maps_icons(dat_manager):
    maps_icons_result_tree = {}
    for a in map(chr, range(ord('a'), ord('z') + 1)):
        for i in range(10):
            for b in map(chr, range(ord('a'), ord('z') + 1)):
                for j in range(10):
                    for k in range(100):
                        basename = '%s%d%s%d' % (a, i, b, j)
                        num = '%0.2d' % k
                        folder_path = 'ui/map/%s/%s/' % (basename, num)
                        file_path = '%s%s%sm.dds' % (folder_path, basename, num)
                        if dat_manager.check_file_existence(file_path):
                            maps_icons_result_tree.setdefault(basename, {}).setdefault(num, []).append(file_path)
                        if dat_manager.check_file_existence('%s%s%s_0_0.dds' % (folder_path, basename, num)):
                            for x in range(32):
                                for y in range(32):
                                    file_path = '%s%s%s_%d_%d.dds' % (folder_path, basename, num, x, y)
                                    if dat_manager.check_file_existence(file_path):
                                        maps_icons_result_tree.setdefault(basename, {}).setdefault(num, []).append(file_path)
    return maps_icons_result_tree

def find_filename_hash(hash_table, filename):
    results = []
    input_file_hash = get_hash(filename)
    for dir_hash, dir_hash_table in hash_table.items():
        if input_file_hash in dir_hash_table:
            results.append(dir_hash)
    return results

def get_rev_digits_values_matches(prefix_value, suffix_value, hash_dict):
    results = {}
    prefix_crc = crc_32(bytes(prefix_value, encoding='ascii'), 0xFFFFFFFF)
    for dir_hash, file_hash_list in hash_dict.items():
        for file_hash in file_hash_list:
            value = get_rev_digits_values(prefix_crc, suffix_value, file_hash)
            if value:
                results.setdefault(dir_hash, {})[file_hash] = value
    return results

def get_rev_digits_values(prefix_crc, suffix_value, final_crc):
    rev_patched_crc = rev_crc_32(bytes(suffix_value, encoding='ascii'), final_crc)
    rev_crc = prefix_crc ^ rev_patched_crc

    values = [(rev_crc & (0xFF << (i * 8))) >> (i * 8) for i in range(4)]

    for value in values:
        if not(0x30 <= value < 0x40):
            return None
    return ''.join(chr(c) for c in values)

def models(dat_manager):
    models_result_tree = {}

    # Data hash table for chara dat
    chara_cat_hash_table = dat_manager.get_category('chara').get_hash_table()

    # Humans
    # Search for chara/xls/attachOffset/c%04d.atch
    attach_offset_search_folder_hash = get_hash('chara/xls/attachoffset')
    if attach_offset_search_folder_hash in chara_cat_hash_table:
        prefix_crc = get_hash('c')
        for file_hash in chara_cat_hash_table[attach_offset_search_folder_hash].keys():
            c_value = get_rev_digits_values(prefix_crc, '.atch', file_hash)
            if c_value:
                for part, suffix in [('face', 'fac'), ('hair', 'hir'), ('tail', 'til'), ('body', 'top')]:
                    for p in range(10000):
                        p_value = '%0.4d' % p
                        p_name = '%s%s' % (part[0], p_value)
                        file_path = 'chara/human/c%s/obj/%s/%s/model/c%s%s_%s.mdl' % (c_value, part, p_name, c_value, p_name, suffix)
                        if dat_manager.check_file_existence(file_path):
                            models_result_tree.setdefault('human', {}).setdefault(c_value, {}).setdefault(part, {})[p_value] = file_path

    # demihumans sho dwn glv top met
    # for file_hash in chara_cat_hash_table[human_search_folder_hash].keys():
    #     for letter in ['c', 'd', 'm']:
    #         value = get_rev_digits_values(get_hash(letter), '.atch', file_hash)
    #         if value:
    #             logging.info('Found: chara/xls/attachOffset/%s%s.atch' % (letter, value))

    # Search for .imc
    single_file_dirs = {}
    for dir_hash, dir_hash_table in chara_cat_hash_table.items():
        if len(dir_hash_table) == 1:
            for file_hash in dir_hash_table.keys():
                single_file_dirs[dir_hash] = [file_hash]

    file_matches = {}
    file_matches['b'] = get_rev_digits_values_matches('b', '.imc', single_file_dirs)
    file_matches['e'] = get_rev_digits_values_matches('e', '.imc', single_file_dirs)
    file_matches['a'] = get_rev_digits_values_matches('a', '.imc', single_file_dirs)

    # Monster/Weapon
    for cat_type in ['weapon', 'monster']:
        prefix_crc = crc_32(bytes('chara/%s/%s' % (cat_type, cat_type[0]), encoding='ascii'), 0xFFFFFFFF)
        for dir_hash, dir_hash_table in file_matches['b'].items():
            for file_hash, b_name in dir_hash_table.items():
                cat_name = get_rev_digits_values(prefix_crc, '/obj/body/b%s' % b_name, dir_hash)
                if cat_name:
                    file_path = 'chara/%s/%s%s/obj/body/b%s/model/%s%sb%s.mdl' % (cat_type, cat_type[0], cat_name, b_name, cat_type[0], cat_name, b_name)
                    if dat_manager.check_file_existence(file_path):
                        models_result_tree.setdefault(cat_type, {}).setdefault(cat_name, {})[b_name] = file_path

    # # Equipment/Accessory
    # for cat_type in ['equipment', 'accessory']:
    #     prefix_crc = crc_32(bytes('chara/%s/%s' % (cat_type, cat_type[0]), encoding='ascii'), 0xFFFFFFFF)
    #     for dir_hash, dir_hash_table in file_matches[cat_type[0]].items():
    #         for file_hash, b_name in dir_hash_table.items():
    #             values = get_rev_digits_values(prefix_crc, '', dir_hash)
    #             if values:
    #                 cat_name = ''.join(chr(c) for c in values)
    #                 file_path = 'chara/%s/%s%s/model/m%sb%s.mdl' % (cat_type, cat_type[0], cat_name, cat_name, b_name)
    #                 if dat_manager.check_file_existence(file_path):
    #                     models_result_tree.setdefault(cat_type, {}).setdefault(cat_name, {})[b_name] = file_path



        # for i in range(10000):
        #     i_value = '%0.4d' % i
        #     i_name = '%s%s' % (s[0], i_value)
        #     folder_path = 'chara/%s/%s/model/' % (s, i_name)
        #     if dat_manager.check_dir_existence(folder_path):
        #         for c in range(10000):
        #             c_value = '%0.4d' % c
        #             c_name = 'c%s' % c_value
        #             for s2 in ['ril', 'rir', 'wrs', 'nek', 'ear', 'sho', 'dwn', 'glv', 'top', 'met']:
        #                 file_path = '%s%s%s_%s.mdl' % (folder_path, c_name, i_name, s2)
        #                 if dat_manager.check_file_existence(file_path):
        #                     models_result_tree.setdefault(s, {}).setdefault(i_value, {}).setdefault(s2, {})[c_value] = file_path

    # for c in range(10000):
    #     c_value = '%0.4d' % c
    #     c_name = 'c%s' % c_value
    #     base_folder_path = 'chara/human/%s/obj/' % c_name
    #     for part, postfix in [('face', 'fac'), ('hair', 'hir'), ('tail', 'til'), ('body', 'top')]:
    #         for j in range(10000):
    #             p_value = '%0.4d' % j
    #             p_name = '%s%s' % (part[0], p_value)
    #             file_path = '%s%s/%s/model/%s%s_%s.mdl' % (base_folder_path, part, p_name, c_name, p_name, postfix)
    #             if dat_manager.check_file_existence(file_path):
    #                 models_result_tree.setdefault('human', {}).setdefault(c_value, {}).setdefault(part, {})[p_value] = file_path

    # for s in ['equipment', 'accessory']:
    #     for i in range(10000):
    #         i_value = '%0.4d' % i
    #         i_name = '%s%s' % (s[0], i_value)
    #         folder_path = 'chara/%s/%s/model/' % (s, i_name)
    #         if dat_manager.check_dir_existence(folder_path):
    #             for c in range(10000):
    #                 c_value = '%0.4d' % c
    #                 c_name = 'c%s' % c_value
    #                 for s2 in ['ril', 'rir', 'wrs', 'nek', 'ear', 'sho', 'dwn', 'glv', 'top', 'met']:
    #                     file_path = '%s%s%s_%s.mdl' % (folder_path, c_name, i_name, s2)
    #                     if dat_manager.check_file_existence(file_path):
    #                         models_result_tree.setdefault(s, {}).setdefault(i_value, {}).setdefault(s2, {})[c_value] = file_path

    # for d in range(10000):
    #     d_value = '%0.4d' % d
    #     d_name = 'd%s' % d_value
    #     for e in range(10000):
    #         e_value = '%0.4d' % e
    #         e_name = 'e%s' % e_value
    #         folder_path = 'chara/demihuman/%s/obj/equipment/%s/model/' % (d_name, e_name)
    #         if dat_manager.check_dir_existence(folder_path):
    #             for s in ['sho', 'dwn', 'glv', 'top', 'met']:
    #                 file_path = '%s%s%s_%s.mdl'% (folder_path, d_name, e_name, s)
    #                 if dat_manager.check_file_existence(file_path):
    #                     models_result_tree.setdefault('demihuman', {}).setdefault(d_value, {}).setdefault(e_value, {})[s] = file_path

    # for s in ['weapon', 'monster']:
    #     for i in range(10000):
    #         i_value = '%0.4d' % i
    #         i_name = '%s%s' % (s[0], i_value)
    #         for b in range(10000):
    #             b_value = '%0.4d' % b
    #             b_name = 'b%s' % b_value
    #             file_path = 'chara/%s/%s/obj/body/%s/model/%s%s.mdl' % (s, i_name, b_name, i_name, b_name)
    #             if dat_manager.check_file_existence(file_path):
    #                 models_result_tree.setdefault(s, {}).setdefault(i_value, {})[b_value] = file_path
    logging.info(models_result_tree)
    return models_result_tree