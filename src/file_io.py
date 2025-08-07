import jsonpickle

from task import *
from utils import ErrorMessage

# ? Data sources
# ?     - task file (.tsk): was used as the primary data source because it provides a method of persistent data storage between sessions, allowing the user to save tasks they created in one session and load them in another session

# load tasks from file path
def load_tasks(path: str) -> list[Task] | None:
    # will display an error message if open(path) fails
    try:
        with open(path) as save_file:
            # will display an error if the file cannot be decoded
            try:
                # ! the file data is the primary data source for the application
                # it allows the user to have tasks that persist between sessions
                return jsonpickle.decode(save_file.read())
            except:
                ErrorMessage("Unable to load task file", "Selected task file could not be loaded because it is invald. Check if you have selected the correct file and that the file has not been corrupted.")
    except:
        ErrorMessage("Unable to open file", "Unable to open file, please make sure it exists")

# save the list of Tasks to a file at the provided file path
def save_tasks(path: str, tasks: list[Task]):
    # will display an error message if open() fails
    try:
        with open(path, "w") as save_file:
            # will display an error message if the data cannot be encoded
            try:
                json_data = jsonpickle.encode(tasks)
                if not json_data is None:
                    save_file.write(json_data)
                else:
                    # raise an exception if the encoded data is None
                    # triggers error handling
                    raise ValueError
            except:
                ErrorMessage("Unable to save tasks", "Unable to save tasks to file. Ensure that the file location is able to be written to.")
    except:
        ErrorMessage("Unable to save tasks", "Unable to write to selected file location. Please ensure that the file location is valid and writable.")