import logging

from ms_logging.ms_logger_configurator import MsLoggerConfigurator
from scenarios.ten_seconds_discharge import TenSecondsDischargeScenario

if __name__ == '__main__':
    MsLoggerConfigurator().configure_logging(log_level=logging.INFO)
    log = logging.getLogger("test")
    scenario = TenSecondsDischargeScenario('123').run('hello')
