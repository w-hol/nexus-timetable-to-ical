# Nexus Timetable to iCal

Converts your Nexus timetable into an iCalendar file you can import into Outlook or Apple Calendar.

Everything runs locally on your browser, so I can't see your data, and you don't have to download any software

## How to use it

1. Open [the site](https://w-hol.github.io/nexus-timetable-to-ical/)
2. Export your timetable from Nexus (Calendar tab → Export → Timetable Classes → Download CSV)
3. Upload the CSV file
4. Pick which dates you want to include using the calendar
5. Customize event names if you want
6. Download the `.ics` file
7. Import it into your calendar app (see below)

## Features

- Visual calendar for selecting date ranges
- Custom event names (or just use the default class names)
- Shows term weeks (T3W5 etc) on the calendar
- All processing happens locally - your data stays on your device

## Importing into your calendar

### Outlook (Mac)
1. Make sure you're in legacy mode (File → Legacy Outlook)
2. Click the calendar icon in the bottom left
3. Drag the `.ics` file into the calendar

### Outlook (Windows)
1. Click the calendar icon on the left
2. File → Open & Export → Open Calendar → select your `.ics` file

### Apple Calendar
1. File → Import, then select your `.ics` file

## Tech stuff

Built with [Bulma CSS](https://bulma.io), hosted on GitHub Pages.

Feel free to open an issue if something's broken or you want a new feature.
