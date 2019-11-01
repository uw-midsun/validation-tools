import logging
import math

from equipments.b2902A import B2902A
from scenarios.b2902a_list_mode_scenario import B2902AListModeScenario


class AcInternalScenario(B2902AListModeScenario):
    TIMEOUT_MS = 2e3

    def run_scenario(self, directory):
        amplitude = 0.1
        measure_time = 2e-5
        num_cycles = 500
        freq = 1e3
        cycle_duration = 1/freq
        num_triggers = int(num_cycles * cycle_duration / measure_time) + 1
        acquire_config = {
            'count': num_triggers,
            'time': measure_time,
            'source': 'tim',
            'delay': measure_time/2
        }
        trans_config = acquire_config.copy()
        trans_config['delay'] = 0
        sense_limit = {
            'max': 4.2,
            'min': 2.5
        }
        steps_in_cycle = int(cycle_duration / measure_time)
        times = [i * measure_time for i in range(steps_in_cycle)]
        steps = [amplitude * math.sin(2 * math.pi * freq * t) for t in times]
        data = self.driver.run_list_mode(B2902A.Mode.CURRENT, steps,
                                         acquire_trig_config=acquire_config,
                                         transient_trig_config=trans_config,
                                         sense_limit=sense_limit,
                                         timeout=self.TIMEOUT_MS)
        return data


log = logging.getLogger("{}.{}".format(AcInternalScenario.__module__, AcInternalScenario.__name__))




