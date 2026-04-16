import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "task4"))
from app import app


def test_header_present(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("h1", timeout=10)
    assert dash_duo.find_element("h1").text == "Pink Morsel Sales Visualiser"


def test_chart_present(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#sales-chart", timeout=10)
    assert dash_duo.find_element("#sales-chart") is not None


def test_region_picker_present(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#region-filter", timeout=10)
    labels = dash_duo.find_elements("#region-filter label")
    values = [label.text for label in labels]
    assert values == ["All", "North", "East", "South", "West"]
