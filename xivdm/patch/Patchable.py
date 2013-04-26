import http.client
from collections import namedtuple
from os import path, makedirs
from io import StringIO

CHECK_RES = namedtuple('check_response', ['is_uptodate', 'response'])

def do_http_request(host, method, uri, data=None, headers={}, is_https=False):
    conn = None
    if is_https:
        conn = http.client.HTTPSConnection(host, 443)
    else:
        conn = http.client.HTTPConnection(host, 80)
    conn.set_debuglevel(1)
    conn.request(method,
                 uri,
                 data,
                 headers)
    response = conn.getresponse()
    body = response.read()
    return response, body

class Patchable:
    def __init__(self, game_path, patchable_name):
        self._base_path = path.join(game_path, patchable_name)
        self._name = patchable_name
        self._patch_path = path.join(self._base_path, 'patch')

        vercheck_path = path.join(self._base_path, 'ffxiv%s.ver' % patchable_name)

        if not path.exists(path.dirname(vercheck_path)):
            makedirs(path.dirname(vercheck_path))

        if not path.exists(vercheck_path):
            with open(vercheck_path, 'w') as file_handle:
                file_handle.write('2012.01.01.0000.0000')

        with open(path.join(self._base_path, 'ffxiv%s.ver' % patchable_name), 'r') as file_handle:
            self._version = file_handle.read()

    def get_name(self):
        return self._name

    def get_version(self):
        return self._version

    def check(self):
        pass

    def download(self, file_infos):
        pass

    def apply(self):
        pass

    def update(self):
        pass

class Boot(Patchable):
    def __init__(self, game_path, patchable_name):
        Patchable.__init__(self, game_path, patchable_name)

    def check(self):
        response, body = do_http_request('patch-bootver.ffxiv.com', 'GET', '/http/win32/ffxivneob1_release_boot/%s' % self.get_version(),
                                         headers={
                                            'User-Agent': 'FFXIV PATCH CLIENT',
                                            'Connection': 'Keep-Alive'
                                         })
        return CHECK_RES._make((response.status==204, body))

    def update(self):
        check_res = self.check()
        if not check_res.is_uptodate:
            string_io = StringIO(check_res.response.decode('ascii'))

            patches = list()

            line = string_io.readline()
            while line:
                if line == '\r\n':
                    line = string_io.readline()
                    while line:
                        if line.startswith('--'):
                            break
                        patches.append(line[:-2].split('\t'))
                        line = string_io.readline()
                else:
                    line = string_io.readline()

            for patch in patches:
                self.download(patch)

    def download(self, file_infos):
        patch_path = path.join(self._patch_path, 'D%s.patch' % file_infos[4])

        if not path.exists(path.dirname(patch_path)):
            makedirs(path.dirname(patch_path))

        uri_part = file_infos[5].split('/')
        response, body = do_http_request(uri_part[2], 'GET', '/%s' % '/'.join(uri_part[3:]),
                                         headers={
                                            'User-Agent': 'FFXIV PATCH CLIENT',
                                            'Connection': 'Keep-Alive'
                                         })

        with open(patch_path, 'wb') as file_handle:
            file_handle.write(body)



