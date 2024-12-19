from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import COMMISSION
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.cinoh_Civil_Service import CinohCivilServiceSpider

test_response = file_response(
    join(dirname(__file__), "files", "cinoh_Civil_Service.json"),
    url="https://go.boarddocs.com/oh/csc/Board.nsf/BD-GetMeetingsList",
)
spider = CinohCivilServiceSpider()

freezer = freeze_time("2024-11-06")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_count():
    assert len(parsed_items) == 12


def test_title():
    assert parsed_items[0]["title"] == "November 7, 2024 Civil Service Commission"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2024, 11, 7, 0, 0)


def test_end():
    assert parsed_items[0]["end"] is None


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert (
        parsed_items[0]["id"]
        == "cinoh_Civil_Service/202411070000/x/november_7_2024_civil_service_commission"
    )


def test_status():
    assert parsed_items[0]["status"] == "tentative"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Cincinnati Civil Service Commission",
        "address": "805 Central Ave, Suite 200, Cincinnati, OH 45202",
    }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://go.boarddocs.com/oh/csc/Board.nsf/vpublic?open#tab-meetings"
    )


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "title": "Agenda",
            "href": "https://go.boarddocs.com/oh/csc/Board.nsf/Download-AgendaDetailed?open&id=CZQLFH5631AD&current_committee_id=A9HCN931D6BA",  # noqa
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == COMMISSION


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
