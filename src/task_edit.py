from datetime import datetime
import calendar

from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from task import *

class TaskEdit(QtWidgets.QVBoxLayout):
    def __init__(self):
        super().__init__()
        super().setAlignment(Qt.AlignmentFlag.AlignTop)

        self.title = QtWidgets.QLabel('<h1>Task Title</h1>')
        super().addWidget(self.title)

        self.show_txt_fields()
        self.show_btn_fields()
        self.show_date_picker()

    def show_txt_fields(self):
        self.txt_hbox = QtWidgets.QHBoxLayout()
        
        self.name_field = QtWidgets.QLineEdit()
        self.name_field.setPlaceholderText("Enter Name")
        self.txt_hbox.addWidget(self.name_field)

        self.class_field = QtWidgets.QLineEdit()
        self.class_field.setPlaceholderText("Enter Class")
        self.txt_hbox.addWidget(self.class_field)

        super().addLayout(self.txt_hbox)

    def show_btn_fields(self):
        self.btn_hbox = QtWidgets.QHBoxLayout()

        self.complete_btn = QtWidgets.QPushButton("Mark as complete")
        self.btn_hbox.addWidget(self.complete_btn)

        self.priority_combo = QtWidgets.QComboBox()
        self.priority_combo.addItems([
            "Set Priority",
            "Low",
            "Medium",
            "High",
            "Very High",
        ])
        self.btn_hbox.addWidget(self.priority_combo)

        super().addLayout(self.btn_hbox)

    def show_date_picker(self):
        self.date_picker_title = QtWidgets.QLabel("<h4>Due Date<h4/>")
        super().addWidget(self.date_picker_title)

        self.date_picker = DatePicker()
        #self.date_picker = QtWidgets.QCalendarWidget()
        super().addLayout(self.date_picker)

    def set_selected_task(self, task: Task):
        pass

# TODO document
class DatePicker(QtWidgets.QHBoxLayout):
    def __init__(self):
        super().__init__()

        self.selected_date = datetime.now()

        self.year_combo = QtWidgets.QComboBox()   
        self.month_combo = QtWidgets.QComboBox()
        self.day_combo = QtWidgets.QComboBox()

        self.day_combo.currentIndexChanged.connect(self.day_changed)
        self.month_combo.currentIndexChanged.connect(self.month_changed)
        self.year_combo.currentIndexChanged.connect(self.year_changed)

        # initialise combo box items
        self.redraw_combos()

        super().addWidget(self.day_combo)
        super().addWidget(self.month_combo)
        super().addWidget(self.year_combo)
    
    def redraw_combos(self):
        # repopulate year combo
        # * the index changed event needs to be disconnected before the combobox items can be changed
        # * this prevents a recursion loop from hanging the application
        self.year_combo.currentIndexChanged.disconnect()
        self.year_combo.clear()

        # RANGE CHECK: prevents the user from selecting a year that is before the current year
        for year in range(self.selected_date.year, self.selected_date.year + 10):
            self.year_combo.addItem(str(year))
        self.year_combo.setCurrentIndex(0)
        self.year_combo.currentIndexChanged.connect(self.year_changed)

        # repopulate month combo
        self.month_combo.currentIndexChanged.disconnect()
        self.month_combo.clear()

        for month in calendar.month_name[1:]:
            self.month_combo.addItem(month)
        self.month_combo.setCurrentIndex(self.selected_date.month - 1)
        self.month_combo.currentIndexChanged.connect(self.month_changed)

        # repopulate day combo
        self.day_combo.currentIndexChanged.disconnect() 
        self.day_combo.clear()

        # clamp the selected day within the days of the month
        (_, max_day) = calendar.monthrange(self.selected_date.year, self.selected_date.month)
        self.selected_date = self.selected_date = datetime(
            self.selected_date.year, 
            self.selected_date.month, 
            min(self.selected_date.day, max_day)
        )

        print(f"clamped to {max_day} for month {self.selected_date.month}")

        for day in range(1, max_day + 1):
            self.day_combo.addItem(str(day))
        self.day_combo.setCurrentIndex(self.selected_date.day - 1)
        self.day_combo.currentIndexChanged.connect(self.day_changed)

    
    def day_changed(self, index):
        print(f"new day: {index + 1}")
        self.selected_date = datetime(self.selected_date.year, self.selected_date.month, index + 1)
        self.redraw_combos()

    def month_changed(self, index):
        clamped_day = self.get_clamped_day(self.selected_date.year, index + 1)
        self.selected_date = datetime(self.selected_date.year, index + 1, clamped_day)
        self.redraw_combos()

    def year_changed(self, index):
        clamped_day = self.get_clamped_day(int(self.year_combo.currentText()), self.selected_date.month)
        self.selected_date = datetime(int(self.year_combo.currentText()), self.selected_date.month, clamped_day)
        self.redraw_combos()
    
    def get_clamped_day(self, year, month) -> int:
        (_, max_day) = calendar.monthrange(year, month)
        # ensure the day field is within the range of the days of the month
        return min(self.selected_date.day, max_day)

    """
    def update_day_combo(self):

        (_, max_day) = calendar.monthrange(self.selected_date.year, self.selected_date.month)

        #print(f"min({self.day_combo.currentIndex()}, {max_day - 1}")
        new_index = min(self.day_combo.currentIndex(), max_day - 1)

        print(f"cur index: {self.day_combo.currentIndex()}, new month: {self.selected_date.month}, max day: {max_day}, new index: {new_index}")

        self.day_combo.currentIndexChanged.disconnect()

        self.day_combo.clear()
        for day in range(1, max_day):
            self.day_combo.addItem(str(day))
        
        self.day_combo.currentIndexChanged.connect(self.day_changed)

        self.day_combo.setCurrentIndex(new_index)

        print(f"max day: {max_day}")
    """
