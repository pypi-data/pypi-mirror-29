from ScopusWp.config import PROJECT_PATH

from jutil.configuration import config_singleton

import os


PATH = os.path.dirname(os.path.realpath(__file__))

class WordpressConfig(config_singleton(
    PROJECT_PATH + '/wordpress',
)):
    pass