import logging
import pyvisa
from equipments.exceptions import DeviceNotFoundException


class Bk8600(object):
    RESOURCE_ID = 'USB0::0xFFFF::0x8800::602197010707510034::INSTR'
    CURRENT_LEVEL_COMMAND = "CURR:LEV"
    RESET_COMMAND = "*RST"
    SELF_ID_QUERY = "*IDN?"

    class Input(object):
        ON = "INP ON"
        OFF = "INP OFF"

    class Functions(object):
        CONSTANT_CURRENT = 'CURR'
        CONSTANT_VOLTAGE = 'VOLT'
        CONSTANT_RESISTANCE = 'RES'
        CONSTANT_POWER = 'POW'

    class Modes(object):
        FIXED = 'FIX'
        LIST = 'LIST'

    # Initialize to the bay's BK8600 address through USB
    def __init__(self, resource_id=RESOURCE_ID):
        self.resource_manager = pyvisa.ResourceManager()
        self.instrument = None

    def list_all_resources(self):
        msg = "Available resources: \n"
        resources = self.resource_manager.list_resources()
        for r in self.resource_manager.list_resources():
            msg += "\t%s\n" % r
        log.debug(msg)
        return resources

    def get_first_resource(self):
        resources = self.list_all_resources()
        if not resources:
            raise DeviceNotFoundException()
        return resources[0]

    def connect(self, resource_id=None):
        resource_id = resource_id or self.get_first_resource()
        log.info("connecting to %s" % resource_id)
        self.instrument = self.resource_manager.open_resource(resource_id)
        self.instrument.write(Bk8600.RESET_COMMAND)

    def set_current_level(self, current_setpoint_amps):
        self.instrument.write("{} {}".format(Bk8600.CURRENT_LEVEL_COMMAND, current_setpoint_amps))
        self.instrument.query("*OPC?")

    def set_function(self, function):
        self.instrument.write("FUNC {}".format(function))

    def set_mode(self, mode):
        self.instrument.write("FUNC:MODE {}".format(mode))

    def set_input(self, input):
        self.instrument.write(input)

    def toggle_eload(self, state):
        if state:
            self.set_input(Bk8600.Input.ON)
        else:
            self.set_input(Bk8600.Input.OFF)

    def set_voltage(self, voltage):
        self.instrument.write("VOLT %s" % voltage)

    def set_current(self, current):
        self.instrument.write("CURR %s" % current)

    def measure_voltage(self):
        return float(self.instrument.query("MEAS:VOLT:DC?"))

    def measure_current(self):
        return float(self.instrument.query("MEAS:CURR:DC?"))

    def get_list_step_counts(self):
        return int(self.instrument.query("LIST:COUN?"))

    def set_list(self, steps):
        num_steps = len(steps)
        levels = [str(s['level']) for s in steps]
        curr_range = 2
        repeat = 1
        save = 2
        self.instrument.write("LIST:RANG %s" % curr_range)
        self.instrument.write("LIST:COUN %s" % repeat)
        self.instrument.write("LIST:STEP %s" % num_steps)
        log.info("LIST:STEP %s" % num_steps)
        for i in range(num_steps):
            self.instrument.write("LIST:LEV %d,%s" % (i + 1, levels[i]))
            self.instrument.write("LIST:SLEW %d,%s" % (i + 1, 1))
            self.instrument.write("LIST:WIDTH %d,%sms" % (i + 1, 1000))
            log.info("LIST:LEV %d,%s" % (i + 1, levels[i]))
            log.info("LIST:SLEW %d,%s" % (i + 1, 1))
            log.info("LIST:WIDTH %d,%sms" % (i + 1, 1000))
        self.instrument.write("LIST:SAV %d" % save)
        self.instrument.write("FUNC:MODE LIST")
        self.instrument.write("TRIG:SOUR BUS")
        self.instrument.write("*TRG")


log = logging.getLogger("{}.{}".format(Bk8600.__module__, Bk8600.__name__))
