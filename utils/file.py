import os

class FileUtilities:
    def __init__(self, data_path):        
        self.data_path = data_path
        self.list_and_sort_files()

    def list_and_sort_files(self):
        if not os.path.exists(self.data_path):
            print(f"The folder {self.data_path} does not exist.")
            return None

        files = [file for file in os.listdir(self.data_path) if os.path.isfile(
            os.path.join(self.data_path, file))]

        if len(files) == 0:
            print(f"The folder {self.data_path} is empty.")
            return None

        self.sorted_files = sorted(files, key=lambda x: int(x[1:].split("_")[0]))
        

    def show_data_content(self):
        print(f"Contents of the '{self.data_path}' folder sorted by name in ascending order:")
        print()
        for file in self.sorted_files:
            print(file)
            print()  
    
    def show_iteration_info(self, **kwargs):
        print(f"INSTANCE {kwargs['instance_number']}: ITEMS NUMBER={kwargs['items_number']}, MAX WEIGHT={kwargs['items_weight']}")
        print()
