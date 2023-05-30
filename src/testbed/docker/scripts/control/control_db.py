#!/usr/bin/env python3


import argparse

from database.db_connection import InfluxDBConnection


CONFIG_FILE = './config.ini'


config = {
    'action': None,
    'testbed_name': None
}


def setup_from_cmdline():

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-a', '--action', type=str)
    parser.add_argument('-t', '--testbed', type=str)

    args = parser.parse_args()

    config['action'] = args.action
    config['testbed_name'] = args.testbed


def main():
    
    setup_from_cmdline()

    database = InfluxDBConnection(configFile=CONFIG_FILE)

    if config['action'] != 'start' and config['action'] != 'stop':
        return

    database.insert(
        bucket=config['testbed_name'],
        measurement='general',
        fields={'status': config['action']}
    )

    database.close()


main()
