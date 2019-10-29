import logging
import pyvisa
from equipments.exceptions import DeviceNotFoundException


# driver for KeySight B2902A
class B2902A(object):
    RESOURCE_ID = 'USB0::0x0957::0x8C18::MY51143785::INSTR'
    RESET_COMMAND = "*RST"
    SELF_ID_QUERY = "*IDN?"

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

    def write(self, cmd):
        return self.instrument.write(cmd)

    def query(self, cmd):
        return self.instrument.query(cmd)

    def connect(self, resource_id=None):
        resource_id = resource_id or self.get_first_resource()
        log.info("connecting to %s" % resource_id)
        self.instrument = self.resource_manager.open_resource(resource_id)
        self.instrument.write(B2902A.RESET_COMMAND)

    def measure_voltage(self):
        self.instrument.write("OUTP:ON:AUTO ON")
        return float(self.instrument.query("VOLT?"))


log = logging.getLogger("{}.{}".format(B2902A.__module__, B2902A.__name__))
