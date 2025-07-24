from datetime import datetime
from enum import Enum

# an enum has been used as the tasks priority can only be defined as these specific values
# (effectively a constant)
class TaskPriority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    VERY_HIGH = 3

class Task:
    def __init__(self, title: str, due_date: datetime, class_name: str, priority: TaskPriority):
        print(type(due_date))
        # type check
        assert(isinstance(due_date, datetime))
        # existence check
        assert(not priority is None)

        self.title = title
        self.due_date = due_date
        self.class_name = class_name
        self.completed = False
        self.priority = priority
    
    def __str__(self) -> str:
        return f"{self.title} {self.due_date.strftime("%d/%m/%y")} {self.class_name} {str(self.priority)} {str(self.completed)}"

    def is_complete(self) -> bool:
        return self.completed
    
    def complete_task(self):
        self.completed = True
    
    def uncomplete_task(self):
        self.completed = False
    
    
    def is_overdue(self) -> bool:
        return datetime.now() > self.due_date
    
    def get_due_date(self) -> datetime:
        return self.due_date

    def set_due_date(self, new_date: datetime):
        self.due_date = new_date
    

    def get_priority(self) -> TaskPriority:
        return self.priority
    
    def set_priority(self, new_priority: TaskPriority):
        self.priority = new_priority
    

    def get_title(self) -> str:
        return self.title
    
    def set_title(self, new_title: str):
        self.title = new_title
    
    
    def get_class(self) -> str:
        return self.class_name

    def set_class(self, new_class: str):
        self.class_name = new_class
