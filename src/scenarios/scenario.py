import logging


class Scenario(object):
    def __init__(self):
        self.name = None

    def run(self, directory):
        log.info("Running: %s" % self.name)


log = logging.getLogger("{}.{}".format(Scenario.__module__, Scenario.__name__))
