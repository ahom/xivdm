import logging

def icons():
    def folders():
        for i in range(1000):
            folder = i * 1000
            folder_path = 'ui/icon/%0.6d/' % folder
            def files():
                for j in range(1000):
                    yield '%s%0.6d.dds' % (folder_path, folder + j)
            yield folder_path, files
    return folders

def maps():
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
                                for x in range(16):
                                    for y in range(16):
                                        yield '%s%s%s_%d_%d.dds' % (folder_path, basename, num, x, y)
                            yield folder_path, files
    return folders

def models():
    def folders():
        for i in range(10000):
            if i%100 == 0:
                logging.debug('Human: %0.2d/100', i//100)
            base_folder_path = 'chara/human/c%0.4d/obj/' % i
            for j in range(10000):
                for s in [('face', 'fac'), ('hair', 'hir'), ('tail', 'til'), ('body', 'top')]:
                    folder_path = '%s%s/%s%0.4d/model/' % (base_folder_path, s[0], s[0][0], j)
                    def files():
                        yield '%sc%0.4d%s%0.4d_%s.mdl' % (folder_path, i, s[0][0], j, s[1])
                    yield folder_path, files

        for i in range(10000):
            if i%100 == 0:
                logging.debug('Equipment/Accessory: %0.2d/100', i//100)
            for s in ['equipment', 'accessory']:
                folder_path = 'chara/%s/%s%0.4d/model/' % (s, s[0], i)
                def files():
                    for j in range(10000):
                        for s2 in ['ril', 'rir', 'wrs', 'nek', 'ear', 'sho', 'dwn', 'glv', 'top', 'met']:
                            yield '%sc%0.4d%s%0.4d_%s.mdl' % (folder_path, j, s[0], i, s2)
                yield folder_path, files   

        for i in range(10000):
            if i%100 == 0:
                logging.debug('Demihuman: %0.2d/100', i//100)
            for j in range(10000):
                folder_path = 'chara/demihuman/d%0.4d/obj/equipment/e%0.4d/model/' % (i, j)
                def files():
                    for s in ['sho', 'dwn', 'glv', 'top', 'met']:
                        yield '%sd%0.4de%0.4d_%s.mdl' % (folder_path, i, j, s)
                yield folder_path, files   

        for i in range(10000):
            if i%100 == 0:
                logging.debug('Weapon/Monster: %0.2d/100', i//100)
            for j in range(10000):
                for s in ['weapon', 'monster']:
                    folder_path = 'chara/%s/%s%04d/obj/body/b%04d/model/' % (s, s[0], i, j)
                    def files():
                        yield '%s%s%0.4db%0.4d.mdl' % (folder_path, s[0], i, j)
                yield folder_path, files   
    return folders