import yaml, logging


class Settings:
    def __init__(self, yaml_file=None, yaml_block=None):
        self.logger = logging.getLogger(__name__)
        self.username = None
        self.email = None
        self.password = None
        self.profile = None
        if yaml_block and yaml_file:
            raise AttributeError('Expecting yaml file or block, not both.')
        if yaml_block:
            self.from_yaml_block(yaml_block)
        if yaml_file:
            self.from_yaml_file(yaml_file)

    def from_yaml_block(self, block):
        self.logger.debug('Parsing yaml')
        content = yaml.safe_load(block)
        self.logger.debug('Parsing username')
        self.username = content['username']
        self.logger.debug('Parsing email')
        self.email = content['email']
        self.logger.debug('Parsing password')
        self.password = content['password']
        self.logger.debug('Parsing profile')
        self.profile = content['profile']

    def from_yaml_file(self, file):
        try:
            self.logger.debug('Opening yaml file')
            with open(file, 'r') as content:
                self.from_yaml_block(content.read())
        except Exception:
            self.logger.exception('Failed to open yaml file')
