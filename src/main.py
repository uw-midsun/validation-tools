import logging
from experiment.experiment import Experiment
from ms_logging.ms_logger_configurator import MsLoggerConfigurator
from scenarios.ac_internal_scenario import AcInternalScenario
from scenarios.dc_current_pulse_scenario import DcCurrentPulseScenario
from scenarios.dc_linear_sweep_scenario import DcLinearSweepScenario
from scenarios.ocv_test_scenario import OcvTestScenario
from scenarios.ten_seconds_discharge import TenSecondsDischargeScenario


if __name__ == '__main__':
    MsLoggerConfigurator().configure_logging(log_level=logging.INFO)
    log = logging.getLogger("test")
    recipes = [
        AcInternalScenario,
        OcvTestScenario,
        DcCurrentPulseScenario,
        DcLinearSweepScenario,
        TenSecondsDischargeScenario
    ]
    e = Experiment(recipes, 'dummy_experiment')
    e.run()
