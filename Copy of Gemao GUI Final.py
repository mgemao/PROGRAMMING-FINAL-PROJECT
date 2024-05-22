import calendar
import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class EventManager:
    def __init__(self):
        self.events = {}

    def add_event(self, date, event):
        self.events[date] = event

    def delete_event(self, date):
        if date in self.events:
            del self.events[date]

    def get_events_for_month(self, year, month):
        return {date: event for date, event in self.events.items() if datetime.datetime.strptime(date, "%Y-%m-%d").month == month and datetime.datetime.strptime(date, "%Y-%m-%d").year == year}

class CalendarApp:
    def __init__(self, master, event_manager):
        self.master = master
        self.event_manager = event_manager

        self.master.title("GUI Calendar")
        self.master.geometry("400x500")
        self.master.configure(bg='#f0f0f0')

        self.create_widgets()

    def create_widgets(self):
        self.input_frame = ttk.Frame(self.master, padding="20", relief="raised", borderwidth=2)
        self.input_frame.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.year_label = ttk.Label(self.input_frame, text="Year:")
        self.year_label.grid(row=0, column=0, sticky="e")
        self.year_entry = ttk.Entry(self.input_frame, width=10)
        self.year_entry.grid(row=0, column=1, padx=5, sticky="w")

        self.month_label = ttk.Label(self.input_frame, text="Month:")
        self.month_label.grid(row=1, column=0, sticky="e")
        self.month_combobox = ttk.Combobox(self.input_frame, values=list(calendar.month_name[1:]), state="readonly")
        self.month_combobox.current(0)
        self.month_combobox.grid(row=1, column=1, padx=5, sticky="w")

        self.day_label = ttk.Label(self.input_frame, text="Day:")
        self.day_label.grid(row=2, column=0, sticky="e")
        self.day_entry = ttk.Entry(self.input_frame, width=10)
        self.day_entry.grid(row=2, column=1, padx=5, sticky="w")

        self.event_label = ttk.Label(self.input_frame, text="Event:")
        self.event_label.grid(row=3, column=0, sticky="e")
        self.event_entry = ttk.Entry(self.input_frame, width=20)
        self.event_entry.grid(row=3, column=1, padx=5, sticky="w")

        self.button_frame = ttk.Frame(self.master)
        self.button_frame.grid(row=1, column=0, padx=20, pady=(0, 20))

        self.show_button = ttk.Button(self.button_frame, text="Show Calendar", command=self.show_calendar)
        self.show_button.grid(row=0, column=0, padx=5, sticky="ew")

        self.add_button = ttk.Button(self.button_frame, text="Add Event", command=self.add_event)
        self.add_button.grid(row=0, column=1, padx=5, sticky="ew")

        self.output_frame = ttk.Frame(self.master, padding="20", relief="sunken", borderwidth=2)
        self.output_frame.grid(row=2, column=0, padx=20, pady=(0, 20))

        self.output_text = tk.Text(self.output_frame, height=10, width=25)
        self.output_text.grid(row=0, column=0, sticky="nsew")

    def show_calendar(self):
        try:
            year = int(self.year_entry.get())
            month = self.month_combobox.current() + 1
            cal = calendar.month(year, month)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, cal)
            self.display_events(year, month)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid year and month.")

    def display_events(self, year, month):
        month_events = self.event_manager.get_events_for_month(year, month)
        if month_events:
            event_notification = "\n\nUpcoming Events:\n"
            for date, event in month_events.items():
                year, month, day = map(int, date.split('-'))
                event_notification += f"{calendar.day_name[datetime.date(year, month, day).weekday()]} {date}: {event}\n"
            self.output_text.insert(tk.END, event_notification)

    def add_event(self):
        try:
            year = int(self.year_entry.get())
            month = self.month_combobox.current() + 1
            day = int(self.day_entry.get())
            date = datetime.date(year, month, day)
            event = self.event_entry.get().strip()
            if event:
                self.event_manager.add_event(date.strftime("%Y-%m-%d"), event)
                messagebox.showinfo("Success", "Event added successfully.")
            else:
                messagebox.showerror("Error", "Event cannot be empty.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input for date.")

if __name__ == "__main__":
    root = tk.Tk()

    event_manager = EventManager()

    app = CalendarApp(root, event_manager)

    root.mainloop()
