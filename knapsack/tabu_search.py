import random
import timeit
from knapsack.instance import StateT
from utils.message import MessageUtilities


class TabuList:
    def __init__(self, tabu_list_length):
        self.tabu_list = [None] * tabu_list_length

    def is_in(self, state):
        return state in self.tabu_list

    def push_front(self, state):
        self.tabu_list.insert(0, state)


class TabuSearchSolver:
    def __init__(self, knapsack_instance, number_of_steps, tabu_list_length):
        self.knapsack_instance = knapsack_instance
        self.state = StateT(knapsack_instance)
        self.tabu_list = TabuList(tabu_list_length)
        self.rng = random.Random()  # TODO: self.rng = random.Random(knapsack_instance.SEED)
        self.number_of_steps = number_of_steps
        
        self.best_solution = [], 
        self.best_value = 0.0, 
        self.current_weight = 0.0, 
        self.execution_time = 0.0

    def solve(self):
        start_time = timeit.default_timer()
        self.state.generate_random_state(self.rng)

        best_state = self.state.clone()  # Almacena la mejor solución encontrada
        best_candidate = self.state.clone()

        for i in range(self.number_of_steps):
            neighbours = best_candidate.get_neighbours(
                self.rng)  # Pasa rng aquí
            best_candidate_evaluation = -1

            for neighbour in neighbours:
                # Verificar si el vecino cumple con las restricciones de peso antes de evaluar
                neighbour_value, neighbour_weight = neighbour.evaluate_state()

                if neighbour_weight <= self.knapsack_instance.MAX_WEIGHT:
                    # Evaluar el vecino y actualizar si es mejor que el mejor candidato actual
                    if (
                        neighbour_value > best_candidate_evaluation
                        and not self.tabu_list.is_in(neighbour.state)
                    ):
                        best_candidate = neighbour.clone()
                        best_candidate_evaluation = neighbour_value

            if best_candidate_evaluation == -1:
                break

            # Verificar si el peso acumulado no excede el límite antes de actualizar la mejor solución
            _, best_candidate_weight = best_candidate.evaluate_state()

            if best_candidate_weight <= self.knapsack_instance.MAX_WEIGHT:
                if best_candidate_evaluation > best_state.evaluate_state()[0]:
                    best_state = best_candidate

                self.tabu_list.push_front(best_candidate.state)

            self.state = best_state  # Actualiza el estado actual al mejor vecino encontrado
            best_value, best_weight = self.state.evaluate_state()
            best_solution = self.state.state

        execution_time = (timeit.default_timer() -
                          start_time) * 1000  # in milliseconds
        # return best_value, best_weight, best_solution, execution_time
    
        self.best_solution = best_solution, 
        self.best_value = best_value, 
        self.current_weight = best_weight, 
        self.execution_time = execution_time
        
    def show_results(self):
        # best_value, best_weight, best_solution, execution_time = self.solve()
        msg = MessageUtilities()
        msg.show_results_message(
            algorithm_name="Tabu Search",
            best_solution=self.best_solution,
            best_value=self.best_value,
            final_weight=self.current_weight,
            execution_time=self.execution_time.__round__(6), # set decimals precision
            colorama_color="CYAN"
        )
        
        
