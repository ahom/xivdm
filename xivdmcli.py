# -*- coding: utf-8 -*-

import argparse
import logging
from pprint import pformat
import sys
from os import path, makedirs
from configparser import SafeConfigParser
import json

from xivdm.logging_utils import set_logging
from xivdm.crc32_utils import crc_32, rev_crc_32
from xivdm.language import get_language_name
from xivdm.dat.Manager import Manager as DatManager, get_hashes
from xivdm.exd.Manager import Manager as ExdManager
from xivdm.exd.Category import Category as ExdCategory
from xivdm.exd.links_analyzer import analyze_links
from xivdm.view.Manager import Manager as ViewManager
from xivdm.gen.Manager import Manager as GenManager
from xivdm.patch.Manager import Manager as PatchManager

def extract_all(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))

    output_path = path.join(conf.get('output', 'path'), 'all')

    for category_name in dat_manager.get_categories():
        category = dat_manager.get_category(category_name)

        output_cat_path = path.join(output_path, category_name)

        for dir_hash in category.get_hash_table().keys():
            output_dir_path = path.join(output_cat_path, '%0.8X' % dir_hash)

            if not path.exists(output_dir_path):
                makedirs(output_dir_path)

            for file_hash in category.get_dir_hash_table(dir_hash).keys():
                output_file_path = path.join(output_dir_path, '%0.8X' % file_hash)

                file_data = category.get_file(dir_hash, file_hash)

                with open(output_file_path, 'wb') as file_handle:
                    file_handle.write(file_data.getvalue())

def extract_category(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))

    category = dat_manager.get_category(args.name)
    output_path = path.join(conf.get('output', 'path'), 'cat', args.name)

    for dir_hash in category.get_hash_table().keys():
        output_dir_path = path.join(output_path, '%0.8X' % dir_hash)

        if not path.exists(output_dir_path):
            makedirs(output_dir_path)

        for file_hash in category.get_dir_hash_table(dir_hash).keys():
            output_file_path = path.join(output_dir_path, '%0.8X' % file_hash)

            file_data = category.get_file(dir_hash, file_hash)

            with open(output_file_path, 'wb') as file_handle:
                file_handle.write(file_data.getvalue())

def extract_folder(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))

    output_path = path.join(conf.get('output', 'path'), 'folder', args.name)
    category = dat_manager.get_category_from_filename(args.name)

    (dir_hash, _) = get_hashes(args.name)

    dir_hash_table = category.get_dir_hash_table(dir_hash)

    if not path.exists(output_path):
        makedirs(output_path)

    for file_hash in dir_hash_table.keys():
        output_file_path = path.join(output_path, '%0.8X' % file_hash)

        file_data = category.get_file(dir_hash, file_hash)

        with open(output_file_path, 'wb') as file_handle:
            file_handle.write(file_data.getvalue())

def extract_file(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))

    output_file_path = path.join(conf.get('output', 'path'), 'file', args.name)
    file_data = dat_manager.get_file(args.name)

    if not path.exists(path.dirname(output_file_path)):
        makedirs(path.dirname(output_file_path))

    with open(output_file_path, 'wb') as file_handle:
        file_handle.write(file_data.getvalue())

def extract_exd(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))
    exd_manager = ExdManager(dat_manager)

    output_path = path.join(conf.get('output', 'path'), 'csv')

    for category_name in exd_manager.get_categories():
        data = exd_manager.get_category(category_name).get_csv()
        for language, csv in data.items():
            output_file_path = path.join(
                output_path, 
                'exd/%s_%s.exd' % (category_name, get_language_name(language)))

            if not path.exists(path.dirname(output_file_path)):
                makedirs(path.dirname(output_file_path))

            with open(output_file_path, 'w') as file_handle:
                for line in csv:
                    file_handle.write(line)
                    file_handle.write('\n')

def extract_view(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))
    exd_manager = ExdManager(dat_manager)
    view_manager = ViewManager(exd_manager)

    output_path = path.join(conf.get('output', 'path'), 'json')

    for view_name in view_manager.get_mappings():
        output_file_path = path.join(output_path, '%s.json' % (view_name))

        if not path.exists(path.dirname(output_file_path)):
            makedirs(path.dirname(output_file_path))

        with open(output_file_path, 'w') as file_handle:
            file_handle.write(
                json.dumps(
                    view_manager.get_json(view_name), 
                    sort_keys=True, 
                    indent=4, 
                    separators=(',', ': ')))

def walk_gen(dat_manager, node, output_path):
    if type(node) == dict:
        for key, value in node.items():
            walk_gen(dat_manager, value, output_path)
    elif type(node) == list:
        for value in node:
            walk_gen(dat_manager, value, output_path)
    elif type(node) == str:
        output_file_path = path.join(output_path, node)
        if not path.exists(path.dirname(output_file_path)):
            makedirs(path.dirname(output_file_path))
        data = dat_manager.get_file(node)
        with open(output_file_path, 'wb') as file_handle:
            file_handle.write(data.getvalue())

