import logging


class DataSource:

    def __init__(self, controller):
        self.controller = controller
        self.logger = logging.getLogger('source-{}'.format(self.name))

    def fetch(self):
        raise NotImplementedError()

    @property
    def name(self):
        raise NotImplementedError()


class DataSink:

    def __init__(self, controller):
        self.controller = controller
        self.logger = logging.getLogger('sink-{}'.format(self.name))

    @property
    def run(self):
        raise NotImplementedError()

    @property
    def register(self):
        return self.controller.register

    @property
    def config(self):
        return self.controller.config

    @property
    def name(self):
        raise NotImplementedError()
