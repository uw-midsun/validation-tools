import logging
import os
from datetime import datetime
from equipments.scale import Scale
from ms_logging.ms_logger_configurator import MsLoggerConfigurator
from scenarios.ac_internal_scenario import AcInternalScenario
from scenarios.weight_measurement_scenario import WeightMeasurementScenario

if __name__ == '__main__':
    directory = 'scale-' + datetime.now().strftime("%H-%M-%S")
    os.makedirs(directory)
    serial_number = '1234'
    MsLoggerConfigurator().configure_logging(log_level=logging.INFO)
    log = logging.getLogger("test")
    scale = Scale().calibrate()
    WeightMeasurementScenario(scale, serial_number).run(directory)





