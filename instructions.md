i want to build a page hosted on github pages, that takes a school timetable csv file exported from nexus (a schoolbox instance), then converts the csv into an ical file, while giving options for formatting things like name, location, and event description.
it should be hosted on github pages, meaning all the conversion must be done client side
all the libraries used should be local from the github repository, and not from another url
on the website, it should use the bulma framework for a lightweight, sleek interface
it should detect what range of dates are included in the csv, because nexus doesnt export infinite range
the available data points i have are: start time, start date, end time, end date, name (which includes the full class name, year level, class code, and which group it is), and the location/classroom
there should be fields for these options: what year level (to format correctly), start date and end date to include, which school term number it is, a list of text boxes for renaming subjects,
it should save these options from above in cookies or some other method (i dont know), so it saves
instead of plain css i want to use inline bulma (i think thats what inline means), i should only need 1 html file aswell.
if there are any lightweight libraries that you think would be useful please recommend them. a good example is ics.js.
instead of having a full rename customisation, i just want to have an option where you choose to have the calendar event as either the full class name (or renamed if the user chooses to, through the renaming text boxes), or just the class code