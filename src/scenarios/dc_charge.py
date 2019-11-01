from equipments.b2902A import B2902A
from scenarios.scenario import Scenario


class Charge(Scenario):
    def __init__(self):
        super().__init__()

    def run(self, directory):
        driver = B2902A().connect()