def extract_gen(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))
    gen_manager = GenManager(dat_manager)
    output_path = path.join(conf.get('output', 'path'), 'gen', args.name)
    walk_gen(dat_manager, gen_manager.get_category(args.name), output_path)

def analyze_exd_links(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))
    exd_manager = ExdManager(dat_manager)
    results = analyze_links(exd_manager)
    logging.info(pformat(results))

def extract_music(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))
    exd_manager = ExdManager(dat_manager)
    output_path = path.join(conf.get('output', 'path'), 'music')

    for data in exd_manager.get_category('BGM').get_ln_data(0).values():
        file_path = data[0].decode('utf-8')

        if file_path == '':
            continue

        output_file_path = path.join(output_path, file_path)

        if not path.exists(path.dirname(output_file_path)):
            makedirs(path.dirname(output_file_path))

        try:
            file_data = dat_manager.get_file(file_path)
        except:
            continue

        with open(output_file_path, 'wb') as file_handle:
            file_handle.write(file_data.getvalue())

def crc_gen(args, conf):
    crc = crc_32(bytes(args.name, encoding='ascii'), 0xFFFFFFFF)
    print('crc_32: %0.8X' % crc)

def crc_rev(args, conf):
    start = bytes(args.start, encoding='ascii')
    end = bytes(args.end, encoding='ascii')

    crc0 = crc_32(start, 0xFFFFFFFF)
    crc1 = rev_crc_32(end, int(args.crc, 0))

    rev_crc = crc0 ^ crc1

    print('reverse: %0.8X - %s' % (rev_crc, [chr((rev_crc & (0xFF << (i * 8))) >> (i * 8)) for i in range(4)]))

def crc_find(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))

    cat = dat_manager.get_category('chara')

    hash_table = cat.get_hash_table()

    single_file_dirs = []
    for dir_hash, dir_hash_table in hash_table.items():
        if len(dir_hash_table) == 1:
            for file_hash in dir_hash_table.keys():
                single_file_dirs.append((dir_hash, file_hash))

    logging.info('Number of sinle_file_dirs: %d' % len(single_file_dirs))

    crc_list = []
    for c in map(chr, range(ord(b'a'), ord(b'z') + 1)):
        crc_list.append((crc_32(bytes(c, encoding='ascii'), 0xFFFFFFFF), c))

    imc = b'.imc'

    for dir_hash, dir_hash_table in hash_table.items():
        for file_hash in dir_hash_table.keys():
            logging.info('dir_hash: %0.8X - file_hash: %0.8X' % (dir_hash, file_hash))
            for (crc0, letter) in crc_list:
                crc1 = rev_crc_32(imc, file_hash)
                crc = crc0 ^ crc1

                match = True

                for i in range(4):
                    if not (0x30 <= ((crc & (0xFF << (i * 8))) >> (i * 8)) < 0x40):
                        match = False
                        break

                if match:
                    logging.info('name: %s' % ('%s%s.imc' % (letter, [chr((crc & (0xFF << (i * 8))) >> (i * 8)) for i in range(4)])))

    # for dir_hash, file_hash in single_file_dirs:
    #     logging.info('dir_hash: %0.8X - file_hash: %0.8X' % (dir_hash, file_hash))
    #     for (crc0, letter) in crc_list:
    #         crc1 = rev_crc_32(imc, file_hash)
    #         crc = crc0 ^ crc1

    #         match = True

    #         for i in range(4):
    #             if not (0x30 <= ((crc & (0xFF << (i * 8))) >> (i * 8)) < 0x40):
    #                 match = False
    #                 break

    #         if match:
    #             logging.info('name: %s' % ('%s%s.imc' % (letter, [chr((crc & (0xFF << (i * 8))) >> (i * 8)) for i in range(4)])))

    def check_dir_existence(self, dir_hash):
        return dir_hash in self._hash_table

    def check_file_existence(self, dir_hash, file_hash):
        return self.check_dir_existence(dir_hash) and file_hash in self.get_dir_hash_table(dir_hash)

    def get_file(self, dir_hash, file_hash):
        logging.info('%0.8X/%0.8X', dir_hash, file_hash)
        file_infos = self.get_dir_hash_table(dir_hash)[file_hash]
        logging.info('%s', file_infos)
        dat_file_handle = self._get_dat_file_handle(file_infos.dat_nb)
        return extract_file(dat_file_handle, file_infos.dat_offset)

    def get_hash_table(self):
        return self._hash_table

    def get_dir_hash_table(self, dir_hash):
        return self._hash_table[dir_hash]


def patch_version(args, conf):
    patch_manager = PatchManager(conf.get('game', 'path'))

    for patchable_name in patch_manager.get_patchables():
        print('%s: %s' % (patchable_name, patch_manager.get_patchable(patchable_name).get_version()))

