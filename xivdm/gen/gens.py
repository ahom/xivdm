import logging

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

def models(dat_manager):
    models_result_tree = {}
    for c in range(10000):
        c_value = '%0.4d' % c
        c_name = 'c%s' % c_value
        base_folder_path = 'chara/human/%s/obj/' % c_name
        for part, postfix in [('face', 'fac'), ('hair', 'hir'), ('tail', 'til'), ('body', 'top')]:
            for j in range(10000):
                p_value = '%0.4d' % j
                p_name = '%s%s' % (part[0], p_value)
                file_path = '%s%s/%s/model/%s%s_%s.mdl' % (base_folder_path, part, p_name, c_name, p_name, postfix)
                if dat_manager.check_file_existence(file_path):
                    models_result_tree.setdefault('human', {}).setdefault(c_value, {}).setdefault(part, {})[p_value] = file_path

    for s in ['equipment', 'accessory']:
        for i in range(10000):
            i_value = '%0.4d' % i
            i_name = '%s%s' % (s[0], i_value)
            folder_path = 'chara/%s/%s/model/' % (s, i_name)
            if dat_manager.check_dir_existence(folder_path):
                for c in range(10000):
                    c_value = '%0.4d' % c
                    c_name = 'c%s' % c_value
                    for s2 in ['ril', 'rir', 'wrs', 'nek', 'ear', 'sho', 'dwn', 'glv', 'top', 'met']:
                        file_path = '%s%s%s_%s.mdl' % (folder_path, c_name, i_name, s2)
                        if dat_manager.check_file_existence(file_path):
                            models_result_tree.setdefault(s, {}).setdefault(i_value, {}).setdefault(s2, {})[c_value] = file_path

    for d in range(10000):
        d_value = '%0.4d' % d
        d_name = 'd%s' % d_value
        for e in range(10000):
            e_value = '%0.4d' % e
            e_name = 'e%s' % e_value
            folder_path = 'chara/demihuman/%s/obj/equipment/%s/model/' % (d_name, e_name)
            if dat_manager.check_dir_existence(folder_path):
                for s in ['sho', 'dwn', 'glv', 'top', 'met']:
                    file_path = '%s%s%s_%s.mdl'% (folder_path, d_name, e_name, s)
                    if dat_manager.check_file_existence(file_path):
                        models_result_tree.setdefault('demihuman', {}).setdefault(d_value, {}).setdefault(e_value, {})[s] = file_path

    for s in ['weapon', 'monster']:
        for i in range(10000):
            i_value = '%0.4d' % i
            i_name = '%s%s' % (s[0], i_value)
            for b in range(10000):
                b_value = '%0.4d' % b
                b_name = 'b%s' % b_value
                file_path = 'chara/%s/%s/obj/body/%s/model/%s%s.mdl' % (s, i_name, b_name, i_name, b_name)
                if dat_manager.check_file_existence(file_path):
                    models_result_tree.setdefault(s, {}).setdefault(i_value, {})[b_value] = file_path
    return models_result_tree