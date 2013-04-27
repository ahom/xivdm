# -*- coding: utf-8 -*-

import argparse
import logging
import sys
from os import path, makedirs
from configparser import SafeConfigParser
import json

from xivdm.logging_utils import set_logging
from xivdm.language import get_language_name
from xivdm.dat.Manager import Manager as DatManager
from xivdm.exd.Manager import Manager as ExdManager
from xivdm.exd.Category import Category as ExdCategory
from xivdm.view.Manager import Manager as ViewManager
from xivdm.patch.Manager import Manager as PatchManager

def extract_category(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))

    category = dat_manager.get_category('exd')

    for file_hash in category.get_dir_hash_table(0xE39B7999).keys():

        file_path = path.join(conf.get('output', 'path'), '%0.8X' % 0xE39B7999, '%0.8X' % file_hash)

        if not path.exists(path.dirname(file_path)):
            makedirs(path.dirname(file_path))

        file_data = category.get_file(0xE39B7999, file_hash)

        with open(file_path, 'wb') as file_handle:
            file_handle.write(file_data.getvalue())

def extract_file(args, conf):
    file_path = path.join(conf.get('output', 'path'), args.name)

    if not path.exists(path.dirname(file_path)):
        makedirs(path.dirname(file_path))

    dat_manager = DatManager(conf.get('game', 'path'))
    file_data = dat_manager.get_file(args.name)

    with open(file_path, 'wb') as file_handle:
        file_handle.write(file_data.getvalue())

def extract_exd(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))
    exd_manager = ExdManager(dat_manager)

    for category_name in exd_manager.get_categories():
        data = exd_manager.get_category(category_name).get_csv()
        for language, csv in data.items():
            file_path = path.join(
                conf.get('output', 'path'), 
                'exd/%s%s.exd' % (category_name, get_language_name(language)))

            if not path.exists(path.dirname(file_path)):
                makedirs(path.dirname(file_path))

            with open(file_path, 'w') as file_handle:
                for line in csv:
                    file_handle.write(line)
                    file_handle.write('\n')

def extract_view(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))
    exd_manager = ExdManager(dat_manager)
    view_manager = ViewManager(exd_manager)

    for view_name in view_manager.get_mappings():
        file_path = path.join(conf.get('output', 'path'), '%s.json' % (view_name))

        if not path.exists(path.dirname(file_path)):
            makedirs(path.dirname(file_path))

        with open(file_path, 'w') as file_handle:
            file_handle.write(
                json.dumps(
                    view_manager.get_json(view_name), 
                    sort_keys=True, 
                    indent=4, 
                    separators=(',', ': ')))

def extract_icon(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))
    
    for i in range(1000):
        folder = i * 1000
        folder_path = 'ui/icon/%0.6d/' % folder
        if dat_manager.check_dir_existence(folder_path):
            for j in range(1000):
                icon = folder + j
                icon_path = '%s%0.6d.dds' % (folder_path, icon)
                if dat_manager.check_file_existence(icon_path):
                    output_path = path.join(conf.get('output', 'path'), icon_path)

                    if not path.exists(path.dirname(output_path)):
                        makedirs(path.dirname(output_path))

                    with open(output_path, 'wb') as file_handle:
                        file_handle.write(dat_manager.get_file(icon_path).getvalue())

def extract_map(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))
    for a in map(chr, range(ord('a'), ord('z') + 1)):
        for i in range(10):
            for b in map(chr, range(ord('a'), ord('z') + 1)):
                for j in range(10):
                    for k in range(100):
                        basename = '%s%d%s%d' % (a, i, b, j)
                        num = '%0.2d' % k
                        folder_path = 'ui/map/%s/%s/' % (basename, num)
                        if dat_manager.check_dir_existence(folder_path):
                            background_path = '%s%s%sm.dds' % (folder_path, basename, num)
                            if dat_manager.check_file_existence(background_path):
                                output_path = path.join(conf.get('output', 'path'), background_path)

                                if not path.exists(path.dirname(output_path)):
                                    makedirs(path.dirname(output_path))

                                with open(output_path, 'wb') as file_handle:
                                    file_handle.write(dat_manager.get_file(background_path).getvalue())

                            for x in range(16):
                                for y in range(16):
                                    tile_path = '%s%s%s_%d_%d.dds' % (folder_path, basename, num, x, y)

                                    if dat_manager.check_file_existence(tile_path):
                                        output_path = path.join(conf.get('output', 'path'), tile_path)

                                        if not path.exists(path.dirname(output_path)):
                                            makedirs(path.dirname(output_path))

                                        with open(output_path, 'wb') as file_handle:
                                            file_handle.write(dat_manager.get_file(tile_path).getvalue())


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

    # Extract category
    extract_category_parser = extract_subparsers.add_parser('category', help='extract all files for category')
    extract_category_parser.add_argument('-n', '--name', required=True)
    extract_category_parser.set_defaults(callback=extract_category)

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

    # Extract icon
    extract_icon_parser = extract_subparsers.add_parser('icon', help='extract icon files')
    extract_icon_parser.set_defaults(callback=extract_icon)

    # Extract map
    extract_map_parser = extract_subparsers.add_parser('map', help='extract map files')
    extract_map_parser.set_defaults(callback=extract_map)

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
