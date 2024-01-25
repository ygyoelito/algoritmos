import random
import timeit
from knapsack.instance import State
from utils.message import MessageUtilities


class HillClimbingSolver:
    def __init__(self, knapsack_instance):
        self.rng = random.Random()
        self.knapsack_instance = knapsack_instance
        self.state = State(knapsack_instance, self.rng)
        
        self.best_solution = [], 
        self.best_value = 0.0, 
        self.current_weight = 0.0, 
        self.execution_time = 0.0
        self.colorama_color = None 

    def best_improvement(self):
        self.state.generate_random_state()

        best_value, best_weight = self.state.evaluate_state()
        best_solution = self.state.state.copy()

        while True:
            current_value, current_weight = best_value, best_weight
            best_neighbour = None

            all_neighbours = [self.state.generate_neighbour(
                i) for i in range(len(self.state.state))]

            for neighbour in all_neighbours:
                neighbour_value, neighbour_weight = neighbour.evaluate_state()

                if (
                    neighbour_value > current_value
                    and neighbour_weight <= self.knapsack_instance.MAX_WEIGHT
                ):
                    if (
                        best_neighbour is None
                        or neighbour_value > best_neighbour.evaluate_state()[0]
                    ):
                        best_neighbour = neighbour

            if best_neighbour is None:
                break

            best_value, best_weight = best_neighbour.evaluate_state()
            best_solution = best_neighbour.state.copy()

        return best_value, best_weight, best_solution

    def first_improvement(self):
        while True:
            neighbours = self.state.get_neighbour()
            new_state_index = -1

            # Buscar la primera mejora entre los vecinos
            for i, neighbour in enumerate(neighbours):
                # Verificar si el nuevo vecino es mejor
                if neighbour.evaluate_state() > self.state.evaluate_state():
                    # Guardar el vecino como el nuevo estado y calcular la nueva evaluación
                    self.state = neighbour  # Asigna el objeto neighbour directamente a self.state
                    new_state_index = i
                    break

            # Si no se encontró un vecino mejor, salir del bucle
            if new_state_index == -1:
                break
        best_value, best_weight = self.state.evaluate_state()
        best_solution = self.state.state
        return best_value, best_weight, best_solution

    def solve(self, method):
        start_time = timeit.default_timer()
        if method == "best_improvement":
            best_value, best_weight, best_solution = self.best_improvement()
            self.colorama_color = "RED"
        if method == "first-improvement":
            best_value, best_weight, best_solution = self.first_improvement()
            self.colorama_color = "GREEN"

        self.execution_time = (timeit.default_timer() -
                          start_time) * 1000  # in milliseconds

        self.best_solution = best_solution, 
        self.best_value = best_value, 
        self.current_weight = best_weight, 
        #return best_value, best_weight, best_solution, self.execution_time

    def show_results(self, algorithm_name=None):
        # best_value, best_weight, best_solution, execution_time = self.solve()
        msg = MessageUtilities()
        msg.show_results_message(
            algorithm_name=algorithm_name,
            best_solution=self.best_solution,
            best_value=self.best_value,
            final_weight=self.current_weight,
            execution_time=self.execution_time.__round__(6),  # set decimals precision
            colorama_color=self.colorama_color
        )
