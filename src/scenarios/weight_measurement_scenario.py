import csv
from datetime import datetime
import logging
from time import sleep


class WeightMeasurementScenario(object):
    SAMPLING_INTERVAL_S = 0.02

    def __init__(self, scale, serial_number):
        self.scale = scale
        self.serial_number = serial_number
        self.file_path = None
        self.field_names = ['time', 'weight(g)']

    def start(self, directory):
        file_name = "weight-%s.csv" % self.serial_number
        file_path = "%s/%s" % (directory, file_name)
        self.file_path = file_path
        log.info("Taking weight measurements:")
        log.info("%s" % file_path)
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.field_names)
            writer.writeheader()
        return self

    def take_measurement(self):
        with open(self.file_path, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.field_names)
            weight = self.scale.measure_weight()
            datum = {
                self.field_names[0]: datetime.now().strftime("%H-%M-%S"),
                self.field_names[1]: weight
            }
            writer.writerow(datum)
            sleep(self.SAMPLING_INTERVAL_S)


log = logging.getLogger("{}.{}".format(WeightMeasurementScenario.__module__,
                                       WeightMeasurementScenario.__name__, ))


