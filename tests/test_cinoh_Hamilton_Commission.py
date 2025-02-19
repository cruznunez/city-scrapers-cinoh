from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import COMMISSION
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.cinoh_Hamilton_Commission import (
    CinohHamiltonCommissionSpider,
)

test_response = file_response(
    join(dirname(__file__), "files", "cinoh_Hamilton_Commission.html"),
    url="https://hcjfsonbase.jfs.hamilton-co.org/OnBaseAgendaOnline",
)
spider = CinohHamiltonCommissionSpider()

freezer = freeze_time("2024-12-31")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[0]["title"] == "Commissioners Organizational Meeting"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2025, 1, 7, 10, 0)


def test_end():
    assert parsed_items[0]["end"] is None


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert (
        parsed_items[0]["id"] == "cinoh_Hamilton_Commission/202501071000/x/"
        "commissioners_organizational_meeting"
    )


def test_status():
    assert parsed_items[0]["status"] == "tentative"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Todd B. Portune Center for County Government",
        "address": "138 East Court Street, Room 603, Cincinnati, OH 45202",
    }


def test_source():
    assert (
        parsed_items[0]["source"] == "https://hcjfsonbase.jfs.hamilton-co.org/"
        "OnBaseAgendaOnline"
    )


def test_links():
    assert parsed_items[0]["links"] == []
    assert parsed_items[20]["links"] == [
        {
            "href": "https://hcjfsonbase.jfs.hamilton-co.org/OnBaseAgendaOnline/"
            "Meetings/ViewMeeting?id=2597&doctype=1",
            "title": "Agenda, Notes, and Media",
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == COMMISSION


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
