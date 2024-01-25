import random
import timeit
from knapsack.instance import StateG
from knapsack.random_num import random_num
from utils.message import MessageUtilities

class GeneticSolver:
    def __init__(self, knapsack_instance, population_size, maximum_generations, crossover_probability, mutation_probability, elitism_count=3):
        self.knapsack_instance = knapsack_instance
        self.population_size = population_size
        self.maximum_generations = maximum_generations
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.elitism_count = elitism_count
        self.population = [StateG(knapsack_instance) for _ in range(population_size)]
        self.population_fitness = [0.0] * population_size
        rng_instance = random_num(seed=knapsack_instance.SEED)
        self.rng_instance = rng_instance
        #self.rng = random.Random() #self.rng = random.Random(knapsack_instance.SEED)
        self.best_state = None
        
        self.report_string = ""
        self.best_value = 0.0, 
        self.final_weight = 0.0, 
        self.execution_time = 0.0

        # Inicialización
        for i in range(population_size):
            self.population[i].generate_random_state()
            self.population_fitness[i] = self.population[i].evaluate_state()[0]
    
    def select(self):
        # Calcular la aptitud total de la población
        total_fitness = sum(self.population_fitness)
    
        if total_fitness == 0:
            # Evitar división por cero
            relative_fitness = [1 / self.population_size] * self.population_size
        else:
            # Calcular aptitud relativa
            relative_fitness = [fit / total_fitness for fit in self.population_fitness]
    
        # Calcular aptitud acumulativa
        cumulative_fitness = [sum(relative_fitness[:i + 1]) for i in range(self.population_size)]
    
        # Seleccionar sobrevivientes usando la aptitud acumulativa
        new_population = list(self.population)
        for i in range(self.population_size):
            probability = self.rng_instance.get_random_probability()
            for j in range(self.population_size):
                if probability < cumulative_fitness[j]:
                    new_population[i] = self.population[j]
                    break
    
        # Una vez que se crea una nueva población, la guardamos
        self.population = new_population

    def crossover(self):
        first = 0
        father_index = 0
        for i in range(self.population_size):
            probability = self.rng_instance.get_random_probability()
            if probability < self.crossover_probability:
                first += 1
                if first % 2 == 0:
                    # Seleccionar punto de cruce
                    split_point = self.rng_instance.get_random_number(self.knapsack_instance.NUMBER_OF_ITEMS - 1)
    
                    # Realizar cruce
                    child1 = self.population[father_index].state[:split_point] + self.population[i].state[split_point:]
                    child2 = self.population[i].state[:split_point] + self.population[father_index].state[split_point:]
    
                    # Crear nuevos objetos State para evaluar los pesos de los hijos
                    state_child1 = StateG(self.knapsack_instance)
                    state_child1.state = child1
    
                    state_child2 = StateG(self.knapsack_instance)
                    state_child2.state = child2
    
                    # Evaluar los pesos de los hijos
                    _, weight_child1 = state_child1.evaluate_state()
                    _, weight_child2 = state_child2.evaluate_state()
    
                    # Actualizar los estados con los nuevos hijos solo si cumplen con el peso máximo
                    if weight_child1 <= self.knapsack_instance.MAX_WEIGHT and weight_child2 <= self.knapsack_instance.MAX_WEIGHT:
                        self.population[father_index] = state_child1
                        self.population[i] = state_child2
    
                else:
                    father_index = i  # Actualizar el índice del padre
    
    def mutate(self):
        for i in range(self.population_size):
            for j in range(self.knapsack_instance.NUMBER_OF_ITEMS):
                probability = self.rng.random()
                if probability < self.mutation_probability:
                    self.population[i].state[j] = 1 - self.population[i].state[j]

    def evaluate(self):
        for i in range(self.population_size):
            evaluation = 0
            weight = 0
            for j in range(len(self.population[i].state)):
                if self.population[i].state[j] == 1:
                    evaluation += self.knapsack_instance.items[j][0]  # Acceder al primer valor en la tupla (value)
                    weight += self.knapsack_instance.items[j][1]      # Acceder al segundo valor en la tupla (weight)

            # Asegurémonos de que el peso no supere el máximo permitido antes de penalizar
            weight = min(weight, self.knapsack_instance.MAX_WEIGHT)

            # Penalizar las soluciones que exceden el peso máximo
            penalty_factor = 1.0  # Ajusta este factor según sea necesario
            if weight > self.knapsack_instance.MAX_WEIGHT:
                evaluation -= penalty_factor * (weight - self.knapsack_instance.MAX_WEIGHT)

            self.population_fitness[i] = evaluation
    
    def report(self, generation):
        # print(f"----- Reporte para la generación {generation} -----")
        # for i in range(self.population_size):
        #     print(f"{self.population[i]} --> {self.population_fitness[i]}")
        # print()
        string_result = "\n"
        string_result += f"----- Reporte para la generación {generation} -----\n"
        for i in range(self.population_size):
            string_result += f"""{self.population[i]} --> {self.population_fitness[i]}"""
            string_result += "\n"
        return string_result

    def save_best(self):
        # Encontrar el índice del valor más alto en el array population_fitness
        index = self.population_fitness.index(max(self.population_fitness))
        self.best_state = self.population[index]

    def elitist(self):
        self.population[:self.elitism_count] = [self.best_state] * self.elitism_count
    
    def aggressive_mutate(self):
        for i in range(self.population_size):
            mutated = False  # Variable para rastrear si se aplicó la mutación
            for j in range(self.knapsack_instance.NUMBER_OF_ITEMS):
                probability = self.rng_instance.get_random_probability()
                if probability < self.mutation_probability:
                    # Utiliza una mutación más agresiva
                    if probability < 0.5:
                        self.population[i].state[j] = 1 - self.population[i].state[j]
                    else:
                        self.population[i].state[j] = random.choice([0, 1])
    
                    mutated = True  # Marcar que se aplicó la mutación
    
            # Si se aplicó la mutación, verifica si el peso excede el máximo permitido
            if mutated:
                # Asegurémonos de que el peso no supere el máximo permitido después de la mutación
                _, weight_after_mutate = self.population[i].evaluate_state()
                if weight_after_mutate > self.knapsack_instance.MAX_WEIGHT:
                    # Si excede el peso máximo, volvemos a la versión anterior del estado
                    for j in range(self.knapsack_instance.NUMBER_OF_ITEMS):
                        self.population[i].state[j] = 1 - self.population[i].state[j]

    def solve(self):
        start_time = timeit.default_timer()
        generation = 0
        
        while generation < self.maximum_generations:
            generation += 1
            self.select()
            self.aggressive_mutate()
            self.crossover()
            #self.mutate()
            self.evaluate()
            self.save_best()
            self.elitist()
            self.report_string += self.report(generation)
        
        self.best_value, self.final_weight = self.best_state.evaluate_state()
        self.execution_time = (timeit.default_timer() - start_time) * 1000  # in milliseconds
        #return best_value, final_weight, self.best_state.state, execution_time
        
    
    def show_results(self):
        # best_state, best_value, current_weight, execution_time = self.solve()
        msg = MessageUtilities()
        msg.show_results_message(
            algorithm_name="Genetic",
            best_solution=self.best_state.state,
            best_value=self.best_value,
            final_weight=self.final_weight,
            execution_time=self.execution_time.__round__(6), # set decimals precision
            report=self.report_string,
            colorama_color="YELLOW"
        )
        

