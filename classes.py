import collections
import csv
import datetime
import sys

class Menu:

    def __init__(self):
        self.query = [0, 0, 0, 0, 0]
        self.low_range = 0
        self.hi_range = 0
        self.selected_entries = {}
        self.previous_menu = 0
        self.prompts = {
            "Home": {"[1]": "Add entry",
                     "[2]": "Lookup entry",
                     "[3]": "Quit"},
            "Lookup": {"[1]": "Find by date",
                       "[2]": "Find by time spent",
                       "[3]": "Find by exact search",
                       "[4]": "Find by pattern"},
            "date": {"[1]": "Search within a range",
                     "[2]": "List all dates"}
            }




        with open('log.csv', 'a') as csvfile:
            fieldnames = ['task_name', 'time_spent', 'notes', 'date']
            logwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

    def main_nav(self, num):
        # Navigation handler for in between methods
        if num == "0":
            print("Work Log")
            print("Menu:")
            print("\n")
            for k,v in self.prompts["Home"]:
                print("{}: {}".format(k, v))
            self.home()
        elif num == "1":
            # Main: Add entry
            self.write()
        elif num == "2":
            # Main: Lookup an entry
            for k,v in self.prompts["Lookup"]:
                print("{}: {}".format(k, v))
            nav = input(">")
            if nav == '1':
                for k,v in self.prompts["date"]:
                    print("{}: {}".format(k, v))
                nav2 = input(">")
                nav = str(int(nav)+int(nav2))
            self.search(nav)
        elif num == "3":
            # Main: Quit
            print("Goodbye.")
            sys.exit()
        elif num == 2.1:
            pass
            # Find by date
            # Find by time spent
            # Find by exact search
            # Find by pattern

    def home(self):
        nav = input(">")

        if nav == "1":
            self.main_nav(1)
        elif nav == "2":
            self.main_nav(2)
        elif nav == "3":
            self.main_nav(3)
        else:
            print("That is not a valid menu command.")

    def write(self):
        taskstr = input("What is the task name? ")
        timestr = input("How much time did you spend? (in minutes) ")
        notesstr = input("Notes: ")
        time = datetime.datetime.today().strftime("%Y-%m-%d")
        self.submit_entry(taskstr, timestr, notesstr, time)

    def submit_entry(self, taskstr, timestr, notesstr, time):
        with open('log.csv', 'a') as csvfile:
            fieldnames = ['task_name', 'time_spent', 'notes', 'date']
            logwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

            logwriter.writeheader()
            logwriter.writerow({
                'task_name': taskstr,
                'time_spent': timestr,
                'notes': notesstr,
                'date': time
            })

    def search(self, num):
        if num == 1.1:
            self.low_range = input("Please enter the beginning date (mm/dd/yyyy): ")
            self.hi_range = input("Please enter the end date (mm/dd/yyyy): ")
            self.low_range = datetime.datetime.strptime(self.low_range, "%m/%d/%Y")
            self.hi_range = datetime.datetime.strptime(self.hi_range, "%m/%d/%Y")
        elif num == "2":
            self.finder(12)
            self.finder(nav)
        elif int == '2':
            # Sort by time spent (list)
            self.query = input("Time Spent: ")
            self.finder(int)
        elif int == '3':
            # Find by exact search
            self.query = input("Enter your search string: ")
            self.finder(int)
            pass
        elif int == '4':
            # Find by pattern
            self.query = input("Enter your search pattern: ")
            self.finder(int)
            pass
        else:
            print("That is not a valid menu command.")

    def finder(self, int):
        with open('log.csv', newline='') as csvfile:
            logreader = csv.DictReader(csvfile, delimiter=',')
            rows = list(logreader)


        if int == '1':
            # Sort by range
            n = 1
            for row in rows:
                date = datetime.datetime.strptime(row['date'], "%Y-%m-%d")
                if self.low_range < date and date < self.hi_range:
                    print("[{}] {}: {}".format(n, row['date'], row['task_name']))
                    self.selected_entries[n] = row
                    n = n + 1

            nav = input("Please select an entry: ")
            self.presenter(nav)
        elif int == 12:
            # Print all dates
            n = 1
            for row in rows:
                print("[{}] {}: {}".format(n, row['date'], row['task_name']))
                self.selected_entries[n] = row
                n = n + 1
            nav = input("Please select an entry: ")
            self.presenter(nav)
        elif int == '2':
            # Sort by time spent
            for row in rows:
                if self.query == row['time_spent']:
                    print("[{}] {}: {}".format(n, row['time_spent'], row['task_name']))
                    self.selected_entries[n] = row
                    n = n + 1
            nav = input(">")
            self.presenter(nav)
        elif int == '3':
            # Sort by exact search
            pass
        elif int == '4':
            # Find by pattern
            pass

    def presenter(self, choice):
        var = int(choice)
        self.formatter(self.selected_entries[var])
        try:
            self.selected_entries[var-1]
            print("[P] - Previous")
        except KeyError:
            pass
        try:
            self.selected_entries[var+1]
            print("[N] - Next")
        except KeyError:
            pass
        print("[E] - Edit")
        print("[B] - Back")

        nav = input(">")
        if nav.upper() == 'E':
            self.editor(self.selected_entries[var])
        elif nav.upper() == 'N':
            choice = var + 1
            self.presenter(choice)
        elif nav.upper() == 'P':
            choice = var - 1
            self.presenter(choice)
        elif nav.upper == 'B':
            pass

    def formatter(self, dict):
        print(
            """
            Task: {}
            Time Spent (in minutes): {}
            Notes: {}
            Date: {}
            """.format(dict['task_name'], dict['time_spent'], dict['notes'], dict['date'])
        )

    def editor(self, dict):
        logreader = csv.reader(open('log.csv', 'r'))
        row = list(logreader)
        # logwriter = csv.writer(open('logout.csv', 'wb'))
        with open('log.csv', 'a') as csvfile:
            fieldnames = ['task_name', 'time_spent', 'notes', 'date']
            logwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)


        option = 0
        while option != 5:
            print("Which would you like to edit?")
            print("[1] Task")
            print("[2] Time Spent (in minutes)")
            print("[3] Notes")
            print("[4] Date")
            print("[5] Quit")
            option = input(">")
            if option == '1':
                # Task
                print("Task: {}".format(dict['task_name']))
                new = input("New Task: ")
                dict['task_name'] = new
                for row in logreader:
                    if row == dict:
                        logwriter.writerow([dict['task_name'], row['time_spent'], row['notes'], row['date']])
            elif option == '2':
                # Time Spent
                print("Time Spent: {}".format(dict['time_spent']))
                new = input("New Time Spent: ")
                for row in logreader:
                    if row == dict:
                        logwriter.writerow([row['task_name'], new, row['notes'], row['date']])
            elif option == '3':
                # Notes
                print("Notes: {}".format(dict['notes']))
                new = input("New Notes: ")
                for row in logreader:
                    if row == dict:
                        logwriter.writerow([row['task_name'], row['time_spent'], new, row['date']])
            elif option == '4':
                # Date
                print("Date: {}".format(dict['date']))
                new = input("New Date (mm/dd/yyyy): ")
                new = datetime.datetime.strptime(new, "%m/%d/%Y")
                for row in logreader:
                    if row == dict:
                        logwriter.writerow([row['task_name'], row['time_spent'], row['notes'], new])
            elif option == '5':
                break
            else:
                print("Invalid option, please try again.")
        self.finder(12)
