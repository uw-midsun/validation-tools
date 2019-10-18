import logging
import pyvisa

# E load
class Bk8600(object):
    RESOURCE_ID = 'USB0::65535::34816::602197010707510034::0::INSTR'
    CURRENT_LEVEL_COMMAND = "CURR:LEV"
    INPUT_ON_CMD = "INPut ON"
    INPUT_OFF_CMD = "INPut OFF"
    DC_VOLTAGE_QUERY = "MEAS:VOLT:DC?"
    DC_CURRENT_QUERY = "MEAS:CURR:DC?"
    RESET_COMMAND = "*RST"
    SELF_ID_QUERY = "*IDN?"

    # Initialize to the bay's BK8600 address through USB
    def __init__(self, resource_id=RESOURCE_ID):
        self.instrument = pyvisa.ResourceManager().open_resource(resource_id)
        log.info("Connected to %s\n" % self.instrument.query(Bk8600.SELF_ID_QUERY))
        self.instrument.write(Bk8600.RESET_COMMAND)

    # To Set E-Load in Amps
    def set_current(self, current_setpoint_amps):
        self.instrument.write("{} {}".format(Bk8600.CURRENT_LEVEL_COMMAND, current_setpoint_amps))
        self.instrument.query("*OPC?")
        self._set_input_on()

    def _set_input_on(self):
        self.instrument.write(Bk8600.INPUT_ON_CMD)

    def _set_input_off(self):
        self.instrument.write(Bk8600.INPUT_OFF_CMD)

    def toggle_eload(self, state):
        if state:
            self._set_input_on()
        else:
            self._set_input_off()

    def measure_voltage(self):
        return float(self.instrument.query(Bk8600.DC_VOLTAGE_QUERY))

    def measure_current(self):
        return float(self.instrument.query(Bk8600.DC_CURRENT_QUERY))


log = logging.getLogger("{}.{}".format(Bk8600.__module__, Bk8600.__name__))
