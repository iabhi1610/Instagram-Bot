import configparser
import time
import functools
import logging


def init_config(config_file_path):
    path = config_file_path.split('.')

    assert(path[len(path)-1] == 'ini')

    config = configparser.ConfigParser()
    config.read(config_file_path)
    return config


def get_logger(logger_file_path):
    logger = logging.getLogger('InstaBotLogger')
    logger.setLevel(logging.DEBUG)

    file_handeler = logging.FileHandler(logger_file_path)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %l(levelname)s - %(message)s')
    file_handeler.setFormatter(formatter)

    logger.addHandler(file_handeler)
    return logger


def exception(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except:
            message = "Exception in method {}".format(func.__name__)
            logger = get_logger('bot.log')
            logger.exception(message)

    return wrapper


def insta_method(func):
    def wrapper(*args, **kwargs):
        time.sleep(2)
        func(*args, **kwargs)
        return wrapper