def patch_check(args, conf):
    patch_manager = PatchManager(path.join(conf.get('game', 'path'), '../ffxiv_data_test'))
    print('%s: %s' % ('boot', patch_manager.get_patchable('boot').check()))

def patch_update(args, conf):
    patch_manager = PatchManager(path.join(conf.get('game', 'path'), '../ffxiv_data_test'))
    patch_manager.get_patchable('boot').update()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='xivdm command line interface')
    subparsers = parser.add_subparsers(title='sub modules')

    ######################
    # Extract sub module #
    ######################
    extract_parser = subparsers.add_parser('extract', help='extract files')
    extract_subparsers = extract_parser.add_subparsers(title='type')

    # Extract all
    extract_all_parser = extract_subparsers.add_parser('all', help='extract all files')
    extract_all_parser.set_defaults(callback=extract_all)

    # Extract category
    extract_category_parser = extract_subparsers.add_parser('category', help='extract all files for category')
    extract_category_parser.add_argument('-n', '--name', required=True)
    extract_category_parser.set_defaults(callback=extract_category)

    # Extract folder
    extract_folder_parser = extract_subparsers.add_parser('folder', help='extract all files for folder')
    extract_folder_parser.add_argument('-n', '--name', required=True)
    extract_folder_parser.set_defaults(callback=extract_folder)

    # Extract file
    extract_file_parser = extract_subparsers.add_parser('file', help='extract a single file')
    extract_file_parser.add_argument('-n', '--name', required=True)
    extract_file_parser.set_defaults(callback=extract_file)

    # Extract exd
    extract_exd_parser = extract_subparsers.add_parser('exd', help='extract exd files as csv')
    extract_exd_parser.set_defaults(callback=extract_exd)

    # Extract view
    extract_view_parser = extract_subparsers.add_parser('view', help='extract view files as json')
    extract_view_parser.set_defaults(callback=extract_view)

    # Extract music
    extract_music_parser = extract_subparsers.add_parser('music', help='extract music files')
    extract_music_parser.set_defaults(callback=extract_music)

    # Extract gen
    extract_gen_parser = extract_subparsers.add_parser('gen', help='extract gen files')
    extract_gen_parser.add_argument('-n', '--name', required=True)
    extract_gen_parser.set_defaults(callback=extract_gen)

    ######################
    # Analyze sub module #
    ######################
    analyze_parser = subparsers.add_parser('analyze', help='analyze stuff')
    analyze_subparsers = analyze_parser.add_subparsers(title='type')

    # Analyze exd_links category
    analyze_exd_links_parser = analyze_subparsers.add_parser('exd_links', help='analyze exd_links')
    analyze_exd_links_parser.set_defaults(callback=analyze_exd_links)


    ######################
    # Crc sub module   #
    ######################
    crc_parser = subparsers.add_parser('crc', help='crc utils')
    crc_subparsers = crc_parser.add_subparsers(title='type')

    # Generate crc
    crc_gen_parser = crc_subparsers.add_parser('gen', help='generate crc32 of string')
    crc_gen_parser.add_argument('-n', '--name', required=True)
    crc_gen_parser.set_defaults(callback=crc_gen)

    # Reverse crc
    crc_rev_parser = crc_subparsers.add_parser('rev', help='reverse crc32 of string')
    crc_rev_parser.add_argument('-c', '--crc', required=True)
    crc_rev_parser.add_argument('-s', '--start', required=True)
    crc_rev_parser.add_argument('-e', '--end', required=True)
    crc_rev_parser.set_defaults(callback=crc_rev)

    # Find files crc
    crc_find_parser = crc_subparsers.add_parser('find', help='find models.imc')
    crc_find_parser.set_defaults(callback=crc_find)

    ######################
    # Patch sub module   #
    ######################
    patch_parser = subparsers.add_parser('patch', help='handle patch')
    patch_subparsers = patch_parser.add_subparsers(title='type')

    # Patch version
    patch_version_parser = patch_subparsers.add_parser('version', help='displays versions of patchables')
    patch_version_parser.set_defaults(callback=patch_version)

    # Patch check
    patch_check_parser = patch_subparsers.add_parser('check', help='displays checks of patchables')
    patch_check_parser.set_defaults(callback=patch_check)

    # Patch check
    patch_update_parser = patch_subparsers.add_parser('update', help='updates of patchables')
    patch_update_parser.set_defaults(callback=patch_update)

    args = parser.parse_args()

    config = SafeConfigParser()
    config.readfp(open('config.cfg'))

    set_logging(config.get('logs', 'path'), 'xivdmcli')

    logging.info('Executing command: ' + str(sys.argv))

    if not hasattr(args, 'callback'):
        logging.error('Command-line parsing error.')
        parser.print_help()
    else:
        args.callback(args, config)
