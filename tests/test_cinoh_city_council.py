import json
from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import CITY_COUNCIL, COMMITTEE
from freezegun import freeze_time

from city_scrapers.spiders.cinoh_city_council import CinohCityCouncilSpider

freezer = freeze_time("2024-10-18")
freezer.start()

with open(
    join(dirname(__file__), "files", "cinoh_city_council.json"), "r", encoding="utf-8"
) as f:
    test_response = json.load(f)

spider = CinohCityCouncilSpider()
parsed_items = [item for item in spider.parse_legistar(test_response)]

freezer.stop()


def test_count():
    assert len(parsed_items) == 21


def test_title():
    assert parsed_items[0]["title"] == "Cincinnati City Council"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2024, 10, 30, 14, 0)


def test_end():
    assert parsed_items[0]["end"] is None


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert (
        parsed_items[0]["id"]
        == "cinoh_city_council/202410301400/x/cincinnati_city_council"
    )


def test_status():
    assert parsed_items[0]["status"] == "tentative"


def test_location():
    assert parsed_items[0]["location"] == {
        "address": "801 Plum St. Cincinnati, OH 45202",
        "name": "Council Chambers, Room 300",
    }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://cincinnatioh.legistar.com/DepartmentDetail.aspx"
        "?ID=38076&GUID=1CA48415-BFFD-4857-8A93-48AA89BD31C6"
    )


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "title": "meeting page",
            "href": "https://cincinnatioh.legistar.com/DepartmentDetail"
            ".aspx?ID=38076&GUID=1CA48415-BFFD-4857-8A93-48AA89BD31C6",
        },
        {
            "title": "iCalendar",
            "href": "https://cincinnatioh.legistar.com/View.ashx?M=IC&ID"
            "=1229949&GUID=40029B38-4ED1-4770-8B4F-E76E6D0FE583",
        },
    ]
    assert parsed_items[8]["links"] == [
        {
            "title": "meeting page",
            "href": "https://cincinnatioh.legistar.com/DepartmentDetail"
            ".aspx?ID=38076&GUID=1CA48415-BFFD-4857-8A93-48AA89BD31C6",
        },
        {
            "title": "iCalendar",
            "href": "https://cincinnatioh.legistar.com/View.ashx?M=IC&ID"
            "=1235477&GUID=0CC17DD2-8A13-4EC6-A533-F86D41F010D3",
        },
        {
            "title": "Meeting Details",
            "href": "https://cincinnatioh.legistar.com/MeetingDetail.aspx?ID="
            "1235477&GUID=0CC17DD2-8A13-4EC6-A533-F86D41F010D3&Options=info|&Search=",
        },
        {
            "title": "Agenda",
            "href": "https://cincinnatioh.legistar.com/View.ashx?M=A&ID=1235477&GUID="
            "0CC17DD2-8A13-4EC6-A533-F86D41F010D3",
        },
        {
            "title": "Agenda Packet",
            "href": "https://cincinnatioh.legistar.com/View.ashx?M=PA&ID=1235477&GUID="
            "0CC17DD2-8A13-4EC6-A533-F86D41F010D3",
        },
    ]


def test_classification():
    assert parsed_items[0]["classification"] == CITY_COUNCIL
    assert parsed_items[1]["classification"] == COMMITTEE


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
