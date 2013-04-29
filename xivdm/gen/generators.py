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