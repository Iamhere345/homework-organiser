import jsonpickle

from task import *
from utils import ErrorMessage

def load_tasks(path: str) -> list[Task] | None:
    try:
        with open(path) as save_file:
            try:
                return jsonpickle.decode(save_file)
            except:
                ErrorMessage("Unable to load task file", "Selected task file is invalid. Check if you have selected the correct file.")
    except:
        ErrorMessage("Unable to open file", "Unable to open file, please make sure it exists")

def save_tasks(path: str, tasks: list[Task]):
    try:
        with open(path, "w") as save_file:
            try:
                json_data = jsonpickle.encode(tasks)
                if not json_data is None:
                    save_file.write(json_data)
                else:
                    raise ValueError
            except:
                ErrorMessage("Unable to save tasks", "Unable to save tasks to file. Ensure that the file location is able to be written to.")
    except:
        ErrorMessage("Unable to save tasks", "Unable to write to selected file location. Please ensure that the file location is valid and writable.")