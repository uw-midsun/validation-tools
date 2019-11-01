class DataGenerator(object):
    def generate_b2902a_data(self, data):
        file_name = time
        with open('eggs.csv', newline='') as csvfile:
            ...
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        ...
        for row in spamreader:
            ...
            print(', '.join(row))