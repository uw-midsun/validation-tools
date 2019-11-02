from equipments.b2902A import B2902A
from scenarios.b2902a_list_mode_scenario import B2902AListModeScenario


class DcCurrentPulseScenario(B2902AListModeScenario):
    TIMEOUT_MS = 10e3

    def run_scenario(self, directory):
        super().run_scenario(directory)
        measure_time = 12.5e-3
        start = 0.5
        delta = 0.5
        end = 3
        num_levels = round((end - start)/delta) + 1
        points_in_each_level = 20
        steps = []
        for i in range(num_levels):
            steps += [0] * points_in_each_level
            level = start + i * delta
            steps += [level] * points_in_each_level
            steps += [0] * points_in_each_level
            steps += [-level] * points_in_each_level
        num_triggers = len(steps)
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


