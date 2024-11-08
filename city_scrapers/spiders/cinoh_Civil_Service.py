import datetime

import scrapy
from city_scrapers_core.constants import COMMISSION
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parse


class CinohCivilServiceSpider(CityScrapersSpider):
    name = "cinoh_Civil_Service"
    agency = "Cincinnati Civil Service Commission"
    timezone = "America/Chicago"
    committee_id = "A9HCN931D6BA"
    custom_settings = {
        "ROBOTSTXT_OBEY": False,
    }

    # original URL: https://go.boarddocs.com/oh/csc/Board.nsf/vpublic?open
    # clicking on meetings tab takes you to meetings index and uses API
    # we scrape API instead via POST request and ignore robots file
    def start_requests(self):
        url = "https://go.boarddocs.com/oh/csc/Board.nsf/BD-GetMeetingsList"
        form_data = {"current_committee_id": self.committee_id}
        # send the POST request and use parse method when response is returned
        yield scrapy.FormRequest(url, formdata=form_data, callback=self.parse)

    def parse(self, response):
        """
        Parse JSON response.
        """

        year = str(datetime.datetime.today().year)

        data = response.json()

        for item in data:
            numb = item.get("numberdate")

            # skip iteration if meeting is not for current year
            if numb is None or year not in numb:
                continue

            # if we are in current year then parse meeting
            meeting = Meeting(
                title=item["name"],
                description="",
                classification=COMMISSION,
                start=parse(numb),
                end=None,
                all_day=False,
                time_notes="",
                location=self._parse_location(item),
                links=self._parse_links(item),
                source=self._parse_source(response),
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_location(self, item):
        """Generate location."""
        return {
            "name": "Cincinnati Civil Service Commission",
            "address": "805 Central Ave, Suite 200, Cincinnati, OH 45202",
        }

    def _parse_links(self, item):
        """Generate links."""
        href = (
            f"https://go.boarddocs.com/oh/csc/Board.nsf/Download-AgendaDetailed?"
            f"open&id={item['unique']}&current_committee_id={self.committee_id}"
        )
        return [{"title": "Agenda", "href": href}]

    def _parse_source(self, response):
        """
        Generate source. Instead of returning API URL
        we return the more user-friendly web page we can see this data from.
        """
        return "https://go.boarddocs.com/oh/csc/Board.nsf/vpublic?open#tab-meetings"
