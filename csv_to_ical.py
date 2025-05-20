import csv
from datetime import datetime

def csv_to_ical(csv_file, ical_file):
    with open(csv_file, newline='', encoding='utf-8') as infile, \
         open(ical_file, 'w', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        outfile.write("BEGIN:VCALENDAR\n")
        outfile.write("VERSION:2.0\n")
        outfile.write("PRODID:-//Generated from w-hol's nexus-timetable-to-ical on GitHub//CSV to iCal//EN\n")
        outfile.write("CALSCALE:GREGORIAN\n")
        outfile.write("X-WR-CALNAME;VALUE=TEXT:output\n")
        for row in reader:
            # Parse date and time
            dtstart = datetime.strptime(f"{row['Start Date']} {row['Start Time']}", "%d/%m/%Y %H:%M")
            dtend = datetime.strptime(f"{row['End Date']} {row['End Time']}", "%d/%m/%Y %H:%M")
            dtstamp = dtstart.strftime("%Y%m%dT%H%M%S")
            dtstart_str = dtstart.strftime("%Y%m%dT%H%M%S")
            dtend_str = dtend.strftime("%Y%m%dT%H%M%S")
            outfile.write("BEGIN:VEVENT\n")
            outfile.write(f"SUMMARY:{row['Subject']}\n")
            outfile.write(f"DTSTAMP:{dtstamp}\n")
            outfile.write(f"DESCRIPTION:{row['Description']}\n")
            outfile.write(f"DTSTART:{dtstart_str}\n")
            outfile.write(f"DTEND:{dtend_str}\n")
            outfile.write(f"LOCATION:{row['Location']}\n")
            outfile.write("END:VEVENT\n")
        outfile.write("END:VCALENDAR\n")