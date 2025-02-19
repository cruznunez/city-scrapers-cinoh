from urllib.parse import urljoin

from city_scrapers_core.constants import COMMISSION
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parse


class CinohHamiltonCommissionSpider(CityScrapersSpider):
    name = "cinoh_Hamilton_Commission"
    agency = "Hamilton County Board of Commissioners"
    timezone = "America/New_York"
    start_urls = ["https://hcjfsonbase.jfs.hamilton-co.org/OnBaseAgendaOnline"]

    def parse(self, response):
        """
        Parse upcoming and past meetings from the
        Hamilton County Board of Commissioners meetings table.
        """
        location = {
            "name": "Todd B. Portune Center for County Government",
            "address": "138 East Court Street, Room 603, Cincinnati, OH 45202",
        }

        for item in response.css(".meeting-row"):
            meeting = Meeting(
                title=self._parse_title(item),
                description="",
                classification=COMMISSION,
                start=self._parse_start(item),
                end=None,
                all_day=False,
                time_notes="",
                location=location,
                links=self._parse_links(item),
                source="https://hcjfsonbase.jfs.hamilton-co.org/OnBaseAgendaOnline",
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_title(self, item):
        """Parse meeting title."""
        string = item.css(".visible-xs::text").get()
        return string.strip()

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        date = item.css("td::text")[2].get()
        return parse(date, fuzzy=True)

    # all three link types on the table--Agenda, Minutes,
    # and View Media--all link to the same page
    def _parse_links(self, item):
        """Parse links."""
        url_first_half = "https://hcjfsonbase.jfs.hamilton-co.org"
        url_second_half = item.css("::attr(href)").get()
        url = urljoin(url_first_half, url_second_half)
        if url == "https://hcjfsonbase.jfs.hamilton-co.org":
            return []
        else:
            return [{"title": "Agenda, Notes, and Media", "href": url}]
