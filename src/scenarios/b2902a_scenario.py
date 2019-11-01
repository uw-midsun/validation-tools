from equipments.b2902A import B2902A
from scenarios.scenario import Scenario


class B2902AScenario(Scenario):
    def __init__(self):
        super().__init__()
        self.driver = B2902A()
        self.driver.connect()


