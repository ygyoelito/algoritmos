from colorama import Fore, Back
class MessageUtilities:
    color_mapping = {
        "BLUE": Fore.BLUE,
        "MAGENTA": Fore.MAGENTA,
        "GREEN": Fore.GREEN,
        "RED": Fore.RED,
        "YELLOW": Fore.YELLOW,
        "CYAN": Fore.CYAN,
        "WHITE": Fore.WHITE,
        "BLACK": Fore.BLACK,
        "RESET": Fore.RESET,
    }

    def __init__(self) -> None:
        pass

    def show_results_message(self, **kargs):
        print(self.color_mapping.get(kargs['colorama_color'], Fore.RESET) + Back.BLACK + f"**** {kargs['algorithm_name'].upper()} ****")
        print(self.color_mapping.get(kargs['colorama_color'], Fore.RESET) + Back.BLACK + f"\tBest Solution: {kargs['best_solution']}")
        print(self.color_mapping.get(kargs['colorama_color'], Fore.RESET) + Back.BLACK + f"\tBest Value: {kargs['best_value']}")
        print(self.color_mapping.get(kargs['colorama_color'], Fore.RESET) + Back.BLACK + f"\tFinal weight: {kargs['final_weight']}")
        print(self.color_mapping.get(kargs['colorama_color'], Fore.RESET) + Back.BLACK + f"\tExecution time (ms): {kargs['execution_time']}")
        
        if 'report' in kargs:
            print(self.color_mapping.get(kargs['colorama_color'], Fore.RESET) + Back.BLACK + kargs['report'])
        print()      
