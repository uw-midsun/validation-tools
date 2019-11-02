import logging
from equipments.b2902A import B2902A
from ms_logging.ms_logger_configurator import MsLoggerConfigurator

if __name__ == '__main__':
    MsLoggerConfigurator().configure_logging(log_level=logging.INFO)
    log = logging.getLogger("test")
    driver = B2902A()
    driver.connect()
    driver.experiment()
    log.info('voltage: %f' % driver.get_voltage())
    #mode = 'curr'
    #steps = [0.01 * d for d in range(10)]
    #data = driver.run_list_mode(B2902A.Mode.CURRENT, steps)
    #log.info(data)

