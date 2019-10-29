import logging
from ms_logging.ms_logger_configurator import MsLoggerConfigurator
from equipments.bk8600 import Bk8600

if __name__ == '__main__':
    MsLoggerConfigurator().configure_logging(log_level=logging.INFO)
    log = logging.getLogger("test")
    driver = Bk8600()
    driver.connect()
    driver.set_function(Bk8600.Functions.CONSTANT_CURRENT)
    steps = [{'level': d*0.1, 'width': 1} for d in range(1, 11)]
    driver.set_list(steps)
    driver.set_input(Bk8600.Input.ON)

