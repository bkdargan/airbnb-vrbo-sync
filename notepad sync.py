import requests
from ics import Calendar, Event
import uuid

AIRBNB_URL = "YOUR_AIRBNB_ICAL_URL"
VRBO_URL = "YOUR_VRBO_ICAL_URL"

def fetch_calendar(url):
    r = requests.get(url)
    r.raise_for_status()
    return Calendar(r.text)

def normalize_event(e, source):
    new = Event()
    new.uid = e.uid or str(uuid.uuid4())
    new.begin = e.begin
    new.end = e.end

    guest = e.name.replace("Reserved - ", "").strip()
    if not guest:
        guest = "Guest"

    new.name = f"Reserved – {guest} (from {source})"
    return new

def merge_calendars(airbnb_cal, vrbo_cal):
    merged = Calendar()
    seen = set()

    for e in airbnb_cal.events:
        key = (e.begin, e.end)
        if key not in seen:
            merged.events.add(normalize_event(e, "Airbnb"))
            seen.add(key)

    for e in vrbo_cal.events:
        key = (e.begin, e.end)
        if key not in seen:
            merged.events.add(normalize_event(e, "VRBO"))
            seen.add(key)

    return merged

def main():
    airbnb = fetch_calendar(AIRBNB_URL)
    vrbo = fetch_calendar(VRBO_URL)

    merged = merge_calendars(airbnb, vrbo)

    with open("master.ics", "w") as f:
        f.writelines(merged)

    print("master.ics updated successfully.")

if __name__ == "__main__":
    main()
