import logging
import pyvisa
from equipments.exceptions import DeviceNotFoundException


# driver for KeySight B2902A
class B2902A(object):
    RESOURCE_ID = 'USB0::0x0957::0x8C18::MY51143785::INSTR'
    RESET_COMMAND = "*RST"
    SELF_ID_QUERY = "*IDN?"
    TIMEOUT = 1e3

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

    def _get_user_input(self):
        usr_inp = input()
        if usr_inp == "exit":
            return False
        if usr_inp[-1] == '?':
            log.info(self.query(usr_inp))
        else:
            log.info(self.write(usr_inp))
        return True

    def experiment(self):
        # enters experiment mode
        while self._get_user_input():
            pass

    def write(self, cmd, timeout=TIMEOUT):
        prev_timeout = self.instrument.timeout
        self.instrument.timeout = timeout
        log.debug(cmd)
        status = self.instrument.write(cmd)
        self.instrument.query('*opc?')
        self.instrument.timeout = prev_timeout
        return status

    def query(self, cmd):
        return self.instrument.query(cmd)

    SENSE_MAX_KEY = 'max'
    SENSE_MIN_KEY = 'min'
    DEFAULT_SENSE_LIMIT_CURR = {
        SENSE_MAX_KEY: 3,
        SENSE_MIN_KEY: -3
    }
    DEFAULT_SENSE_LIMIT_VOLT = {
        SENSE_MAX_KEY: 4.2,
        SENSE_MIN_KEY: 2.5
    }
    DEFAULT_ACQUIRE_CONFIG = {
        'count': 50,
        'time': 2e-5,
        'source': 'tim',
        'delay': 0
    }
    DEFAULT_TRANSIENT_CONFIG = {
        'count': 50,
        'time': 2e-5,
        'source': 'tim',
        'delay': 0
    }

    class Mode:
        CURRENT = 'curr'
        VOLTAGE = 'volt'

    def run_list_mode(self, mode, steps,
                      transient_trig_config=None,
                      acquire_trig_config=None,
                      sense_limit=None,
                      timeout=TIMEOUT):
        sense_limit = sense_limit or B2902A.DEFAULT_SENSE_LIMIT_CURR if \
            mode is B2902A.Mode.VOLTAGE \
            else B2902A.DEFAULT_SENSE_LIMIT_VOLT
        acquire_trig_config = acquire_trig_config or B2902A.DEFAULT_ACQUIRE_CONFIG
        transient_trig_config = transient_trig_config or B2902A.DEFAULT_TRANSIENT_CONFIG
        op_mode_lookup = {
            "volt": "curr",
            "curr": "volt"
        }
        op_mode = op_mode_lookup[mode]
        commands = [
            "sens:rem on",
            "func:mode %s" % mode,
            "sour:%s:mode list" % mode,
            "sour:mode:%s on" % mode,
            "sour:list:%s %s" % (mode, ",".join([str(s)for s in steps])),
            "trigger:acq:coun %s" % (acquire_trig_config['count']),
            "trigger:tran:coun %s" % (transient_trig_config['count']),
            "trigger:acq:tim %s" % (acquire_trig_config['time']),
            "trigger:tran:tim %s" % (transient_trig_config['time']),
            "trigger:acq:del %s" % (acquire_trig_config['delay']),
            "trigger:tran:del %s" % (transient_trig_config['delay']),
            "trigger:acq:sour %s" % (acquire_trig_config['source']),
            "trigger:tran:sour %s" % (transient_trig_config['source']),
            "sens:func: %s" % op_mode,
            "sens:%s:prot:pos %s" % (op_mode, sense_limit['max']),
            "sens:%s:prot:neg %s" % (op_mode, sense_limit['min']),
            "*wai"
        ]
        for c in commands:
            self.write(c)
        #self.experiment() # uncomment if debugging
        self.write('init', timeout=timeout)
        op = self.query('*opc?')
        if not op == '1\n':
            log.error('operation not complete: %s' % op)
        self.write('outp off')
        raw_data = self.query('sens:data?')
        data = self.convert_from_raw_data(raw_data)
        return data

    def convert_from_raw_data(self, raw_data):
        raw_data.split(',')
        data = []
        keys = ['voltage', 'current', 'resistance', 'time', 'stat', 'sour']
        l_keys = len(keys)
        d = {}
        for i, s in enumerate(raw_data.split(',')):
            f = i % l_keys
            d[keys[f]] = s
            if f == l_keys - 1:
                data.append(d.copy())
        return data

    def connect(self, resource_id=None):
        resource_id = resource_id or self.get_first_resource()
        log.info("connecting to %s" % resource_id)
        self.instrument = self.resource_manager.open_resource(resource_id)
        self.instrument.write(B2902A.RESET_COMMAND)

    def measure_voltage(self):
        self.instrument.write("OUTP:ON:AUTO ON")
        return float(self.instrument.query("VOLT?"))


log = logging.getLogger("{}.{}".format(B2902A.__module__, B2902A.__name__))
