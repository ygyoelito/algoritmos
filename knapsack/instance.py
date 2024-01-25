import random

class KnapsackInstance:
    def __init__(self):
        self.NUMBER_OF_ITEMS = 0
        self.MAX_WEIGHT = 0
        self.items = []
        self.SEED = None  # Agrega un atributo SEED con un valor predeterminado None

    def load_instance(self, file_path):
        with open(file_path, 'r') as infile:
            first_line = infile.readline().strip()
            knapsack_instance_values = [int(value) for value in first_line.split()]
            self.NUMBER_OF_ITEMS = knapsack_instance_values[0]
            self.MAX_WEIGHT = knapsack_instance_values[1]
            self.items = []
            for line in infile:
                value, weight = map(float, line.split())
                self.items.append((value, weight))

    def get_neighbour(self, state):
        neighbour = state.copy()
        index = random.randint(0, len(state) - 1)
        neighbour[index] = 1 - neighbour[index]
        return neighbour

    def evaluate_state(self, state):
        total_value = 0
        total_weight = 0
        for i in range(len(state)):
            if state[i] == 1:
                total_value += self.items[i][0]
                total_weight += self.items[i][1]
        return total_value, total_weight
    
class State:
    def __init__(self, knapsack_instance, rng):
        self.knapsack_instance = knapsack_instance
        self.rng = rng  
        self.state = [0] * knapsack_instance.NUMBER_OF_ITEMS
        self.value = 0.0
        self.weight = 0.0

    def evaluate_state(self):
        total_weight = 0.0
        total_value = 0.0
        # Calcula el valor y el peso total del estado actual de la mochila
        for i in range(len(self.state)):
            if self.state[i] == 1:
                total_value += self.knapsack_instance.items[i][0]
                total_weight += self.knapsack_instance.items[i][1]
        # Retorna -1 si el peso total excede el peso máximo permitido
        if total_weight > self.knapsack_instance.MAX_WEIGHT:
            return -1, -1
        return total_value, total_weight
        
    def get_neighbour(self):
        neighbours = []
        for i in range(len(self.state)):
            neighbour = self.state.copy()
            neighbour[i] = 1 - neighbour[i]
            neighbour_state = State(self.knapsack_instance, self.rng)
            neighbour_state.state = neighbour
            neighbours.append(neighbour_state)
        return neighbours
        
    def generate_random_state(self):
        while True:
            for i in range(len(self.state)):
                # Get a random integer number in the range [0, 1]
                random_number = self.rng.randint(0, 1)
                self.state[i] = random_number

            # Verifica si la solución es factible
            if self.evaluate_state()[0] >= 0:
                return

    def generate_neighbour(self, index):
        neighbour = self.state.copy()
        neighbour[index] = 1 - neighbour[index]
        neighbour_state = State(self.knapsack_instance, self.rng)
        neighbour_state.state = neighbour
        return neighbour_state
    
    def generate_random_neighbour(self):
        neighbour = self.get_neighbour()
        neighbour_state = State(self.knapsack_instance)
        neighbour_state.state = neighbour
        return neighbour_state
    
class StateT:
    def __init__(self, knapsack_instance):
        self.knapsack_instance = knapsack_instance
        self.state = [0] * knapsack_instance.NUMBER_OF_ITEMS

    def generate_random_state(self, rng):
        for i in range(len(self.state)):
            self.state[i] = rng.randint(0, 1)

    def evaluate_state(self):
        total_weight = 0.0
        total_value = 0.0

        for i in range(len(self.state)):
            if self.state[i] == 1:
                total_value += self.knapsack_instance.items[i][0]
                total_weight += self.knapsack_instance.items[i][1]

        # Si el peso total excede el límite, devuelve -1 para indicar una solución no válida
        if total_weight > self.knapsack_instance.MAX_WEIGHT:
            return -1, -1

        return total_value, total_weight


    def get_neighbours(self, rng):
        neighbours = []

        for i in range(len(self.state)):
            neighbour = self.state.copy()
            neighbour[i] = 1 - neighbour[i]  # Cambia el estado del elemento

            neighbour_state = StateT(self.knapsack_instance)
            neighbour_state.state = neighbour

            # Ciclo hasta encontrar un vecino que cumple con las restricciones de peso
            while True:
                # Verifica si el nuevo vecino cumple con las restricciones de peso
                neighbour_value, neighbour_weight = neighbour_state.evaluate_state()
                if neighbour_value != -1 and neighbour_weight <= self.knapsack_instance.MAX_WEIGHT:
                    neighbours.append(neighbour_state)
                    break
                else:
                    # Si el vecino no cumple, genera uno nuevo
                    neighbour_state = StateT(self.knapsack_instance)
                    neighbour_state.generate_random_state(rng)

        return neighbours

    def clone(self):
        # Crea una copia profunda del estado actual
        new_state = StateT(self.knapsack_instance)
        new_state.state = self.state.copy()
        return new_state

class StateG:
    def __init__(self, knapsack_instance):
        self.knapsack_instance = knapsack_instance
        self.state = [0] * knapsack_instance.NUMBER_OF_ITEMS

    def generate_random_state(self):
        self.state = [random.choice([0, 1]) for _ in range(len(self.state))]

    def evaluate_state(self):
        evaluation = 0
        weight = 0
        for j in range(len(self.state)):
            if self.state[j] == 1:
                evaluation += self.knapsack_instance.items[j][0]  # Acceder al primer valor en la tupla (value)
                weight += self.knapsack_instance.items[j][1]      # Acceder al segundo valor en la tupla (weight)
        return evaluation, weight

    def __str__(self):
        return str(self.state)