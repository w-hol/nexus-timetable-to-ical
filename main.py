import csv
import re
from datetime import datetime, timedelta
from sys import platform
import json

# Constants
TERM_STARTS = {
    1: datetime(2025, 2, 3),
    2: datetime(2025, 4, 28),
    3: datetime(2025, 7, 21),
    4: datetime(2025, 10, 13)
}
prefs = {
    "year_level": int,
    "term_number": int,
    "exclude_or_include_mode": "e" or "i",
    "selected_subjects": set(),
    "rename_map": {}
}

# File picker for CSV
try:
    with open('calendar.csv', 'r', encoding='utf-8') as f:
        CSV_PATH = 'calendar.csv'
except FileNotFoundError:
    if platform == "win32":
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        CSV_PATH = filedialog.askopenfilename(
            title="Select your CSV file",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if not CSV_PATH:
            print("No file selected. Exiting.")
            exit(1)
    elif platform == "ios":
        from file_system import import_file
        try:
            CSV_PATH = import_file(file_extension=["csv"])
        except Exception as e:
            print(f"Error selecting file: {e}")
            exit(1)

def inputInRangeLoop(prompt, min_val, max_val):
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid, try again.")

def load_preferences():
    while True:
        x = input("Do you want to load preferences from file? (y/n)\n> ").lower()
        if x == 'y':
            try:
                with open('prefs.json', 'r', encoding='utf-8') as f:
                    PREFS_PATH = 'prefs.json'
                    print("Loading preferences from prefs.json")
                    break
            except FileNotFoundError:
                if platform == "win32":
                    import tkinter as tk
                    from tkinter import filedialog
                    root = tk.Tk()
                    root.withdraw()
                    PREFS_PATH = filedialog.askopenfilename(
                        title="Select your preferences file",
                        filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
                    )
                    if PREFS_PATH:
                        print(f"Loading preferences from {PREFS_PATH}")
                        break
                    else:
                        print("No file selected. Exiting.")
                        exit(1)
                elif platform == "ios":
                    from file_system import import_file
                    try:
                        PREFS_PATH = import_file(file_extension=["json"])
                        print(f"Loading preferences from {PREFS_PATH}")
                        break
                    except Exception as e:
                        print(f"Error selecting file: {e}")
                        exit(1)
        elif x == 'n':
            PREFS_PATH = None
            break
        else:
            print("Invalid input, try again.")
    try:
        with open(PREFS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def get_week_range():
    start_week = inputInRangeLoop("Enter the START week number (1 - 10):\n> ", 1, 10)
    end_week = inputInRangeLoop(f"Enter the END week number ({start_week} - 10):\n> ", start_week, 10)
    return start_week, end_week

def get_user_inputs():
    # Prompts the user for a valid integer in a specified range until one is provided.


    print("This script converts CSV files to ICS format.")
    # Required for finding classes properly
    year_level = str(inputInRangeLoop("Enter your year level (7 - 12):\n> ", 7, 12)).   zfill(2)
    prefs["year_level"] = year_level

    # Ask for term and week range
    term_num = inputInRangeLoop("Enter the term number (1-4):\n> ", 1, 4)
    prefs["term_number"] = term_num

    if input("Do you want to include all events? (y/n)\n> ").lower() == 'n':
        week_start_num = inputInRangeLoop("Enter the START week number (1 - 10):\n>     ", 1, 10)
        week_end_num = inputInRangeLoop(f"Enter the END week number ({week_start_num}   - 10):\n> ", week_start_num, 10)
    else:
        week_start_num = 1
        week_end_num = 10

    term_start = TERM_STARTS[term_num]
    # Calculate the dates
    date_range_start = term_start + timedelta(weeks=week_start_num - 1)
    date_range_end = term_start + timedelta(weeks=week_end_num - 1, days=4)  # 5-day    week

    if week_start_num == 1 and week_end_num == 10:
        print(f"You chose term {term_num}, all weeks, which is from {date_range_start.strftime('%d/%m/%Y')} to {date_range_end.strftime('%d/%m/%Y')}")
    elif week_start_num == week_end_num:
        print(f"You chose term {term_num}, week {week_start_num}, which is from {date_range_start.strftime('%d/%m/%Y')} to {date_range_end.strftime('%d/%m/%Y')}")
    else:
        print(f"You chose term {term_num}, weeks {week_start_num} to {week_end_num}, which is from {date_range_start.strftime('%d/%m/%Y')} to {date_range_end.strftime('%d/%m/%Y')}")

    # Read the CSV and get all unique subjects
    subjects_set = set()
    with open(CSV_PATH, newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        next(reader)  # Skip header
        for row in reader:
            name_field = row[5]
            match = re.match(rf'(.*?) {year_level}', name_field)
            if match:
                subjects_set.add(match.group(1).strip()) # A set is used because it     will ignore duplicates
    subjects_list = sorted(subjects_set) # Converts set to a list for proper usage

    # Causes errors if not defined
    mode = 'e'
    selected_subjects = []

    # Excluding subjects
    if input("Do you want to exclude or include specific subjects? (y/n)\n> ").lower    () == 'y':
        # Ask for inclusion/exclusion mode
        mode = input("Type 'e' to EXCLUDE or 'i' to INCLUDE the selected subjects:\n>   ").strip().lower()
        if mode not in ('e', 'i'):
            mode = 'e'
        prefs["exclude_or_include_mode"] = mode

        # Print all subjects
        print("Subjects found in your timetable:")
        for idx, subj in enumerate(subjects_list, 1):
            print(f"{idx}. {subj}")

        # Ask for input
        selection_indices = []
        while True:
            num = input(f"Enter the number of the subject you want to {'EXCLUDE' if     mode == 'e' else 'INCLUDE'}, or press Enter to finish:\n> ")
            if not num.strip(): # Makes "press enter to finish" work
                print(f"Finished {'EXCLUDING' if mode == 'e' else 'INCLUDING'}  subjects.")
                break
            if num.isdigit() and 1 <= int(num) <= len(subjects_list):
                selection_indices.append(int(num))
                print(f"{'EXCLUDED' if mode == 'e' else 'INCLUDED'} {subjects_list[int  (num)-1]}.")
            else: print("Invalid number, try again.")
        for i in selection_indices:
            selected_subjects.append(subjects_list[i-1])
        if mode == 'e': subjects_list = [subj for subj in subjects_list if subj not     in selected_subjects]
        elif mode == 'i': subjects_list = [subj for subj in subjects_list if subj in    selected_subjects]

        prefs["selected_subjects"] = selected_subjects

    # Renaming subjects
    rename_map = {}
    if input("Do you want to rename any subjects? (y/n)\n> ").lower() == 'y':
        while True:
            print("\nSubjects found in your timetable:")
            for idx, subj in enumerate(subjects_list, 1): print(f"{idx}. {subj}")
            num = input("Enter the number of the subject you want to rename, or press   Enter to finish:\n> ")
            if not num.strip(): # Makes "press enter to finish" work
                print("Finished renaming subjects.")
                break
            if num.isdigit() and 1 <= int(num) <= len(subjects_list):
                idx = int(num) - 1
                while True:
                    new_name = input(f"Enter new name for '{subjects_list[idx]}':\n>    ")
                    if new_name.strip():
                        rename_map[subjects_list[idx]] = new_name.strip()
                        print(f"Renamed '{subjects_list[idx]}' to '{new_name.strip()}   '")
                        break
                    else: print("Name cannot be empty.")
            else: print("Invalid number, try again.")
        prefs["rename_map"] = rename_map

def write_ics_file():
    # Write ICS file directly, skipping output.csv
    with open(CSV_PATH, newline='', encoding='utf-8') as infile, open('output.ics', 'w', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        next(reader)  # Skip header
        outfile.write("BEGIN:VCALENDAR\n")
        outfile.write("VERSION:2.0\n")
        outfile.write("PRODID:-//Generated from w-hol's nexus-timetable-to-ical on  GitHub//CSV to iCal//EN\n")
        outfile.write("CALSCALE:GREGORIAN\n")
        outfile.write("X-WR-CALNAME;VALUE=TEXT:output\n")
        for row in reader:
            start_date_field = row[0]
            event_date = datetime.strptime(start_date_field, "%d/%m/%Y")
            # Only include events in the selected week range
            if not (date_range_start <= event_date <= date_range_end):
                continue

            # Extract subject and class code
            name_field = row[5]
            match = re.match(rf'(.*?) {year_level} \((.*?)\)', name_field)
            if not match:
                continue
            subject = match.group(1).strip()
            description = match.group(2)

            # Use renamed subject if provided
            subject = rename_map.get(subject, subject)

            # Filter subjects
            if (mode == 'e' and subject in selected_subjects) or (mode == 'i' and   subject not in selected_subjects):
                continue

            # Parse date and time for ICS
            try:
                dtstart = datetime.strptime(f"{row[0]} {row[1]}", "%d/%m/%Y %H:%M")
                dtend = datetime.strptime(f"{row[2]} {row[3]}", "%d/%m/%Y %H:%M")
            except Exception as e:
                print(f"Skipping row due to date/time parse error: {e}")
                continue
            dtstamp = dtstart.strftime("%Y%m%dT%H%M%S")
            dtstart_str = dtstart.strftime("%Y%m%dT%H%M%S")
            dtend_str = dtend.strftime("%Y%m%dT%H%M%S")

            outfile.write("BEGIN:VEVENT\n")
            outfile.write(f"SUMMARY:{subject}\n")
            outfile.write(f"DTSTAMP:{dtstamp}\n")
            outfile.write(f"DESCRIPTION:{description}\n")
            outfile.write(f"DTSTART:{dtstart_str}\n")
            outfile.write(f"DTEND:{dtend_str}\n")
            outfile.write(f"LOCATION:{row[7]}\n")
            outfile.write("END:VEVENT\n")
        outfile.write("END:VCALENDAR\n")
    print("ICS file created as output.ics")

def save_preferences():
    if input("Would you like to save your preferences to file? (y/n)\n> ").lower() == 'y':
        s = list(prefs["selected_subjects"])
        prefs["selected_subjects"] = s
        with open("prefs.json", "w") as f:
            f.write(json.dumps(prefs, indent=4))

def main():
    prefs = load_preferences()
    if prefs:
        print("Loaded preferences from prefs.json.")
        # Use prefs to set variables, skip input prompts
    else:
        prefs = get_user_inputs()
        save_preferences()
    write_ics_file()

if __name__ == "__main__":
    main()