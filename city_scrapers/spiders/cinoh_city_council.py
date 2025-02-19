from datetime import datetime

from city_scrapers_core.constants import CITY_COUNCIL, COMMITTEE
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import LegistarSpider
from dateutil.parser import parse


class CinohCityCouncilSpider(LegistarSpider):
    name = "cinoh_city_council"
    agency = "Cincinnati City Council"
    timezone = "America/New_York"
    start_urls = ["https://cincinnatioh.legistar.com/Calendar.aspx"]

    def parse_legistar(self, response):
        """
        Parse upcoming and past meetings from the
        Cincinnati City Council meetings table.

        Oftentimes, the columns: meeting details, agenda,
        minutes, and video are left blank on the calander
        but when they are, they are in the form of links.
        """
        for obj in response:
            meeting = Meeting(
                title=obj["Name"]["label"],
                description="",
                classification=self._parse_classification(obj),
                start=self.legistar_start(obj),
                end=None,
                all_day=False,
                time_notes="",
                status=self._parse_status(obj),
                location=self._parse_location(obj),
                links=self._parse_links(obj),
                source=self.legistar_source(obj),
            )

            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_classification(self, obj):
        if obj["Name"]["label"] == "Cincinnati City Council":
            return CITY_COUNCIL
        else:
            return COMMITTEE

    def _parse_status(self, obj):

        date = obj["Meeting Date"]
        parsed_date = parse(date, fuzzy=True)

        if (
            obj["Meeting Location"]
            == "Council Chambers, Room 300 NOTICE OF CANCELLATION"
        ):
            return "cancelled"
        elif parsed_date < datetime.today():
            return "passed"
        else:
            return "tentative"

    def _parse_location(self, obj):
        room = obj["Meeting Location"]
        return {"address": "801 Plum St. Cincinnati, OH 45202", "name": f"{room}"}

    def _parse_links(self, obj):

        links = []

        if obj.get("Name"):
            links.append({"title": "meeting page", "href": obj["Name"]["url"]})

        if obj.get("iCalendar"):
            links.append({"title": "iCalendar", "href": obj["iCalendar"]["url"]})

        if not obj.get("Meeting Details") == "Meeting\u00a0details":
            links.append(
                {"title": "Meeting Details", "href": obj["Meeting Details"]["url"]}
            )

        if not obj.get("Agenda") == "Not\u00a0available":
            links.append({"title": "Agenda", "href": obj["Agenda"]["url"]})

        if not obj.get("Agenda Packet") == "Not\u00a0available":
            links.append(
                {"title": "Agenda Packet", "href": obj["Agenda Packet"]["url"]}
            )

        if not obj.get("Minutes") == "Not\u00a0available":
            links.append({"title": "Minutes", "href": obj["Minutes"]["url"]})

        if not obj.get("Video") == "Not\u00a0available":
            links.append({"title": "Video", "href": obj["Video"]["url"]})

        return links
