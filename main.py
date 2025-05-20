import csv
import re
from datetime import datetime, timedelta
from csv_to_ical import csv_to_ical

# Prompts the user for a valid integer in a specified range until one is provided.
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

print("This script converts CSV files to ICS format.")
# Required for finding classes properly
year_level = str(inputInRangeLoop("Enter your year level (7 - 12):\n> ", 7, 12)).zfill(2)

# Ask for term and week range
term_num = inputInRangeLoop("Enter the term number (1-4):\n> ", 1, 4)

if input("Do you want to include all events? (y/n)\n> ").lower() == 'n':
    week_start_num = inputInRangeLoop("Enter the START week number (1 - 10):\n> ", 1, 10)
    week_end_num = inputInRangeLoop(f"Enter the END week number ({week_start_num} - 10):\n> ", week_start_num, 10)
else:
    week_start_num = 1
    week_end_num = 10

# Define term start dates
term_starts = {
    1: datetime(2025, 2, 3),
    2: datetime(2025, 4, 28),
    3: datetime(2025, 7, 21),
    4: datetime(2025, 10, 13)
}
term_start = term_starts[term_num]
# Calculate the dates
date_range_start = term_start + timedelta(weeks=week_start_num - 1)
date_range_end = term_start + timedelta(weeks=week_end_num - 1, days=4)  # 5-day week

if week_start_num == 1 and week_end_num == 10:
    print(f"You chose term {term_num}, all weeks, which is from {date_range_start.strftime('%d/%m/%Y')} to {date_range_end.strftime('%d/%m/%Y')}")
elif week_start_num == week_end_num:
    print(f"You chose term {term_num}, week {week_start_num}, which is from {date_range_start.strftime('%d/%m/%Y')} to {date_range_end.strftime('%d/%m/%Y')}")
else:
    print(f"You chose term {term_num}, weeks {week_start_num} to {week_end_num}, which is from {date_range_start.strftime('%d/%m/%Y')} to {date_range_end.strftime('%d/%m/%Y')}")

# Read the CSV and get all unique subjects
subjects_set = set()
with open('input.csv', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    next(reader)  # Skip header
    for row in reader:
        name_field = row[5]
        match = re.match(rf'(.*?) {year_level}', name_field)
        if match:
            subjects_set.add(match.group(1).strip()) # A set is used because it will ignore dupplicates
subjects_list = sorted(subjects_set) # Converts set to a list for proper usage

# Causes errors if not defined
mode = 'e'
selected_subjects = set()

# Excluding subjects
if input("Do you want to exclude or include specific subjects? (y/n)\n> ").lower() == 'y':
    # Ask for inclusion/exclusion mode
    mode = input("\nType 'e' to EXCLUDE or 'i' to INCLUDE the selected subjects:\n> ").strip().lower()
    if mode not in ('e', 'i'):
        mode = 'e'

    # Print all subjects
    print("Subjects found in your timetable:")
    for idx, subj in enumerate(subjects_list, 1):
        print(f"{idx}. {subj}")

    # Ask for input
    selection_input = input(f"\nEnter the numbers of subjects to {'EXCLUDE' if mode == 'e' else 'INCLUDE'}, separated by spaces (or leave blank for none):\n> ")
    selection_indices = {int(x.strip()) for x in selection_input.split() if x.strip().isdigit()}
    selected_subjects = {subjects_list[i-1] for i in selection_indices if 1 <= i <= len (subjects_list)}

    # if selected_subjects:
    #     print(f"\n{'Excluded' if mode == 'e' else 'Included'} subjects: {', '.join(selected_subjects)}")

# Renaming subjects
rename_map = {subj: subj for subj in subjects_list}
if input("Do you want to rename any subjects? (y/n)\n> ").lower() == 'y':
    print("\nSubjects found in your timetable:")
    for idx, subj in enumerate(subjects_list, 1):
        print(f"{idx}. {subj}")
    
    while True:
        num = input("Enter the number of the subject you want to rename, or press Enter to finish:\n> ")
        if not num.strip(): # Makes "press enter to finish" work
            print("Finished renaming subjects.")
            break
        if num.isdigit() and 1 <= int(num) <= len(subjects_list):
            idx = int(num) - 1
            while True:
                new_name = input(f"Enter new name for '{subjects_list[idx]}':\n> ")
                if new_name.strip():
                    rename_map[subjects_list[idx]] = new_name.strip()
                    print(f"Renamed '{subjects_list[idx]}' to '{new_name.strip()}'")
                    break
                else: print("Name cannot be empty.")
        else: print("Invalid number, try again.")

# Writing the new CSV
with open('input.csv', newline='', encoding='utf-8') as infile, \
     open('output.csv', 'w', newline='', encoding='utf-8') as outfile: 
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    next(reader)  # Skip the old header row
    writer.writerow(["Subject", "Start Date", "Start Time", "End Date", "End Time", "All Day", "Description", "Location"]) # Write new header
    for row in reader:
        start_date_field = row[0]
        event_date = datetime.strptime(start_date_field, "%d/%m/%Y")
        # Only include events in the selected week range
        if not (date_range_start <= event_date <= date_range_end):
            continue

        # Extracts the subject and "class code" from the name field
        # Formatted: "[subject] [year level] ([class code])"
        # Example: "English 09 (09Eng_S2_6)"
        name_field = row[5]
        match = re.match(rf'(.*?) {year_level} \((.*?)\)', name_field)
        if not match:
            continue
        subject = match.group(1).strip()
        description = match.group(2)

        # Use renamed subject if provided
        subject = rename_map.get(subject, subject)

        # Filter subjects
        if (mode == 'e' and subject in selected_subjects) or (mode == 'i' and subject not in selected_subjects):
            continue
        
        # Unused - Convert date format from dd/mm/yyyy to mm/dd/yyyy
        # match = re.match(r'(\d{2})/(\d{2})/(\d{4})', start_date_field)
        # us_start_date = f"{match.group(2)}/{match.group(1)}/{match.group(3)}"
        
        # finish_date_field = row[2]
        # match = re.match(r'(\d{2})/(\d{2})/(\d{4})', finish_date_field)
        # us_end_date = f"{match.group(2)}/{match.group(1)}/{match.group(3)}"

        writer.writerow([
            subject,
            row[0],  # Start Date
            row[1],  # Start Time
            row[2],  # End Date
            row[3],  # End Time
            row[4],  # All Day
            description, # Description
            row[7]   # Location
        ])
        
# Convert CSV to iCal format (ICS)
csv_to_ical("output.csv", "output.ics")
print("ICS file created as output.ics")