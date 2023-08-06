import configparser
import importlib
import logging


class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        for line in self.linebuf.splitlines():
            self.logger.log(self.log_level, line.rstrip())


def get_cloud_handler(config_path='/etc/smartscheduler/config.cfg'):
    config = configparser.RawConfigParser()
    config.read(config_path)
    module = importlib.import_module(config.get('cloud', 'driver'))
    cloud_handler = module.init_handler(dict(config.items('cloud')))
    return cloud_handler


def get_monitoring_handler(config_path='/etc/smartscheduler/config.cfg'):
    config = configparser.ConfigParser()
    config.read(config_path)
    module = importlib.import_module(config.get('monitoring', 'driver'))
    dbms_handler = module.init_handler(dict(config.items('monitoring')))
    return dbms_handler


def init_logging(config_path='/etc/smartscheduler/config.cfg'):
    config = configparser.ConfigParser()
    config.read(config_path)
    logger = logging.getLogger(config.get('logging', 'name'))
    logger.setLevel(logging.getLevelName(config.get('logging', 'level')))
    handler = logging.FileHandler(config.get('logging', 'filename'))
    formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
