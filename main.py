import os
from colorama import init

from knapsack.instance import KnapsackInstance
from knapsack.simulated_annealing import SimulatedAnnealingSolver
from knapsack.greedy_solution import GreedySolver
from knapsack.hill_climbing import HillClimbingSolver
from knapsack.tabu_search import TabuSearchSolver
from knapsack.genetic import GeneticSolver
from knapsack.instance import State

from utils.file import FileUtilities

if __name__ == "__main__":
    init()  # Initializing Colorama

    data_path = "data/instances_01_KP/low-dimensional/"
    file_utils = FileUtilities(data_path)
    file_utils.show_data_content()

    items_list = []
    for entry in file_utils.sorted_files:
        file_path = os.path.join(file_utils.data_path, entry)
        if os.path.isfile(file_path):
            knapsack_instance = KnapsackInstance()
            knapsack_instance.load_instance(file_path)
            items_list.append(knapsack_instance)

    for i, knapsack_instance in enumerate(items_list, start=1):
        # Show iteration data as header
        file_utils.show_iteration_info(
            instance_number=i,
            items_number=knapsack_instance.NUMBER_OF_ITEMS,
            items_weight=knapsack_instance.MAX_WEIGHT,                     
        )

        # **Simulated Annealing**
        # Instantiate the solver
        annealing_solver = SimulatedAnnealingSolver(knapsack_instance, initial_temperature=1000, cooling_rate=0.03, max_iterations=1000)       
        # Run the algorithm
        annealing_solver.solve()
        # Show results
        annealing_solver.show_results()

        # **Greedy**
        # Instantiate the solver
        greedy_solver = GreedySolver(knapsack_instance)        
        # Run the algorithm
        greedy_solver.solve()
        # Show results        
        greedy_solver.show_results()

        # **Hill Climbing BI**
        # Instantiate the solver
        solver_best = HillClimbingSolver(knapsack_instance)
        # Run the algorithm
        solver_best.solve(method="best_improvement")
        # Show results        
        solver_best.show_results(algorithm_name="Hill Climbing BI")

        # **Hill Climbing FI**
        # Instantiate the solver
        solver_first = HillClimbingSolver(knapsack_instance)
        # Run the algorithm
        solver_first.solve(method="first-improvement")
        # Show results        
        solver_first.show_results(algorithm_name="Hill Climbing FI")

        # **Tabu Search**
        # Instantiate the solver
        tabu_solver = TabuSearchSolver(knapsack_instance, number_of_steps=100, tabu_list_length=10)
        # Run the algorithm
        tabu_solver.solve()
        # Show results
        tabu_solver.show_results()


        # **Genetic**
        # Instantiate the solver
        genetic_solver = GeneticSolver(knapsack_instance, population_size=20, maximum_generations=30, crossover_probability=0.8, mutation_probability=0.05)
        # Run the algorithm
        genetic_solver.solve()
        # Show results
        genetic_solver.show_results()
        

        # Eliminate reference to class instances
        del (annealing_solver)
        del (greedy_solver)
        del (solver_best)
        del (solver_first)
        del (tabu_solver)
        del (genetic_solver)
