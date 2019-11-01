import logging

from ms_logging.ms_logger_configurator import MsLoggerConfigurator
from scenarios.ac_internal_scenario import AcInternalScenario

if __name__ == '__main__':
    MsLoggerConfigurator().configure_logging(log_level=logging.INFO)
    log = logging.getLogger("test")
    scenario = AcInternalScenario('123')
    path = '.'
    log.info('running this bish')
    data = scenario.run(path)
    log.info(len(data))
    log.info('exiting')

