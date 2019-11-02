from equipments.b2902A import B2902A
from scenarios.b2902a_list_mode_scenario import B2902AListModeScenario


class TenSecondsDischargeScenario(B2902AListModeScenario):
    TIMEOUT_MS = 20e3

    def run_scenario(self, directory):
        super().run_scenario(directory)
        current = -3
        total_time = 10
        num_triggers = 1e5/4
        measure_time = total_time / num_triggers
        num_steps = 20
        steps = [current] * num_steps
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
        data = self.driver.run_list_mode(B2902A.Mode.CURRENT, steps,
                                         acquire_trig_config=acquire_config,
                                         transient_trig_config=trans_config,
                                         sense_limit=sense_limit,
                                         timeout=self.TIMEOUT_MS)
        return data


