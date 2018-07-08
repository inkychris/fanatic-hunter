import logging.config, yaml

logger = logging.getLogger('test')

with open('logging_config.yml', 'r') as yml:
    logging.config.dictConfig(yaml.safe_load(yml))

try:
    raise AttributeError('Something went wrong :(')
except AttributeError:
    logger.exception("Tried to do something but it didn't work")
