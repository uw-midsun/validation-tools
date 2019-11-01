import csv
import logging
from scenarios.b2902a_scenario import B2902AScenario


class B2902AListModeScenario(B2902AScenario):
    def __init__(self, serial_number):
        super().__init__()
        self.serial_number = serial_number

    def run_scenario(self, directory):
        return {}

    def run(self, directory):
        data = self.run_scenario(directory)
        self.write_to_csv(data, directory)

    def write_to_csv(self, data, directory):
        name = self.__class__.__name__
        file_name = "%s-%s" % (self.serial_number, name)
        path_to_file = "%s/%s.csv" % (directory, file_name)
        log.info('dumping results of %s to %s' % (name, path_to_file))
        with open(path_to_file, 'w', newline='') as csvfile:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for d in data:
                writer.writerow(d)


log = logging.getLogger("{}.{}".format(B2902AListModeScenario.__module__,
                                       B2902AListModeScenario.__name__, ))
