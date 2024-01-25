import math
import timeit
from knapsack.random_num import random_num
from utils.message import MessageUtilities


class SimulatedAnnealingSolver:

    def __init__(self, knapsack_instance, initial_temperature, cooling_rate, max_iterations) -> None:
        self.knapsack_instance = knapsack_instance
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.max_iterations = max_iterations
        self.rng_instance = random_num(seed=self.knapsack_instance.SEED)   
        
        self.best_solution = [], 
        self.best_value = 0.0, 
        self.current_weight = 0.0, 
        self.execution_time = 0.0
            

    def solve(self):

        start_time = timeit.default_timer()
        current_state = [0] * self.knapsack_instance.NUMBER_OF_ITEMS
        current_value = 0
        current_weight = 0
        best_state = current_state
        best_value = current_value
        temperature = self.initial_temperature

        for _ in range(self.max_iterations):
            neighbour = self.knapsack_instance.get_neighbour(current_state)
            neighbour_value, neighbour_weight = self.knapsack_instance.evaluate_state(
                neighbour)

            if neighbour_weight <= self.knapsack_instance.MAX_WEIGHT and (neighbour_value > current_value or self.rng_instance.get_random_probability() < math.exp((neighbour_value - current_value) / temperature)):
                current_state = neighbour
                current_value = neighbour_value
                current_weight = neighbour_weight

            if current_value > best_value:
                best_state = current_state
                best_value = current_value

            temperature *= 1 - self.cooling_rate

        self.execution_time = (timeit.default_timer() -
                          start_time) * 1000  # in milliseconds

        self.best_solution = best_state, 
        self.best_value = best_value, 
        self.current_weight = current_weight, 
        # return best_state, best_value, current_weight, self.execution_time
        

    def show_results(self):
        # best_state, best_value, current_weight, execution_time = self.solve()
        msg = MessageUtilities()
        msg.show_results_message(
            algorithm_name="Simulated Annealing",
            best_solution=self.best_solution,
            best_value=self.best_value,
            final_weight=self.current_weight,
            execution_time=self.execution_time.__round__(6), # set decimals precision
            colorama_color="BLUE"
        )
