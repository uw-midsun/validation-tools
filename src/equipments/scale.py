import logging

from Phidget22.Devices.VoltageRatioInput import VoltageRatioInput


class Scale(object):
    CALIBRATION_WEIGHT = 20
    WAIT = 1000

    def __init__(self):
        self.channel = VoltageRatioInput()
        self.channel.openWaitForAttachment(Scale.WAIT)
        self.lower_ratio = None
        self.higher_ratio = None

    def wait_for_keypress(self, queue):
        while queue.empty():
            pass
        while not queue.empty():
            queue.get()

    def calibrate(self, queue):
        log.info("Beginning calibration.")
        log.info("Please take off any weights from the scale and hit enter:")
        self.wait_for_keypress(queue)
        self.lower_ratio = self.measure_ratio()
        log.info("Please put the %sg weight on scale and hit enter:" % Scale.CALIBRATION_WEIGHT)
        self.wait_for_keypress(queue)
        self.higher_ratio = self.measure_ratio()
        return self

    def measure_ratio(self):
        voltage_ratio = self.channel.getVoltageRatio()
        return float(voltage_ratio)

    def measure_weight(self):
        ratio = self.measure_ratio()
        return self.CALIBRATION_WEIGHT * (ratio - self.lower_ratio) / (self.higher_ratio - self.lower_ratio)


log = logging.getLogger("{}.{}".format(Scale.__module__, Scale.__name__))





