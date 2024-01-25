import random

class random_num:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)

    def get_random_number(self, max_value):
        return self.rng.randint(0, max_value)

    def get_random_probability(self):
        return self.rng.uniform(0, 1) / 100.0  # Divide el resultado por 100