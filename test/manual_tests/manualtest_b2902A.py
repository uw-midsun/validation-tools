import logging
from equipments.b2902A import B2902A
from ms_logging.ms_logger_configurator import MsLoggerConfigurator

if __name__ == '__main__':
    MsLoggerConfigurator().configure_logging(log_level=logging.INFO)
    log = logging.getLogger("test")
    driver = B2902A()
    driver.connect()
    """
        outp: on/off
        sens: only sets the sensing parameters
        volt // sets to volt
        curr    
    """
    def dothatshit():
        usr_inp = input()
        if usr_inp[-1] == '?':
            log.info(driver.query(usr_inp))
        else:
            log.info(driver.write(usr_inp))
    while (True):
        try:
            dothatshit()
        except:
            pass











