from scenarios.scenario import Scenario


class DummyScenario(Scenario):
    def __init__(self):
        super().__init__()
        self.name = 'dummy'

    def run(self, directory):
        file_path = "{}/{}".format(directory, self.name)
        with open(file_path, 'w') as f:
            f.write('hello')
