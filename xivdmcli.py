# -*- coding: utf-8 -*-

import argparse
import logging
import sys
from os import path, makedirs
from configparser import SafeConfigParser

from xivdm.logging_utils import set_logging
from xivdm.dat.Manager import Manager as DatManager
from xivdm.exd.Manager import Manager as ExdManager
from xivdm.exd.Category import Category as ExdCategory

def extract_file(args, conf):
    file_path = path.join(conf.get('output', 'path'), args.name)

    if not path.exists(path.dirname(file_path)):
        makedirs(path.dirname(file_path))

    dat_manager = DatManager(conf.get('game', 'path'))
    file_data = dat_manager.get_file(args.name)

    open(file_path, 'wb').write(file_data.getvalue())

def extract_exd(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))
    exd_manager = ExdManager(dat_manager)

    for category_name in exd_manager.get_categories():
        data = exd_manager.get_category(category_name).get_csv()
        for language, csv in data.items():
            file_path = path.join(conf.get('output', 'path'), 'exd/%s%s.exd' % (category_name, ExdCategory.LANGUAGE_SUFFIX[language]))

            if not path.exists(path.dirname(file_path)):
                makedirs(path.dirname(file_path))

            with open(file_path, 'w') as file_handle:
                for line in csv:
                    file_handle.write(line)
                    file_handle.write('\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='xivdm command line interface')
    subparsers = parser.add_subparsers(title='sub modules')

    ######################
    # Extract sub module #
    ######################
    extract_parser = subparsers.add_parser('extract', help='extract files')
    extract_subparsers = extract_parser.add_subparsers(title='type')

    # Extract file
    extract_file_parser = extract_subparsers.add_parser('file', help='extract a single file')
    extract_file_parser.add_argument('-n', '--name', required=True)
    extract_file_parser.set_defaults(callback=extract_file)

    # Extract exd
    extract_exd_parser = extract_subparsers.add_parser('exd', help='extract a exd files as csv')
    extract_exd_parser.set_defaults(callback=extract_exd)

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
