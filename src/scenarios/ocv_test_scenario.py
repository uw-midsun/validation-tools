from equipments.b2902A import B2902A
from scenarios.b2902a_list_mode_scenario import B2902AListModeScenario


class OcvTestScenario(B2902AListModeScenario):
    TIMEOUT_MS = 1e3

    def run_scenario(self, directory):
        super().run_scenario(directory)
        amplitude = 0.0
        measure_time = 2e-5
        num_triggers = 1000
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
        steps = [amplitude for _ in range(num_triggers)]
        data = self.driver.run_list_mode(B2902A.Mode.CURRENT, steps,
                                         acquire_trig_config=acquire_config,
                                         transient_trig_config=trans_config,
                                         sense_limit=sense_limit,
                                         timeout=self.TIMEOUT_MS)
        return data

