import csv
import datetime
import os.path
import re
import sys

class Menu:

    def __init__(self):
        self.query = [0, 0, 0, 0, 0]
        self.low_range = '1'
        self.hi_range = '1'
        self.back = 0
        self.selected_entries = {}
        self.home_menu = ["[1]: Add entry",
                "[2]: Lookup entry",
                "[3]: Quit"]
        self.lookup_menu = ["[1]: Find by date",
                  "[2]: Find by time spent",
                  "[3]: Find by exact search",
                  "[4]: Find by pattern",
                  "[5]: Home"]
        self.date_menu = ["[1]: Search within a range",
                "[2]: List all dates",
                "[3]: Home"]
        self.edit_menu = ["[1] Task",
                "[2] Time Spent (in minutes)",
                "[3] Notes",
                "[4] Date",
                "[5] Delete Entry",
                "[6] Back"]


        # with open('log.csv', 'a') as csvfile:
        #     fieldnames = ['task_name', 'time_spent', 'notes', 'date']
        #     logwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

    def main_nav(self, num):
        # Main Navigation
        if num == 0:
            print("Work Log")
            print("Menu:")
            for item in self.home_menu:
                print(item)
            self.home()
        elif num == 1:
            # Main: Add entry
            self.write()
        elif num == 2:
            # Main: Lookup an entry
            for item in self.lookup_menu:
                print(item)
            nav = input(">")
            if nav == '1':
                for item in self.date_menu:
                    print(item)
                nav2 = input(">")
                try:
                    nav = str(5+int(nav2))
                except ValueError:
                    print("That is not a valid menu command.")
                    self.main_nav(num)
            self.search(nav)
        elif num == 3:
            # Main: Quit
            print("Goodbye.")
            sys.exit()

    def home(self):
        nav = input(">")
        if nav == '1':
            self.main_nav(1)
        elif nav == '2':
            self.main_nav(2)
        elif nav == '3':
            self.main_nav(3)
        else:
            print("That is not a valid menu command.")

    def write(self):
        taskstr = input("What is the task name? ")
        timestr = input("How much time did you spend? (in minutes) ")
        notesstr = input("Notes: ")
        time = datetime.datetime.today().strftime("%m/%d/%Y")
        self.submit_entry(taskstr, timestr, notesstr, time)

    def submit_entry(self, taskstr, timestr, notesstr, time):
        file_exists = os.path.isfile('log.csv')
        with open('log.csv', 'a') as csvfile:
            fieldnames = ['task_name', 'time_spent', 'notes', 'date']
            logwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                logwriter.writeheader()

            logwriter.writerow({
                'task_name': taskstr,
                'time_spent': timestr,
                'notes': notesstr,
                'date': time
            })

    def search(self, num):
        date_check = r'\d{2}\/\d{2}\/\d{4}'
        # 1 - Find by date
        if num == '1':
            self.query = input("Please enter the date (mm/dd/yyyy): ")
            self.query = datetime.datetime.strptime(self.query, "%m/%d/%Y")
            self.finder(num)
        # 2 - Find by time spent
        elif num == '2':
            self.query = input("Time Spent: ")
            self.finder(num)
        # 3 - Find by exact string
        elif num == '3':
            self.query = input("Enter your search string: ")
            self.finder(num)
        # 4 - Find by pattern
        elif num == '4':
            self.query = input("Enter your search pattern (regular expression): ")
            self.finder(num)
        # Home
        elif num == '5' or num == '8':
            self.main_nav(0)
        # 6 - Search within a range
        elif num == '6':
            self.low_range = input("Please enter the beginning date (mm/dd/yyyy): ")
            if not re.match(date_check, self.low_range):
                print("Error! input needs to be in the following format: mm/dd/yyyy")
                self.search(num)
            self.hi_range = input("Please enter the end date (mm/dd/yyyy): ")
            if not re.match(date_check, self.hi_range):
                print("Error! input needs to be in the following format: mm/dd/yyyy")
                self.search(num)
            self.low_range = datetime.datetime.strptime(self.low_range, "%m/%d/%Y")
            self.hi_range = datetime.datetime.strptime(self.hi_range, "%m/%d/%Y")
            self.finder(num)
        # 7 - List all dates
        elif num == '7':
            self.finder(num)
        else:
            print("That is not a valid menu command.")

    def finder(self, int):
        self.back = int
        try:
            with open('log.csv', newline='') as csvfile:
                logreader = csv.DictReader(csvfile, delimiter=',')
                rows = list(logreader)
        except FileNotFoundError:
            print("There are no entries.")
            self.main_nav(0)


        if int == '1':      # 1 - Find by date
            n = 1
            for row in rows:
                if self.query == row['date']:
                    print("[{}] {}: {}".format(n, row['date'], row['task_name']))
                    self.selected_entries[n] = row
                    n = n + 1

        elif int == '2':    # 2 - Find by time spent
            n = 1
            for row in rows:
                if self.query == row['time_spent']:
                    print("[{}] {}: {}".format(n, row['time_spent'], row['task_name']))
                    self.selected_entries[n] = row
                    n = n + 1

        elif int == '3':    # 3 - FInd by exact string
            n = 1
            for row in rows:
                if self.query.lower() in row['task_name'].lower() or self.query.lower() in row['notes'].lower():
                    print("[{}] {}: {}".format(n, row['task_name'], row['notes']))
                    self.selected_entries[n] = row
                    n = n + 1

        elif int == '4':    # 4 - Find by pattern
            n = 1
            regex_query = r'{}'.format(self.query)
            for row in rows:
                if re.search(regex_query, row['task_name']) is not None or re.search(regex_query, row['notes']) is not None:
                    print("[{}] {}: {}".format(n, row['task_name'], row['notes']))
                    self.selected_entries[n] = row
                    n += 1

        elif int == '6':    # 6 - Search within a range
            n = 1
            for row in rows:
                date = datetime.datetime.strptime(row['date'], "%m/%d/%Y")
                if self.low_range <= date and date <= self.hi_range:
                    print("[{}] {}: {}".format(n, row['date'], row['task_name']))
                    self.selected_entries[n] = row
                    n = n + 1

        elif int == '7':    # 7 - List all dates
            n = 1
            for row in rows:
                print("[{}] {}: {}".format(n, row['date'], row['task_name']))
                self.selected_entries[n] = row
                n = n + 1
        else:
            print("That is not a valid menu command.")

        print("[0] Return Home")
        nav = input("Please select an entry: ")
        while not nav:
            print("Please enter a valid command")
            nav = input("Please select an entry: ")
        self.presenter(nav)

    def presenter(self, num):
        var = int(num)
        if var == 0:
            self.main_nav(0)
        try:
            self.formatter(self.selected_entries[var])
        except KeyError:
            self.main_nav(0)
        try:
            # If it's the first entry, do not display [P]
            self.selected_entries[var-1]
            print("[P] - Previous")
        except KeyError:
            pass
        try:
            # If it's the last entry, do not display [N]
            self.selected_entries[var+1]
            print("[N] - Next")
        except KeyError:
            pass
        print("[E] - Edit")
        print("[H] - Home")

        nav = input(">")
        if nav.upper() == 'E':
            try:
                self.editor(self.selected_entries[var])
            except KeyError:
                self.main_nav(0)
        elif nav.upper() == 'N':
            try:
                self.selected_entries[var+1]
            except KeyError:
                print("This is the last item")
                self.presenter(var)
            choice = var + 1
            self.presenter(choice)
        elif nav.upper() == 'P':
            try:
                self.selected_entries[var-1]
            except KeyError:
                print("This is the first item")
                self.presenter(var)
            choice = var - 1
            self.presenter(choice)
        elif nav.upper == 'H':
            self.main_nav(0)
        else:
            print("That is not a valid menu command.")

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
        with open('log.csv', newline='') as csvfile:
            logreader = csv.DictReader(csvfile, delimiter=',')
            rows = list(logreader)

            all_entries = {}
            i = 0
            for row in rows:
                all_entries[i] = row
                i += 1

        for k, v in all_entries.items():
            if v == dict:
                key_var = k

        del all_entries[key_var]

        #edit here
        for item in self.edit_menu:
            print(item)
        nav = input(">")

        if nav == '1':
            print("Task: {}".format(dict['task_name']))
            taskstr = input("New task name: ")
            timestr = dict['time_spent']
            notesstr = dict['notes']
            time = dict['date']
        elif nav == '2':
            print("Time Spent (in minutes): {}".format(dict['time_spent']))
            timestr = input("New time spent (in minutes): ")
            taskstr = dict['task_name']
            notesstr = dict['notes']
            time = dict['date']
        elif nav == '3':
            print("Notes: {}".format(dict['notes']))
            notesstr = input("New notes: ")
            taskstr = dict['task_name']
            timestr = dict['time_spent']
            time = dict['date']
        elif nav == '4':
            print("Date: {}".format(dict['date']))
            time = input("New date (mm/dd/yyyy): ")
            time = datetime.datetime.strptime(time, "%m/%d/%Y")
            time = datetime.datetime.strftime(time, "%m/%d/%Y")
            taskstr = dict['task_name']
            timestr = dict['time_spent']
            notesstr = dict['notes']
        elif nav == '5':
            pass
        elif nav == '6':
            self.finder(self.back)
        else:
            print("Invalid option, please try again.")
            self.presenter(self.selected_entries[0])

        file_exists = os.path.isfile('output.csv')
        with open('output.csv', 'w') as csvfile:
            fieldnames = ['task_name', 'time_spent', 'notes', 'date']
            logwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

            logwriter.writeheader()

            for item in all_entries:
                logwriter.writerow({
                    'task_name': all_entries[item]['task_name'],
                    'time_spent': all_entries[item]['time_spent'],
                    'notes': all_entries[item]['notes'],
                    'date': all_entries[item]['date']
                })
            if nav != '5':
                logwriter.writerow({
                    'task_name': taskstr,
                    'time_spent': timestr,
                    'notes': notesstr,
                    'date': time
                })

        os.remove('log.csv')
        os.rename('output.csv', 'log.csv')
