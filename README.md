# nexus-timetable-to-ical
This is a tool that converts the Nexus timetable into a `.isc` file, then imports it into Apple iCalendar. 

Current features:
- Converting events from `.csv` to `.ics`
- Renaming subjects
- Including/excluding subjects
- Choose only classes from a week/term time period (eg. term 2 week 3 - 4)

# Usage
## Downloading and converting events
### Part 1
1. Navigate to the "calendar" tab from the top
2. Click export
3. Select "Timetable classes" then "Download CSV"
4. Save the file somewhere you will remember it
   
### Part 2
1. Download the latest release from the repository
2. Ensure `main.py` and `csv_to_ical.py` are in the same directory
3. Run `main.py`
   
### Part 3

Once your `.isc` file is generated, you have three options for how to import it into iCalendar:

### Alternative to Part 2
#### Organising events
In the case that you cannot/don't want to run the Python script, RegEx (regular expression) can be used to format the `.csv` file.
Note that this method doesn't have as much customisability as the script, and will not recieve updates or new features.
*You will need a text editor or program capable of running RegEx find and replace searches*
Run the following find and replace operation:

> Find: `^(\d\d)/(\d\d)/(\d{4}),(\d\d:\d\d),(\d\d)/(\d\d)/(\d{4}),(\d\d:\d\d),(\d),"(.*) 08 \((.*)\)",.*,(.*),.*,.*,.*`
> 
> Replace: `"$10",$2/$1/$3,$4,$6/$5/$7,$8,$9,$11,$12`

If you want to change the names of specific subjects like the script, run an operation like this:

> Find: `Health and Physical Education`
>
> Replace: `HPE`

This will replace the subject named `Health and Physical Education` with `HPE`, no extra formatting is needed

Replace the first line (header line) with:

> `Subject,Start Date,Start Time,End Date,End Time,All Day,Description,Location`

#### Converting events
Go to [this link](https://csv-to-ical.chimbori.com) and convert the `.csv` file, then download the `.ics` file.
Note that for this converter to work, the dates must be in mm/dd/yyyy format, which is covered by the RegEx string.
The Python script has a commented section that converts the date format to US format. This will break the `.ics` file, but the `.csv` file will be usable in the online converter.

## Importing events
### Method 1: Shortcut method

1. Get the `Import ICal File` shortcut from [RoutineHub](https://routinehub.co/shortcut/5773/). The website may ask you to log in, but you can just tap off popup and tap `Get Shortcut` again. If it still doesn't, download the shortcut directly from the bottom of the page.
2. Run the shortcut and select your `.ics` file
3. Click on "Add All" and choose a calendar from the popup (recommended to make a new one for timetable events only)

### Method 2: Email method

*You will need to have Apple's "Mail" app installed on your device.*
1. Email the `.ics` file to an account that you are logged in to in the Mail app (doesn't have to be iCloud)
2. Click on the attachment in the email from the Mail app and click "Add All"
3. Choose a calendar from the popup (recommended to make a new one for timetable events only)

### Method 3: Mac method

I don't have a Mac, meaning I can't actually test it, but I assume it will work anyway, since there is an [Apple Help article](https://support.apple.com/en-au/guide/calendar/icl1023/mac) on it. Scroll down to the section titled *Import events from a calendar file.*

# Development

This is still a project in the works, and is still rough around the edges. Eventually I plan to make a GitHub page, meaning you don't have to run a Python script, which can be inconvenient for iOS users. Forks and pull requests are welcome.

###### [Shortcut](https://www.icloud.com/shortcuts/1326eea828f34d4297003a07e361f5cf)
