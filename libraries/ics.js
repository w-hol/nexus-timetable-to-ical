// Lightweight iCalendar (ICS) generator
// Minimal implementation for calendar event generation

const ics = (() => {
    function formatDate(date) {
        // Format date as YYYYMMDD
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}${month}${day}`;
    }

    function formatDateTime(date) {
        // Format date/time as YYYYMMDDTHHmmss
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');
        return `${year}${month}${day}T${hours}${minutes}${seconds}`;
    }

    function escapeText(text) {
        // Escape special characters in iCalendar format
        if (!text) return '';
        return text
            .replace(/\\/g, '\\\\')
            .replace(/\n/g, '\\n')
            .replace(/,/g, '\\,')
            .replace(/;/g, '\\;');
    }

    function generateUID() {
        // Generate a unique ID
        return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}@nexus-timetable`;
    }

    return {
        events: [],

        addEvent(eventObject) {
            this.events.push(eventObject);
            return this;
        },

        download(filename = 'calendar.ics') {
            const icsContent = this.toString();
            const blob = new Blob([icsContent], { type: 'text/calendar;charset=utf-8' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = filename;
            link.click();
        },

        toString() {
            let ics = 'BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Nexus Timetable to iCal//EN\r\nCALSCALE:GREGORIAN\r\nMETHOD:PUBLISH\r\nX-WR-CALNAME:School Timetable\r\nX-WR-TIMEZONE:UTC\r\n';

            this.events.forEach(event => {
                ics += 'BEGIN:VEVENT\r\n';
                ics += `UID:${generateUID()}\r\n`;
                ics += `DTSTAMP:${formatDateTime(new Date())}\r\n`;
                ics += `DTSTART:${formatDateTime(event.start)}\r\n`;
                ics += `DTEND:${formatDateTime(event.end)}\r\n`;
                ics += `SUMMARY:${escapeText(event.title)}\r\n`;
                
                if (event.description) {
                    ics += `DESCRIPTION:${escapeText(event.description)}\r\n`;
                }
                
                if (event.location) {
                    ics += `LOCATION:${escapeText(event.location)}\r\n`;
                }

                ics += 'END:VEVENT\r\n';
            });

            ics += 'END:VCALENDAR';
            return ics;
        }
    };
})();

if (typeof module !== 'undefined' && module.exports) {
    module.exports = ics;
}
