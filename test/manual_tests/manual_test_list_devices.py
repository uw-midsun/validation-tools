import logging
from equipments.b2902A import B2902A
from ms_logging.ms_logger_configurator import MsLoggerConfigurator

if __name__ == '__main__':
    MsLoggerConfigurator().configure_logging(log_level=logging.INFO)
    log = logging.getLogger("test")
    log.info(B2902A().list_all_resources())
