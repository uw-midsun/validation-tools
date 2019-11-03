import logging
import os
import signal
import stat
from datetime import datetime
from equipments.b2902A import B2902A
from equipments.scale import Scale
from scenarios.dummy_scenario import DummyScenario
from scenarios.weight_measurement_scenario import WeightMeasurementScenario
import sys
import threading
from queue import Queue


class Experiment(object):
    RECALIBRATION_COUNTER = 100

    def __init__(self, recipes, name):
        self.recipes = recipes
        self.experiment_name = name
        self.scale = Scale()
        self.keyboard_queue = Queue()
        self.input_thread = None
        self.results_directory = None

    def add_input(self, input_queue):
        while True:
            input_queue.put(sys.stdin.read(1))

    def signal_handler(self, sig, frame):
        log.info('Exitting.')
        self.teardown()
        sys.exit(0)

    def setup(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder_name = "{}_{}".format(self.experiment_name, timestamp)
        path = "./results/{}".format(folder_name)
        self.results_directory = path
        self.input_thread = threading.Thread(target=self.add_input, args=(self.keyboard_queue,))
        self.input_thread.daemon = True
        self.input_thread.start()
        log.info("Creating folder: %s to store the results" % path)
        os.makedirs(path)
        signal.signal(signal.SIGINT, self.signal_handler)
        return path

    def run(self):
        path = self.setup()
        self.scale.calibrate()
        counter = 0
        last_battery_id = "calibration_weight"
        while True:
            if counter > self.RECALIBRATION_COUNTER:
                counter = 0
                self.scale.calibrate()
            counter += 1
            log.info("Please put the current battery on the scale, "
                     "put the new battery in the fixture, and scan its barcode:")
            weight_scenario = WeightMeasurementScenario(self.scale, last_battery_id).start(path)
            while True:
                weight_scenario.take_measurement()
                if not self.keyboard_queue.empty():
                    cell_id = ''
                    while not self.keyboard_queue.empty():
                        cell_id += self.keyboard_queue.get()
                    cell_id = cell_id[:-1]
                    if not cell_id:
                        log.info("Please scan again:")
                        continue
                    break
            if cell_id == 'exit':
                break
            last_battery_id = cell_id
            while not self.battery_inserted_correctly():
                log.info("Negative Voltage Read: Please make sure you've inserted the battery correctly. "
                         "Hit enter when done.")
                while self.keyboard_queue.empty():
                    pass
                while not self.keyboard_queue.empty():
                    self.keyboard_queue.get()
            for recipe in self.recipes:
                scenario = recipe(cell_id)
                scenario.run(path)
        self.teardown()

    def battery_inserted_correctly(self):
        return B2902A().connect().get_voltage() > 0

    def teardown(self):
        path = self.results_directory
        for root, dirs, files in os.walk(path):
            permissions = stat.S_IROTH | stat.S_IRGRP | stat.S_IREAD
            for d in dirs:
                os.chmod(os.path.join(root, d), permissions)
            for f in files:
                os.chmod(os.path.join(root, f), permissions)


log = logging.getLogger("{}.{}".format(Experiment.__module__, Experiment.__name__))
