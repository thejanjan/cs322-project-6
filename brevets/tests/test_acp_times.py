"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""

import acp_times
import arrow

import nose    # Testing framework
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

open_time = acp_times.open_time
close_time = acp_times.close_time
seconds = acp_times.seconds


def test_opening_a():
    assert open_time(0,   200, arrow.get(0)) == arrow.get(0)
    assert open_time(60,  200, arrow.get(0)) == arrow.get(seconds(hour=1, minute=46))
    assert open_time(120, 200, arrow.get(0)) == arrow.get(seconds(hour=3, minute=32))
    assert open_time(175, 200, arrow.get(0)) == arrow.get(seconds(hour=5, minute=9))
    assert open_time(200, 200, arrow.get(0)) == arrow.get(seconds(hour=5, minute=53))


def test_closing_a():
    assert close_time(0,   200, arrow.get(0)) == arrow.get(seconds(hour=1, minute=0))
    assert close_time(60,  200, arrow.get(0)) == arrow.get(seconds(hour=4, minute=0))
    assert close_time(120, 200, arrow.get(0)) == arrow.get(seconds(hour=8, minute=0))
    assert close_time(175, 200, arrow.get(0)) == arrow.get(seconds(hour=11, minute=40))
    assert close_time(200, 200, arrow.get(0)) == arrow.get(seconds(hour=13, minute=30))


def test_opening_b():
    assert open_time(0,   600, arrow.get(0)) == arrow.get(0)
    assert open_time(100, 600, arrow.get(0)) == arrow.get(seconds(hour=2, minute=56))
    assert open_time(200, 600, arrow.get(0)) == arrow.get(seconds(hour=5, minute=53))
    assert open_time(350, 600, arrow.get(0)) == arrow.get(seconds(hour=10, minute=34))
    assert open_time(550, 600, arrow.get(0)) == arrow.get(seconds(hour=17, minute=8))


def test_closing_b():
    assert close_time(0,   600, arrow.get(0)) == arrow.get(seconds(hour=1))
    assert close_time(100, 600, arrow.get(0)) == arrow.get(seconds(hour=6, minute=40))
    assert close_time(200, 600, arrow.get(0)) == arrow.get(seconds(hour=13, minute=20))
    assert close_time(350, 600, arrow.get(0)) == arrow.get(seconds(hour=23, minute=20))
    assert close_time(550, 600, arrow.get(0)) == arrow.get(seconds(hour=36, minute=40))
    assert close_time(600, 600, arrow.get(0)) == arrow.get(seconds(hour=40, minute=0))


def test_opening_c():
    assert open_time(0,    1000, arrow.get(0)) == arrow.get(0)
    assert open_time(400,  1000, arrow.get(0)) == arrow.get(seconds(hour=12, minute=8))
    assert open_time(600,  1000, arrow.get(0)) == arrow.get(seconds(hour=18, minute=48))
    assert open_time(890,  1000, arrow.get(0)) == arrow.get(seconds(hour=29, minute=9))
    assert open_time(1000, 1000, arrow.get(0)) == arrow.get(seconds(hour=33, minute=5))


def test_closing_c():
    assert close_time(0,    1000, arrow.get(0)) == arrow.get(seconds(hour=1))
    assert close_time(400,  1000, arrow.get(0)) == arrow.get(seconds(hour=26, minute=40))
    assert close_time(600,  1000, arrow.get(0)) == arrow.get(seconds(hour=40, minute=0))
    assert close_time(890,  1000, arrow.get(0)) == arrow.get(seconds(hour=65, minute=23))
    assert close_time(1000, 1000, arrow.get(0)) == arrow.get(seconds(hour=75, minute=0))


def test_edge_cases():
    # Provided by Ali Hassani
    assert close_time(20, 400, arrow.get("2021-05-01T00:00")).format("YYYY-MM-DDTHH:mm") == \
           arrow.get("2021-05-01T02:00").format("YYYY-MM-DDTHH:mm")
    assert open_time(220, 400, arrow.get("2018-11-17T06:00")).format("YYYY-MM-DDTHH:mm") == \
           arrow.get("2018-11-17T12:30").format("YYYY-MM-DDTHH:mm")
