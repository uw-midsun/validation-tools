import logging

from ms_logging.ms_logger_configurator import MsLoggerConfigurator
from scenarios.dc_linear_sweep_scenario import DcLinearSweepScenario

if __name__ == '__main__':
    MsLoggerConfigurator().configure_logging(log_level=logging.INFO)
    log = logging.getLogger("test")
    scenario = DcLinearSweepScenario('123').run('hello')
