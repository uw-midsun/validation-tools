import logging
from equipments.scale import Scale
from ms_logging.ms_logger_configurator import MsLoggerConfigurator


def main():
	MsLoggerConfigurator().configure_logging()
	log = logging.getLogger('test')
	s = Scale().calibrate()
	log.info("Please put the weight on then hit enter")
	input()
	w = []
	num = 1000
	for i in range(num):
		w.append(s.measure_weight())
	sum_weights = 0
	for we in w:
		sum_weights += we
	avg = sum_weights / num
	log.info("Measured weight: %s" % avg)


if __name__ == '__main__':
	main()

