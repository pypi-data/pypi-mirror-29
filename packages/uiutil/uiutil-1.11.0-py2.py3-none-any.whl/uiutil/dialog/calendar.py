# encoding: utf-8

from tkinter.simpledialog import SimpleDialog
from ..ttk_override.ttk_calendar import Calendar

# Source: https://github.com/moshekaplan/tkinter_components/tree/master/CalendarDialog


class CalendarDialog(SimpleDialog):
    """Dialog box that displays a calendar and returns the selected date"""

    def body(self, master):
        self.calendar = Calendar(master)
        self.calendar.pack()

    def apply(self):
        self.result = self.calendar.selection
