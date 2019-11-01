import logging
import os
import stat
from datetime import datetime


class Experiment(object):
    def __init__(self, recipes, name):
        self.recipes = recipes
        self.experiment_name = name

    def setup(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder_name = "{}_{}".format(self.experiment_name, timestamp)
        path = "./results/{}".format(folder_name)
        log.info("Creating folder: %s to store the results" % path)
        os.makedirs(path)
        return path

    def run(self):
        path = self.setup()
        while True:
            log.info("Please scan the barcode and hit enter:")
            log.info("If not, type 'exit'")
            cell_id = input()
            if cell_id == 'exit':
                break
            for recipe in self.recipes:
                scenario = recipe(cell_id)
                scenario.run(path)
        self.teardown(path)

    def teardown(self, path):
        for root, dirs, files in os.walk(path):
            permissions = stat.S_IROTH | stat.S_IRGRP | stat.S_IREAD
            for d in dirs:
                os.chmod(os.path.join(root, d), permissions)
            for f in files:
                os.chmod(os.path.join(root, f), permissions)


log = logging.getLogger("{}.{}".format(Experiment.__module__, Experiment.__name__))
