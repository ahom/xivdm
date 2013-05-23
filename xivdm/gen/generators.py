import logging

def icons(dat_manager):
    def folders():
        for i in range(1000):
            folder = i * 1000
            folder_path = 'ui/icon/%0.6d/' % folder
            def files():
                for j in range(1000):
                    yield '%s%0.6d.dds' % (folder_path, folder + j)
            yield folder_path, files

            for ln in ['en', 'fr', 'de', 'ja']:
                ln_folder_path = '%s%s/' % (folder_path, ln)
                def files():
                    for j in range(1000):
                        yield '%s%0.6d.dds' % (ln_folder_path, folder + j)
                yield ln_folder_path, files
    return folders

def maps(dat_manager):
    def folders():
        for a in map(chr, range(ord('a'), ord('z') + 1)):
            for i in range(10):
                for b in map(chr, range(ord('a'), ord('z') + 1)):
                    for j in range(10):
                        for k in range(100):
                            basename = '%s%d%s%d' % (a, i, b, j)
                            num = '%0.2d' % k
                            folder_path = 'ui/map/%s/%s/' % (basename, num)
                            def files():
                                yield '%s%s%sm.dds' % (folder_path, basename, num)
                                for x in range(16):
                                    for y in range(16):
                                        yield '%s%s%s_%d_%d.dds' % (folder_path, basename, num, x, y)
                            yield folder_path, files
    return folders

def get_mod_range():
    for i in range(100):
        for j in range(10):
            yield i*10 + j

def models(dat_manager):
    def folders():
        # humans
        for c in range(10000):
            c_name = 'c%0.4d' % c
            base_folder_path = 'chara/human/%s/obj/' % c_name
            if dat_manager.check_dir_existence('%sbody/b0001/model/' % base_folder_path):
                for part, postfix in [('face', 'fac'), ('hair', 'hir'), ('tail', 'til'), ('body', 'top')]:
                    for j in range(10000):
                        p_name = '%s%0.4d' % (part[0], j)
                        folder_path = '%s%s/%s/model/' % (base_folder_path, part, p_name)
                        def files():
                            yield '%s%s%s_%s.mdl' % (folder_path, c_name, p_name, postfix)
                        yield folder_path, files

        # for i in range(10000):
        #     if i%100 == 0:
        #         logging.debug('Equipment/Accessory: %0.2d/100', i//100)
        #     for s in ['equipment', 'accessory']:
        #         folder_path = 'chara/%s/%s%0.4d/model/' % (s, s[0], i)
        #         def files():
        #             for j in range(10000):
        #                 for s2 in ['ril', 'rir', 'wrs', 'nek', 'ear', 'sho', 'dwn', 'glv', 'top', 'met']:
        #                     yield '%sc%0.4d%s%0.4d_%s.mdl' % (folder_path, j, s[0], i, s2)
        #         yield folder_path, files   

        # for i in range(10000):
        #     if i%100 == 0:
        #         logging.debug('Demihuman: %0.2d/100', i//100)
        #     for j in range(10000):
        #         folder_path = 'chara/demihuman/d%0.4d/obj/equipment/e%0.4d/model/' % (i, j)
        #         def files():
        #             for s in ['sho', 'dwn', 'glv', 'top', 'met']:
        #                 yield '%sd%0.4de%0.4d_%s.mdl' % (folder_path, i, j, s)
        #         yield folder_path, files   

        # for i in range(10000):
        #     if i%100 == 0:
        #         logging.debug('Weapon/Monster: %0.2d/100', i//100)
        #     for j in range(10000):
        #         for s in ['weapon', 'monster']:
        #             folder_path = 'chara/%s/%s%04d/obj/body/b%04d/model/' % (s, s[0], i, j)
        #             def files():
        #                 yield '%s%s%0.4db%0.4d.mdl' % (folder_path, s[0], i, j)
        #         yield folder_path, files   
    return folders