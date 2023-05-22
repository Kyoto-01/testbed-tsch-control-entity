from configparser import ConfigParser


def configure_from_file(file: 'str'):
    config = {}

    conf = ConfigParser()

    conf.read(file)
    
    config['addr'] = conf['broker']['addr']
    config['port'] = conf['broker']['port']
    config['queue'] = conf['broker']['queue']

    return config
