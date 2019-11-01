import logging

from ms_logging.ms_logger_configurator import MsLoggerConfigurator
from scenarios.dc_constant_current_pulse_scenario import DcConstantCurrentPulseScenario
from scenarios.dc_current_pulse_scenario import DcCurrentPulseScenario

if __name__ == '__main__':
    MsLoggerConfigurator().configure_logging(log_level=logging.INFO)
    log = logging.getLogger("test")
    scenario = DcConstantCurrentPulseScenario('123').run('hello')
