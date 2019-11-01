import logging

from ms_logging.ms_logger_configurator import MsLoggerConfigurator
from scenarios.ocv_test_scenario import OcvTestScenario

if __name__ == '__main__':
    MsLoggerConfigurator().configure_logging(log_level=logging.INFO)
    log = logging.getLogger("test")
    scenario = OcvTestScenario('123').run('hello')
